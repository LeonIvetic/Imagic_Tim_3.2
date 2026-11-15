"""Rute vezane uz korisnike i javnu stranicu (F-010)."""
import re

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.db import get_db
from app.models import User

router = APIRouter(prefix="/api/users", tags=["users"])

USERNAME_RE = re.compile(r"[A-Za-z0-9_.]{1,50}")


class UserOut(BaseModel):
    """Odgovor za korisnika. Namjerno BEZ auth0_sub."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str | None = None
    email: str | None = None
    display_name: str | None = None
    avatar_url: str | None = None
    bio: str | None = None


class ProfileUpdate(BaseModel):
    """Polja koja vlasnik smije mijenjati. Izostavljeno polje ostaje nepromijenjeno."""

    username: str | None = Field(default=None, max_length=50)
    display_name: str | None = Field(default=None, max_length=255)
    bio: str | None = Field(default=None, max_length=1000)
    avatar_url: str | None = Field(default=None, max_length=500)


@router.get("/me", response_model=UserOut)
def read_me(user: User = Depends(get_current_user)):
    return user


@router.patch("/me", response_model=UserOut)
def update_me(body: ProfileUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Uređivanje vlastite javne stranice. Tuđi profil nije moguće mijenjati jer ruta radi samo nad /me."""
    user = db.get(User, user.id)  # zapis u ovoj sesiji, da se izmjene spreme
    changes = body.model_dump(exclude_unset=True)

    if "username" in changes:
        username = (changes["username"] or "").strip()
        if not USERNAME_RE.fullmatch(username):
            raise HTTPException(422, "Korisničko ime smije sadržavati samo slova, brojke, _ i . (najviše 50 znakova).")
        taken = db.scalar(select(User.id).where(User.username == username, User.id != user.id))
        if taken is not None:
            raise HTTPException(409, "Korisničko ime je zauzeto.")
        changes["username"] = username

    if "display_name" in changes:
        changes["display_name"] = (changes["display_name"] or "").strip() or None

    if "bio" in changes:
        changes["bio"] = (changes["bio"] or "").strip() or None

    if "avatar_url" in changes:
        url = (changes["avatar_url"] or "").strip()
        if url and not url.lower().startswith(("https://", "http://")):
            raise HTTPException(422, "URL slike mora počinjati s http:// ili https://.")
        changes["avatar_url"] = url or None

    for field, value in changes.items():
        setattr(user, field, value)
    try:
        db.commit()
    except IntegrityError:  # istovremeni zahtjev je zauzeo isto korisničko ime
        db.rollback()
        raise HTTPException(409, "Korisničko ime je zauzeto.")
    db.refresh(user)
    return user
