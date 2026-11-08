"""Rute vezane uz korisnike."""
from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict

from app.auth import get_current_user
from app.models import User 

router = APIRouter(prefix="/api/users", tags=["users"])


class UserOut(BaseModel):
    """Odgovor za korisnika. Namjerno BEZ auth0_sub."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str | None = None
    email: str | None = None
    display_name: str | None = None
    avatar_url: str | None = None
    bio: str | None = None


@router.get("/me", response_model=UserOut)
def read_me(user: User = Depends(get_current_user)):
    return user
