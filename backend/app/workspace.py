"""Radna okolina: mape i slike (UC-002; F-002, F-003, F-004, F-016).

Svaka ruta radi samo nad mapama i slikama prijavljenog korisnika. Tuđa mapa ili
slika vraća 404, jednako kao nepostojeća, da se ne otkriva njezino postojanje (NF-02).
"""
from datetime import datetime
from pathlib import PurePath

from fastapi import APIRouter, Depends, File, Form, HTTPException, Response, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import storage
from app.auth import get_current_user
from app.db import get_db
from app.models import Folder, ImageFile, User

router = APIRouter(prefix="/api", tags=["workspace"])

ROOT_NAME = "Radna okolina"


# ---------- Sheme ----------

class FolderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    parent_id: int | None
    name: str
    created_at: datetime


class ImageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    folder_id: int
    name: str
    format: str
    size_bytes: int | None
    created_at: datetime
    updated_at: datetime


class ImageDetail(ImageOut):
    width: int | None = None
    height: int | None = None
    path: list[FolderOut]


class FolderContent(BaseModel):
    folder: FolderOut
    path: list[FolderOut]
    folders: list[FolderOut]
    images: list[ImageOut]


class FolderCreate(BaseModel):
    parent_id: int
    name: str = Field(max_length=255)


class FolderUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    parent_id: int | None = None


class ImageUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    folder_id: int | None = None


# ---------- Pomoćne funkcije ----------

def clean_name(name: str) -> str:
    name = name.strip()
    if not name:
        raise HTTPException(422, "Naziv ne smije biti prazan.")
    if "/" in name or "\\" in name or name in (".", ".."):
        raise HTTPException(422, "Naziv ne smije sadržavati znakove / i \\.")
    if len(name) > 255:
        raise HTTPException(422, "Naziv smije imati najviše 255 znakova.")
    return name


def get_or_create_root(db: Session, user: User) -> Folder:
    """Svaki korisnik ima točno jednu korijensku mapu (docs/4)."""
    root = db.scalar(select(Folder).where(Folder.owner_id == user.id, Folder.parent_id.is_(None)))
    if root is not None:
        return root
    root = Folder(owner_id=user.id, parent_id=None, name=ROOT_NAME)
    db.add(root)
    try:
        db.commit()
    except IntegrityError:  # istovremeni zahtjev je već stvorio korijen
        db.rollback()
        return db.scalar(select(Folder).where(Folder.owner_id == user.id, Folder.parent_id.is_(None)))
    db.refresh(root)
    return root


def own_folder(db: Session, user: User, folder_id: int) -> Folder:
    folder = db.get(Folder, folder_id)
    if folder is None or folder.owner_id != user.id:
        raise HTTPException(404, "Mapa ne postoji.")
    return folder


def own_image(db: Session, user: User, image_id: int) -> ImageFile:
    # Vlasnik slike je vlasnik njezine mape (docs/4).
    image = db.scalar(
        select(ImageFile)
        .join(Folder, ImageFile.folder_id == Folder.id)
        .where(ImageFile.id == image_id, Folder.owner_id == user.id)
    )
    if image is None:
        raise HTTPException(404, "Slika ne postoji.")
    return image


def folder_path(db: Session, folder: Folder) -> list[Folder]:
    path = [folder]
    while path[0].parent_id is not None:
        path.insert(0, db.get(Folder, path[0].parent_id))
    return path


def descendant_ids(db: Session, user: User, folder_id: int) -> set[int]:
    """Id-jevi mape i svih njezinih podmapa."""
    children: dict[int | None, list[int]] = {}
    for f_id, parent in db.execute(
        select(Folder.id, Folder.parent_id).where(Folder.owner_id == user.id)
    ):
        children.setdefault(parent, []).append(f_id)
    result, stack = set(), [folder_id]
    while stack:
        current = stack.pop()
        result.add(current)
        stack.extend(children.get(current, []))
    return result


def name_taken_folder(db: Session, user: User, parent_id: int, name: str, exclude: int | None = None) -> bool:
    q = select(Folder.id).where(
        Folder.owner_id == user.id, Folder.parent_id == parent_id, Folder.name == name
    )
    if exclude is not None:
        q = q.where(Folder.id != exclude)
    return db.scalar(q) is not None


def name_taken_image(db: Session, folder_id: int, name: str, exclude: int | None = None) -> bool:
    q = select(ImageFile.id).where(ImageFile.folder_id == folder_id, ImageFile.name == name)
    if exclude is not None:
        q = q.where(ImageFile.id != exclude)
    return db.scalar(q) is not None


def unique_image_name(db: Session, folder_id: int, name: str) -> str:
    """'slika.jpg' -> 'slika (1).jpg' ako ime u mapi već postoji."""
    if not name_taken_image(db, folder_id, name):
        return name
    p = PurePath(name)
    stem, suffix = p.stem, p.suffix
    i = 1
    while name_taken_image(db, folder_id, f"{stem} ({i}){suffix}"):
        i += 1
    return f"{stem} ({i}){suffix}"


def store_image(db: Session, folder: Folder, name: str, data: bytes) -> ImageFile:
    """Provjeri i spremi sliku u mapu. Koristi se za upload i za početne slike."""
    if len(data) == 0:
        raise HTTPException(422, "Datoteka je prazna.")
    if len(data) > storage.MAX_BYTES:
        raise HTTPException(413, "Slika je veća od 10 MB.")
    try:
        fmt = storage.detect_format(data)
    except storage.InvalidImage as e:
        raise HTTPException(415, str(e))

    rel = storage.save(data, fmt)
    image = ImageFile(
        folder_id=folder.id,
        name=unique_image_name(db, folder.id, clean_name(name)),
        format=fmt,
        size_bytes=len(data),
        file_path=rel,
    )
    db.add(image)
    try:
        db.commit()
    except Exception:
        db.rollback()
        storage.delete(rel)
        raise
    db.refresh(image)
    return image


