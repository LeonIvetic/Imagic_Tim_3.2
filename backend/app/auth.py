"""Auth0 autorizacija: provjera JWT access tokena i dependency get_current_user."""
import os

import httpx
import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import get_db 
from app.models import User 

load_dotenv()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "").strip()
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", "").strip()
if not AUTH0_DOMAIN or not AUTH0_AUDIENCE:
    raise RuntimeError(
        "AUTH0_DOMAIN i AUTH0_AUDIENCE moraju biti postavljeni u backend/.env "
        "(vidi backend/.env.example)."
    )

# Napravi se jednom pri učitavanju modula; PyJWKClient sam cachira ključeve.
jwks = jwt.PyJWKClient(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")


def verify_token(token: str) -> dict:
    key = jwks.get_signing_key_from_jwt(token).key
    return jwt.decode(
        token,
        key,
        algorithms=["RS256"],
        audience=AUTH0_AUDIENCE,
        issuer=f"https://{AUTH0_DOMAIN}/",  # kosa crta na kraju je obavezna
    )


bearer_scheme = HTTPBearer(auto_error=False)


def _unauthorized() -> HTTPException:
    return HTTPException(
        status_code=401,
        detail="Nedostaje ili je neispravan token",
        headers={"WWW-Authenticate": "Bearer"},
    )


def _fetch_userinfo(access_token: str) -> dict:
    """Profil korisnika s Auth0 (email, name, picture) pomoću istog access tokena."""
    try:
        response = httpx.get(
            f"https://{AUTH0_DOMAIN}/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=5.0,
        )
        response.raise_for_status()
        return response.json()
    except (httpx.HTTPError, ValueError):
        raise HTTPException(status_code=502, detail="Auth0 profil trenutno nije dostupan")


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise _unauthorized()

    try:
        payload = verify_token(credentials.credentials)
    except jwt.PyJWTError:  # uključuje istek, krivi aud/iss i PyJWKClientError
        raise _unauthorized()

    sub = payload["sub"]
    user = db.scalar(select(User).where(User.auth0_sub == sub))
    if user is not None:
        return user

    # Prva prijava: dohvati profil s Auth0 i stvori korisnika.
    info = _fetch_userinfo(credentials.credentials)
    user = User(
        auth0_sub=sub,
        email=info.get("email"),
        display_name=info.get("name"),
        avatar_url=info.get("picture"),
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        # Dva istovremena prva zahtjeva istog korisnika: drugi je već stvorio redak.
        db.rollback()
        user = db.scalar(select(User).where(User.auth0_sub == sub))
        if user is None:
            raise
        return user
    db.refresh(user)

    # Prva prijava: korijenska mapa i 3 početne slike (UC-001, korak 8).
    from app.seed import seed_initial_images
    from app.workspace import get_or_create_root

    seed_initial_images(db, get_or_create_root(db, user))
    return user
