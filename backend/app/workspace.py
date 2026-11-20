"""Radna okolina: mape i slike (UC-002; F-002, F-003, F-004, F-016).

Svaka ruta radi samo nad mapama i slikama prijavljenog korisnika. Tuđa mapa ili
slika vraća 404, jednako kao nepostojeća, da se ne otkriva njezino postojanje (NF-02).
"""
from datetime import datetime
from pathlib import PurePath
from typing import Literal

from fastapi import APIRouter, Depends, File, Form, HTTPException, Response, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from PIL import Image
from app.filters import FilterName, MultiFrameImage, render_filters

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
    
class ImageFilterRequest(BaseModel):
    filters: list[FilterName] = Field(min_length=1)
    source_updated_at: datetime
    action: Literal["preview", "copy", "overwrite"]
    name: str | None = Field(default=None, max_length=255)


# Slika se prepisuje pod istim URL-om (filteri), pa preglednik mora svaki put
# provjeriti ETag kod servera umjesto da prikaže staru kopiju iz cachea.
NO_CACHE = {"Cache-Control": "no-cache"}


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


def name_with_suffix(name: str, fmt: str) -> str:
    """Usklađuje nastavak imena s formatom slike, da se datoteka preuzme s ispravnim nastavkom.

    'slika' -> 'slika.png', 'slika.jpg' (a format je PNG) -> 'slika.png', 'slika.JPEG' ostaje.
    """
    allowed = storage.SUFFIXES[fmt]
    p = PurePath(name)
    if p.suffix.lower() in allowed:
        return name
    known = {s for suffixes in storage.SUFFIXES.values() for s in suffixes}
    stem = p.stem if p.suffix.lower() in known else name
    return f"{stem[:255 - len(allowed[0])]}{allowed[0]}"


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


def own_image(db: Session, user: User, image_id: int, *, lock: bool = False) -> ImageFile:
    # Vlasnik slike je vlasnik njezine mape (docs/4).
    query = (
        select(ImageFile)
        .join(Folder, ImageFile.folder_id == Folder.id)
        .where(ImageFile.id == image_id, Folder.owner_id == user.id)
    )
    if lock:
        query = query.with_for_update(of=ImageFile)
    image = db.scalar(query)
    if image is None:
        raise HTTPException(404, "Slika ne postoji")
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
    while True:
        marker = f" ({i})"
        available = 255 - len(marker) - len(suffix)
        if available > 0:
            candidate = f"{stem[:available]}{marker}{suffix}"
        else:
            candidate = f"{name[:255 - len(marker)]}{marker}"
        if not name_taken_image(db, folder_id, candidate):
            return candidate
        i += 1
        

