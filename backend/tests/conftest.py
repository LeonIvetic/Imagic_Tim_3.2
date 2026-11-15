"""Zajednička postava testova: zasebna baza imagic_test i privremena mapa za slike.

Pokretanje (iz mape backend, uz pokrenut `docker compose up -d`):
    python -m pytest
"""
import io
import os
import tempfile

import psycopg
import pytest
from PIL import Image

TEST_DB = "imagic_test"
os.environ["DATABASE_URL"] = f"postgresql+psycopg://imagic:imagic@localhost:5433/{TEST_DB}"
os.environ["UPLOAD_DIR"] = tempfile.mkdtemp(prefix="imagic-uploads-")

# Stvori testnu bazu ako ne postoji (prije uvoza aplikacije).
with psycopg.connect("postgresql://imagic:imagic@localhost:5433/postgres", autocommit=True) as conn:
    if not conn.execute("SELECT 1 FROM pg_database WHERE datname = %s", (TEST_DB,)).fetchone():
        conn.execute(f"CREATE DATABASE {TEST_DB}")

from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import text  # noqa: E402

from app.auth import get_current_user  # noqa: E402
from app.db import Base, SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models import User  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def schema():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(autouse=True)
def clean_tables():
    yield
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE users, folders, image_files, posts, favorite_posts, "
                          "favorite_profiles RESTART IDENTITY CASCADE"))
    app.dependency_overrides.clear()


@pytest.fixture
def users():
    """Dva korisnika: ana (prijavljena po zadanom) i ivo."""
    with SessionLocal() as db:
        ana = User(auth0_sub="auth0|ana", username="ana")
        ivo = User(auth0_sub="auth0|ivo", username="ivo")
        db.add_all([ana, ivo])
        db.commit()
        return {"ana": ana.id, "ivo": ivo.id}


@pytest.fixture
def login(users):
    """login('ivo') mijenja prijavljenog korisnika (zamjena za Auth0 token)."""
    def _login(name):
        user_id = users[name]

        def current_user():
            with SessionLocal() as db:
                return db.get(User, user_id)

        app.dependency_overrides[get_current_user] = current_user
    _login("ana")
    return _login


@pytest.fixture
def client(login):
    return TestClient(app)


@pytest.fixture
def anon_client():
    return TestClient(app)


def make_image(fmt="PNG", size=(40, 30)) -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", size, (200, 30, 30)).save(buf, format=fmt)
    return buf.getvalue()
