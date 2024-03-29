from typing import Optional

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from .common import _create_tables
from .types import TYPE_ANNOTATION_MAP, varchar

metadata_obj = MetaData(schema="geospatial")


class Base(DeclarativeBase):
    metadata = metadata_obj
    type_annotation_map = TYPE_ANNOTATION_MAP


class Shipwreck(Base):
    __tablename__ = "shipwrecks"

    id: Mapped[varchar] = mapped_column(primary_key=True)
    recrd: Mapped[Optional[str]] = mapped_column(nullable=True)
    vesslterms: Mapped[Optional[str]] = mapped_column(nullable=True)
    feature_type: Mapped[Optional[str]] = mapped_column(nullable=True)
    chart: Mapped[Optional[str]] = mapped_column(nullable=True)
    latdec: Mapped[float]
    londec: Mapped[float]
    gp_quality: Mapped[Optional[str]] = mapped_column(nullable=True)
    depth: Mapped[Optional[str]] = mapped_column(nullable=True)
    sounding_type: Mapped[Optional[str]] = mapped_column(nullable=True)
    history: Mapped[Optional[str]] = mapped_column(nullable=True)
    quasou: Mapped[Optional[str]] = mapped_column(nullable=True)
    watlev: Mapped[Optional[str]] = mapped_column(nullable=True)
    coordinates: Mapped[list[float]]


def create_tables(engine):
    _create_tables(engine, Base)
