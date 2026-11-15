"""Postovi na javnoj stranici (UC-004; F-011, F-012).

Post upućuje na sliku iz autorove radne okoline (Post.image_id), a ne na kopiju.
Slika posta dohvaća se preko /api/posts/{id}/image: vlasnik je uvijek vidi, a drugi
prijavljeni korisnici samo ako je post javan (docs/4). Radna okolina ostaje privatna.
"""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.db import get_db
from app.models import ImageFile, Post, User
from app.workspace import own_image, preview_response

router = APIRouter(prefix="/api/posts", tags=["posts"])


class PostOut(BaseModel):
    id: int
    user_id: int
    image_id: int
    image_name: str
    image_updated_at: datetime
    description: str
    is_public: bool
    created_at: datetime
    updated_at: datetime


class PostCreate(BaseModel):
    image_id: int
    description: str = Field(default="", max_length=2000)
    is_public: bool = False


class PostUpdate(BaseModel):
    image_id: int | None = None
    description: str | None = Field(default=None, max_length=2000)
    is_public: bool | None = None


def post_out(post: Post, image: ImageFile) -> PostOut:
    return PostOut(
        id=post.id,
        user_id=post.user_id,
        image_id=image.id,
        image_name=image.name,
        image_updated_at=image.updated_at,
        description=post.description,
        is_public=post.is_public,
        created_at=post.created_at,
        updated_at=post.updated_at,
    )


def own_post(db: Session, user: User, post_id: int) -> Post:
    post = db.get(Post, post_id)
    if post is None or post.user_id != user.id:
        raise HTTPException(404, "Post ne postoji.")
    return post


@router.get("/mine", response_model=list[PostOut])
def my_posts(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Svi postovi prijavljenog korisnika, i javni i privatni, od najnovijeg."""
    rows = db.execute(
        select(Post, ImageFile)
        .join(ImageFile, Post.image_id == ImageFile.id)
        .where(Post.user_id == user.id)
        .order_by(Post.created_at.desc(), Post.id.desc())
    ).all()
    return [post_out(post, image) for post, image in rows]


@router.post("", response_model=PostOut, status_code=201)
def create_post(body: PostCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Autor posta mora biti vlasnik slike (docs/4); tuđa slika vraća 404.
    image = own_image(db, user, body.image_id)
    post = Post(
        user_id=user.id,
        image_id=image.id,
        description=body.description.strip(),
        is_public=body.is_public,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post_out(post, image)


@router.patch("/{post_id}", response_model=PostOut)
def update_post(post_id: int, body: PostUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    post = own_post(db, user, post_id)
    changes = body.model_dump(exclude_unset=True)
    if changes.get("image_id") is not None:
        post.image_id = own_image(db, user, changes["image_id"]).id
    if changes.get("description") is not None:
        post.description = changes["description"].strip()
    if changes.get("is_public") is not None:
        post.is_public = changes["is_public"]
    db.commit()
    db.refresh(post)
    return post_out(post, db.get(ImageFile, post.image_id))


@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Zapisi u favoritima drugih korisnika brišu se kaskadno (docs/4).
    db.delete(own_post(db, user, post_id))
    db.commit()
    return Response(status_code=204)


@router.get("/{post_id}/image")
def post_image(post_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Slika posta: vlasniku uvijek, ostalima samo ako je post javan (inače 404)."""
    post = db.get(Post, post_id)
    if post is None or (post.user_id != user.id and not post.is_public):
        raise HTTPException(404, "Post ne postoji.")
    return preview_response(db.get(ImageFile, post.image_id))
