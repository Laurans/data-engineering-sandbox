from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, TEXT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing_extensions import Annotated

varchar = Annotated[str, 24]
ostr = Optional[str]


class Base(DeclarativeBase):
    type_annotation_map = {
        varchar: String(24),
        dict: JSONB,
        str: TEXT,
        datetime: DateTime,
        list[str]: ARRAY(TEXT, dimensions=1),
        list[float]: ARRAY(Float, dimensions=1),
    }


class User(Base):
    __tablename__ = "users"

    id: Mapped[varchar] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]


class Theater(Base):
    __tablename__ = "theaters"

    id: Mapped[varchar] = mapped_column(primary_key=True)
    theaterId: Mapped[int]
    location: Mapped[dict]


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[varchar] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    jwt: Mapped[str] = mapped_column(comment="JSON Web Token")


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[varchar] = mapped_column(primary_key=True)
    title: Mapped[str]
    year: Mapped[int]
    runtime: Mapped[int]
    released: Mapped[datetime]
    poster: Mapped[str]
    plot: Mapped[str]
    fullplot: Mapped[str]
    lastupdated: Mapped[datetime]
    type: Mapped[str]
    directors: Mapped[list[str]]
    imdb: Mapped[dict]
    cast: Mapped[list[str]]
    countries: Mapped[list[str]]
    genres: Mapped[list[str]]
    tomatoes: Mapped[dict]
    num_mflix_comments: Mapped[int]
    rated: Mapped[str]
    awards: Mapped[dict]


class Embedded_Movie(Base):
    __tablename__ = "embedded_movies"

    id: Mapped[varchar] = mapped_column(primary_key=True)
    title: Mapped[str]
    year: Mapped[int]
    runtime: Mapped[int]
    released: Mapped[datetime]
    poster: Mapped[str]
    plot: Mapped[str]
    fullplot: Mapped[str]
    lastupdated: Mapped[datetime]
    type: Mapped[str]
    directors: Mapped[list[str]]
    imdb: Mapped[dict]
    cast: Mapped[list[str]]
    countries: Mapped[list[str]]
    genres: Mapped[list[str]]
    tomatoes: Mapped[dict]
    num_mflix_comments: Mapped[int]
    rated: Mapped[str]
    awards: Mapped[dict]
    plot_embedding: Mapped[list[float]]


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[varchar] = mapped_column(primary_key=True)
    movie_id: Mapped[varchar] = mapped_column(ForeignKey("movies.id"))
    name: Mapped[str]
    email: Mapped[str]
    text_: Mapped[str]
    date: Mapped[datetime]
