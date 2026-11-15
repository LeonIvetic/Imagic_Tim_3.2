"""SQLAlchemy modeli. Odgovaraju ER dijagramu i ograničenjima iz docs/4 (4.3)."""
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    auth0_sub: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    email: Mapped[Optional[str]] = mapped_column(String(255))
    username: Mapped[Optional[str]] = mapped_column(String(50), unique=True)
    display_name: Mapped[Optional[str]] = mapped_column(String(255))
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500))
    bio: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Folder(Base):
    """Mapa radne okoline. Korijenska mapa ima parent_id = NULL (jedna po korisniku)."""

    __tablename__ = "folders"
    __table_args__ = (
        # Jedinstveno ime unutar roditelja (za korijen vrijedi indeks ispod).
        UniqueConstraint("owner_id", "parent_id", "name", name="uq_folders_owner_parent_name"),
        Index(
            "uq_folders_one_root_per_user",
            "owner_id",
            unique=True,
            postgresql_where=text("parent_id IS NULL"),
        ),
        CheckConstraint("parent_id IS NULL OR parent_id <> id", name="ck_folders_not_own_parent"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("folders.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class ImageFile(Base):
    """Zapis o slici. Sama datoteka je na disku (file_path relativno na UPLOAD_DIR)."""

    __tablename__ = "image_files"
    __table_args__ = (
        UniqueConstraint("folder_id", "name", name="uq_image_files_folder_name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    folder_id: Mapped[int] = mapped_column(
        ForeignKey("folders.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String(255))
    format: Mapped[str] = mapped_column(String(10))
    size_bytes: Mapped[Optional[int]] = mapped_column(Integer)
    file_path: Mapped[str] = mapped_column(String(500), unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    image_id: Mapped[int] = mapped_column(
        ForeignKey("image_files.id", ondelete="CASCADE"), index=True
    )
    description: Mapped[str] = mapped_column(Text)
    is_public: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class FavoritePost(Base):
    __tablename__ = "favorite_posts"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class FavoriteProfile(Base):
    __tablename__ = "favorite_profiles"
    __table_args__ = (
        CheckConstraint("user_id <> profile_user_id", name="ck_favorite_profiles_not_self"),
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    profile_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
