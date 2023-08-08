from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from sqlalchemy import MetaData
from .types import varchar, TYPE_ANNOTATION_MAP
from .common import _create_tables

metadata_obj = MetaData(schema="mflix")


class Base(DeclarativeBase):
    metadata = metadata_obj
    type_annotation_map = TYPE_ANNOTATION_MAP


class User(Base):
    __tablename__ = "users"

    id: Mapped[varchar] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    preferences: Mapped[dict] = mapped_column(nullable=True)


class Theater(Base):
    __tablename__ = "theaters"

    id: Mapped[varchar] = mapped_column(primary_key=True)
    theaterId: Mapped[int]
    location: Mapped[dict]


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[varchar] = mapped_column(primary_key=True)
    user_id: Mapped[str]
    jwt: Mapped[str] = mapped_column(comment="JSON Web Token")


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[varchar] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=True)
    year: Mapped[int] = mapped_column(nullable=True)
    runtime: Mapped[int] = mapped_column(nullable=True)
    released: Mapped[datetime] = mapped_column(nullable=True)
    poster: Mapped[str] = mapped_column(nullable=True)
    plot: Mapped[str] = mapped_column(nullable=True)
    fullplot: Mapped[str] = mapped_column(nullable=True)
    lastupdated: Mapped[datetime] = mapped_column(nullable=True)
    type: Mapped[str] = mapped_column(nullable=True)
    directors: Mapped[list[str]] = mapped_column(nullable=True)
    imdb: Mapped[dict] = mapped_column(nullable=True)
    cast: Mapped[list[str]] = mapped_column(nullable=True)
    countries: Mapped[list[str]] = mapped_column(nullable=True)
    genres: Mapped[list[str]] = mapped_column(nullable=True)
    tomatoes: Mapped[dict] = mapped_column(nullable=True)
    num_mflix_comments: Mapped[int] = mapped_column(nullable=True)
    rated: Mapped[str] = mapped_column(nullable=True)
    awards: Mapped[dict] = mapped_column(nullable=True)
    languages: Mapped[list[str]] = mapped_column(nullable=True)
    writers: Mapped[list[str]] = mapped_column(nullable=True)
    metacritic: Mapped[int] = mapped_column(nullable=True)


class Comment(Base):
    __tablename__ = "comments"
    __table_args__ = {"comment": "a comment"}

    id: Mapped[varchar] = mapped_column(primary_key=True)
    movie_id: Mapped[varchar] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=True)
    text: Mapped[str] = mapped_column(nullable=True)
    date: Mapped[datetime] = mapped_column(nullable=True)


def create_tables(engine):
    _create_tables(engine, Base)
