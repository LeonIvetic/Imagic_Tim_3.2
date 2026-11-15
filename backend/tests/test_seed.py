"""UC-001, korak 8 i AS-03: početne slike, i kad Artic ne radi."""
import httpx

from app import seed
from app.db import SessionLocal
from app.models import ImageFile, User
from app.workspace import get_or_create_root


def test_bez_artica_koriste_se_ugradene_slike(users, monkeypatch):
    def artic_down():
        raise httpx.ConnectError("nema mreže")
    monkeypatch.setattr(seed, "_from_artic", artic_down)

    with SessionLocal() as db:
        root = get_or_create_root(db, db.get(User, users["ana"]))
        seed.seed_initial_images(db, root)
        assert db.query(ImageFile).filter_by(folder_id=root.id).count() == 3
