from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import MetaData
from .types import varchar, TYPE_ANNOTATION_MAP
from typing import Optional
from .common import _create_tables

metadata_obj = MetaData(schema="geospatial")


class Base(DeclarativeBase):
    metadata = metadata_obj
    type_annotation_map = TYPE_ANNOTATION_MAP


class Shipwrecks(Base):
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
    coordinate: Mapped[list[float]]


def create_tables(engine):
    _create_tables(engine, Base)
