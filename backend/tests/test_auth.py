"""F-001, NF-02: zaštićene rute bez valjanog tokena vraćaju 401."""
import pytest


@pytest.mark.parametrize("path", ["/api/users/me", "/api/folders/root", "/api/folders/1", "/api/images/1"])
def test_bez_tokena_401(anon_client, path):
    assert anon_client.get(path).status_code == 401


def test_neispravan_token_401(anon_client):
    r = anon_client.get("/api/users/me", headers={"Authorization": "Bearer nije.pravi.token"})
    assert r.status_code == 401


def test_health_je_javan(anon_client):
    assert anon_client.get("/api/health").json() == {"status": "ok"}


def test_istovremena_prva_prijava_vidi_pocetne_slike(monkeypatch):
    """UC-001, korak 8: frontend pri prvoj prijavi šalje više zahtjeva odjednom
    (gornja traka i radna okolina). Svaki mora vidjeti gotove početne slike."""
    import threading
    import time

    import httpx
    from fastapi.security import HTTPAuthorizationCredentials
    from sqlalchemy import func, select

    from app import auth, seed
    from app.db import SessionLocal
    from app.models import ImageFile, User
    from app.workspace import get_or_create_root

    def slow_artic():  # Artic sporo odgovori pa padne -> ugrađene slike
        time.sleep(0.5)
        raise httpx.ConnectError("nedostupno")

    monkeypatch.setattr(auth, "verify_token", lambda token: {"sub": "auth0|novi"})
    monkeypatch.setattr(auth, "_fetch_userinfo", lambda token: {"name": "Novi"})
    monkeypatch.setattr(seed, "_from_artic", slow_artic)
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="token")

    counts, errors = [], []

    def request():
        try:
            with SessionLocal() as db:
                user = auth.get_current_user(credentials, db)
                root = get_or_create_root(db, user)
                counts.append(db.scalar(
                    select(func.count()).select_from(ImageFile).where(ImageFile.folder_id == root.id)
                ))
        except Exception as e:  # noqa: BLE001
            errors.append(e)

    threads = [threading.Thread(target=request) for _ in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert errors == []
    assert counts == [3, 3, 3]
    with SessionLocal() as db:
        assert db.scalar(select(func.count()).select_from(User)) == 1