# ---------- Mape ----------

@router.get("/folders/root", response_model=FolderOut)
def root_folder(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_or_create_root(db, user)


@router.get("/folders", response_model=list[FolderOut])
def all_folders(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Sve mape korisnika (za stablo i odabir odredišta pri premještanju)."""
    get_or_create_root(db, user)
    return db.scalars(
        select(Folder).where(Folder.owner_id == user.id).order_by(Folder.name)
    ).all()


@router.get("/folders/{folder_id}", response_model=FolderContent)
def folder_content(folder_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    folder = own_folder(db, user, folder_id)
    folders = db.scalars(
        select(Folder).where(Folder.parent_id == folder.id).order_by(Folder.name)
    ).all()
    images = db.scalars(
        select(ImageFile).where(ImageFile.folder_id == folder.id).order_by(ImageFile.name)
    ).all()
    return FolderContent(
        folder=folder, path=folder_path(db, folder), folders=folders, images=images
    )


@router.post("/folders", response_model=FolderOut, status_code=201)
def create_folder(body: FolderCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    parent = own_folder(db, user, body.parent_id)
    name = clean_name(body.name)
    if name_taken_folder(db, user, parent.id, name):
        raise HTTPException(409, "Mapa s tim imenom već postoji.")
    folder = Folder(owner_id=user.id, parent_id=parent.id, name=name)
    db.add(folder)
    db.commit()
    db.refresh(folder)
    return folder


@router.patch("/folders/{folder_id}", response_model=FolderOut)
def update_folder(folder_id: int, body: FolderUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    folder = own_folder(db, user, folder_id)
    if folder.parent_id is None:
        raise HTTPException(400, "Korijensku mapu nije moguće mijenjati.")

    new_parent = folder.parent_id
    if body.parent_id is not None and body.parent_id != folder.parent_id:
        own_folder(db, user, body.parent_id)
        if body.parent_id in descendant_ids(db, user, folder.id):
            raise HTTPException(400, "Mapu nije moguće premjestiti u nju samu ili njezinu podmapu.")
        new_parent = body.parent_id

    new_name = clean_name(body.name) if body.name is not None else folder.name
    if name_taken_folder(db, user, new_parent, new_name, exclude=folder.id):
        raise HTTPException(409, "Mapa s tim imenom već postoji.")

    folder.name, folder.parent_id = new_name, new_parent
    db.commit()
    db.refresh(folder)
    return folder


@router.delete("/folders/{folder_id}", status_code=204)
def delete_folder(folder_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    folder = own_folder(db, user, folder_id)
    if folder.parent_id is None:
        raise HTTPException(400, "Korijensku mapu nije moguće obrisati.")

    # Baza kaskadno briše podmape i zapise slika, a datoteke s diska brišemo sami.
    ids = descendant_ids(db, user, folder.id)
    files = db.scalars(select(ImageFile.file_path).where(ImageFile.folder_id.in_(ids))).all()
    db.delete(folder)
    db.commit()
    for rel in files:
        storage.delete(rel)
    return Response(status_code=204)


# ---------- Slike ----------

@router.post("/images", response_model=ImageOut, status_code=201)
async def upload_image(
    folder_id: int = Form(...),
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    folder = own_folder(db, user, folder_id)
    data = await file.read(storage.MAX_BYTES + 1)
    return store_image(db, folder, file.filename or "slika", data)


@router.get("/images/{image_id}", response_model=ImageDetail)
def image_detail(image_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    image = own_image(db, user, image_id)
    size = storage.dimensions(image.file_path)
    return ImageDetail(
        **ImageOut.model_validate(image).model_dump(),
        width=size[0] if size else None,
        height=size[1] if size else None,
        path=folder_path(db, db.get(Folder, image.folder_id)),
    )


@router.get("/images/{image_id}/file")
def image_file(
    image_id: int,
    download: bool = False,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Izvorna datoteka. S ?download=true preglednik je sprema pod imenom slike."""
    image = own_image(db, user, image_id)
    path = storage.absolute(image.file_path)
    if not path.exists():
        raise HTTPException(404, "Datoteka slike nije pronađena.")
    return FileResponse(
        path,
        media_type=storage.MIME_BY_FORMAT[image.format],
        filename=image.name if download else None,
    )


@router.get("/images/{image_id}/preview")
def image_preview(image_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Slika za prikaz u pregledniku; TIFF se pretvara u PNG."""
    image = own_image(db, user, image_id)
    if image.format in storage.BROWSER_FORMATS:
        return image_file(image_id, False, user, db)
    return Response(storage.browser_preview(image.file_path), media_type="image/png")


@router.patch("/images/{image_id}", response_model=ImageOut)
def update_image(image_id: int, body: ImageUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    image = own_image(db, user, image_id)
    target = image.folder_id
    if body.folder_id is not None:
        target = own_folder(db, user, body.folder_id).id
    name = clean_name(body.name) if body.name is not None else image.name
    if name_taken_image(db, target, name, exclude=image.id):
        raise HTTPException(409, "Slika s tim imenom već postoji u odredišnoj mapi.")
    image.name, image.folder_id = name, target
    db.commit()
    db.refresh(image)
    return image


@router.delete("/images/{image_id}", status_code=204)
def delete_image(image_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    image = own_image(db, user, image_id)
    rel = image.file_path
    db.delete(image)  # postovi sa slikom brišu se kaskadno (docs/4)
    db.commit()
    storage.delete(rel)
    return Response(status_code=204)
