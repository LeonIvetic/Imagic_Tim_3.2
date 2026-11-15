"""Pohrana datoteka slika na disku i provjera formata (F-002, NF-05).

Baza čuva samo zapis (ImageFile.file_path), a sama datoteka je u UPLOAD_DIR
pod nasumičnim imenom (uuid4), pa korisnikovo ime datoteke nikad ne dolazi do diska.
"""
import io
import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from PIL import Image, UnidentifiedImageError

load_dotenv()

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", Path(__file__).resolve().parent.parent / "uploads"))
MAX_BYTES = 10 * 1024 * 1024

# Pillow format -> (oznaka u bazi, nastavak datoteke, MIME tip)
FORMATS = {
    "JPEG": ("jpeg", "jpg", "image/jpeg"),
    "PNG": ("png", "png", "image/png"),
    "TIFF": ("tiff", "tif", "image/tiff"),
    "WEBP": ("webp", "webp", "image/webp"),
}
MIME_BY_FORMAT = {fmt: mime for fmt, _, mime in FORMATS.values()}
# Preglednici ne prikazuju TIFF, pa se za prikaz pretvara u PNG.
BROWSER_FORMATS = {"jpeg", "png", "webp"}


class InvalidImage(ValueError):
    """Datoteka nije podržana slika. Poruka je namijenjena korisniku."""


def detect_format(data: bytes) -> str:
    """Vraća oznaku formata ('jpeg', 'png', 'tiff', 'webp') prema sadržaju, ne prema nastavku."""
    try:
        with Image.open(io.BytesIO(data)) as img:
            pil_format = img.format
            img.verify()
    except (UnidentifiedImageError, OSError, SyntaxError):
        raise InvalidImage("Datoteka nije ispravna slika.")
    if pil_format not in FORMATS:
        raise InvalidImage("Podržani formati su JPEG, PNG, TIFF i WebP.")
    return FORMATS[pil_format][0]


def extension(fmt: str) -> str:
    return next(ext for f, ext, _ in FORMATS.values() if f == fmt)


def save(data: bytes, fmt: str) -> str:
    """Sprema datoteku i vraća relativnu putanju za ImageFile.file_path."""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    rel = f"{uuid.uuid4().hex}.{extension(fmt)}"
    (UPLOAD_DIR / rel).write_bytes(data)
    return rel


def absolute(rel: str) -> Path:
    return UPLOAD_DIR / rel


def delete(rel: str) -> None:
    try:
        (UPLOAD_DIR / rel).unlink()
    except FileNotFoundError:
        pass


def dimensions(rel: str) -> tuple[int, int] | None:
    try:
        with Image.open(absolute(rel)) as img:
            return img.size
    except (OSError, UnidentifiedImageError):
        return None


def browser_preview(rel: str) -> bytes:
    """PNG inačica slike za prikaz u pregledniku (koristi se za TIFF)."""
    with Image.open(absolute(rel)) as img:
        img.seek(0)
        if img.mode not in ("RGB", "RGBA", "L", "LA"):
            img = img.convert("RGBA")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
