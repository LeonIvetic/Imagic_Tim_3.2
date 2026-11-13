"""Početne slike pri prvoj prijavi (UC-001, korak 8).

Pokušava dohvatiti 3 djela iz javne domene s Artic API-ja. Ako Artic ne odgovori,
koriste se ugrađene slike iz app/seed/ (AS-03). Prijava nikad ne pada zbog Artica.
"""
import logging
from pathlib import Path

import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Folder

log = logging.getLogger(__name__)

SEED_DIR = Path(__file__).resolve().parent / "seed"
ARTIC_IMAGE = "https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg"
# Djela iz javne domene (is_public_domain = true), Art Institute of Chicago.
ARTIC_WORKS = [
    ("Seurat - Nedjelja na La Grande Jatte.jpg", "2d484387-2509-5e8e-2c43-22f9981972eb"),
    ("Van Gogh - Spavaća soba.jpg", "6644829f-f292-c5c4-a73c-0356a6fdbf0d"),
    ("Caillebotte - Pariška ulica, kišni dan.jpg", "f8fd76e9-c396-5678-36ed-6a348c904d27"),
]
HEADERS = {"User-Agent": "Imagic/0.1 (studentski projekt, FER PROGI)"}


def _from_artic() -> list[tuple[str, bytes]]:
    images = []
    with httpx.Client(timeout=4.0, headers=HEADERS, follow_redirects=True) as client:
        for name, image_id in ARTIC_WORKS:
            r = client.get(ARTIC_IMAGE.format(image_id=image_id))
            r.raise_for_status()
            images.append((name, r.content))
    return images


def _from_disk() -> list[tuple[str, bytes]]:
    return [(p.name, p.read_bytes()) for p in sorted(SEED_DIR.iterdir()) if p.is_file()]


def seed_initial_images(db: Session, root: Folder) -> None:
    from app.workspace import store_image  # izbjegava kružni import

    try:
        stored = _store_all(db, root, _from_artic(), store_image)
    except (httpx.HTTPError, OSError) as e:
        log.warning("Artic nije dostupan (%s), koriste se ugrađene slike.", e)
        stored = 0
    if stored == 0:
        # Artic ne radi ili nije vratio slike (npr. HTML stranicu): ugrađene slike.
        _store_all(db, root, _from_disk(), store_image)


def _store_all(db, root, images, store_image) -> int:
    stored = 0
    for name, data in images:
        try:
            store_image(db, root, name, data)
            stored += 1
        except HTTPException as e:
            log.warning("Početna slika %s nije spremljena: %s", name, e.detail)
    return stored
