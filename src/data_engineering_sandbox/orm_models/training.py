from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import MetaData
from .types import varchar, TYPE_ANNOTATION_MAP
from .common import _create_tables
from datetime import datetime

metadata_obj = MetaData(schema="training")


class Base(DeclarativeBase):
    metadata = metadata_obj
    type_annotation_map = TYPE_ANNOTATION_MAP


def create_tables(engine):
    _create_tables(engine, Base)


class Data(Base):
    id: Mapped[varchar] = mapped_column(primary_key=True)