def commit_or_conflict(db: Session, message: str) -> None:
    """Commit; ako istovremeni zahtjev zauzme isto ime, vraća 409 umjesto 500."""
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(409, message) from exc


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

    name = unique_image_name(db, folder.id, name_with_suffix(clean_name(name), fmt))
    rel = storage.save(data, fmt)
    image = ImageFile(
        folder_id=folder.id,
        name=name,
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
    commit_or_conflict(db, "Mapa s tim imenom već postoji.")
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
    commit_or_conflict(db, "Mapa s tim imenom već postoji.")
    db.refresh(folder)
    return folder


@router.delete("/folders/{folder_id}", status_code=204)
def delete_folder(folder_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    folder = own_folder(db, user, folder_id)
    if folder.parent_id is None:
        raise HTTPException(400, "Korijensku mapu nije moguće obrisati.")

    # Baza kaskadno briše podmape i zapise slika, a datoteke s diska brišemo sami.
    ids = descendant_ids(db, user, folder.id)
    files = db.scalars(
        select(ImageFile.file_path).where(ImageFile.folder_id.in_(ids)).with_for_update()
        ).all()
    db.delete(folder)
    db.commit()
    for rel in files:
        storage.delete(rel)
    return Response(status_code=204)


# ---------- Slike ----------

@router.get("/images", response_model=list[ImageOut])
def all_images(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Sve slike korisnika iz svih mapa (npr. za odabir slike pri objavi posta)."""
    return db.scalars(
        select(ImageFile)
        .join(Folder, ImageFile.folder_id == Folder.id)
        .where(Folder.owner_id == user.id)
        .order_by(ImageFile.name, ImageFile.id)
    ).all()


def preview_response(image: ImageFile) -> Response:
    """Slika za prikaz u pregledniku; TIFF se pretvara u PNG. Pozivatelj provjerava pravo pristupa."""
    if image.format in storage.BROWSER_FORMATS:
        path = storage.absolute(image.file_path)
        if not path.exists():
            raise HTTPException(404, "Datoteka slike nije pronađena.")
        return FileResponse(path, media_type=storage.MIME_BY_FORMAT[image.format], headers=NO_CACHE)
    return Response(storage.browser_preview(image.file_path), media_type="image/png", headers=NO_CACHE)


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
        headers=NO_CACHE,
    )


@router.get("/images/{image_id}/preview")
def image_preview(image_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Slika za prikaz u pregledniku; TIFF se pretvara u PNG."""
    return preview_response(own_image(db, user, image_id))

@router.post("/images/{image_id}/filters", response_model=ImageOut)
def filter_image(
    # IZMIJENJUJE ORIGINALNU SLIKU PRI SPREMANJU
    image_id: int,
    body: ImageFilterRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    preview = body.action == "preview"
    image = own_image(db, user, image_id, lock=not preview)
    if image.updated_at != body.source_updated_at:
        raise HTTPException(409, "Slika je u međuvremenu izmijenjena. Osvježi stranicu pa ponovi obradu.")
    
    name = clean_name(body.name or "") if body.action == "copy" else None
    old_path = image.file_path
    try:
        result = render_filters(storage.absolute(old_path), body.filters, preview=preview)
    except FileNotFoundError as exc:
        raise HTTPException(404, "Datoteka slike nije pronađena.") from exc
    except MultiFrameImage as exc:
        raise HTTPException(422, str(exc)) from exc
    except (OSError, SyntaxError, Image.DecompressionBombError) as exc:
        raise HTTPException(422, "Datoteku slike nije moguće obraditi.") from exc
    
    if preview:
        fmt = "png" if image.format == "tiff" else image.format
        return Response(result, media_type=storage.MIME_BY_FORMAT[fmt], headers={"Cache-Control": "no-store"})

    if len(result) > storage.MAX_BYTES:
        raise HTTPException(413, "Obrađena slika je veća od 10 MB.")
    
    if name is not None:
        try:
            return store_image(db, db.get(Folder, image.folder_id), name, result)
        except IntegrityError as exc:
            raise HTTPException(409, "Spremanje nije uspjelo. Pokušaj ponovno.") from exc
        
    new_path = storage.save(result, image.format)
    image.file_path = new_path
    image.size_bytes = len(result)
    image.updated_at = func.now()  # mijenja se samo pri promjeni sadržaja (models.py)
    try:
        db.commit()
    except Exception:
        db.rollback()
        storage.delete(new_path)
        raise
    storage.delete(old_path)
    db.refresh(image)
    return image


@router.patch("/images/{image_id}", response_model=ImageOut)
def update_image(image_id: int, body: ImageUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    image = own_image(db, user, image_id)
    target = image.folder_id
    if body.folder_id is not None:
        target = own_folder(db, user, body.folder_id).id
    name = name_with_suffix(clean_name(body.name), image.format) if body.name is not None else image.name
    if name_taken_image(db, target, name, exclude=image.id):
        raise HTTPException(409, "Slika s tim imenom već postoji u odredišnoj mapi.")
    image.name, image.folder_id = name, target
    commit_or_conflict(db, "Slika s tim imenom već postoji u odredišnoj mapi.")
    db.refresh(image)
    return image


@router.delete("/images/{image_id}", status_code=204)
def delete_image(image_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    image = own_image(db, user, image_id, lock=True)
    rel = image.file_path
    db.delete(image)  # postovi sa slikom brišu se kaskadno (docs/4)
    db.commit()
    storage.delete(rel)
    return Response(status_code=204)
