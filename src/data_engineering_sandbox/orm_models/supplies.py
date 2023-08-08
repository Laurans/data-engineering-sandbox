from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import MetaData
from .types import varchar, TYPE_ANNOTATION_MAP
from .common import _create_tables
from datetime import datetime

metadata_obj = MetaData(schema="supplies")


class Base(DeclarativeBase):
    metadata = metadata_obj
    type_annotation_map = TYPE_ANNOTATION_MAP


def create_tables(engine):
    _create_tables(engine, Base)


class Sales(Base):
    id: Mapped[varchar] = mapped_column(primary_key=True)
    saleDate: Mapped[datetime]
    storeLocation: Mapped[str]
    customer: Mapped[dict]
    couponUsed: Mapped[bool]
    purchaseMethod: Mapped[str]


class Items(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    saleId: Mapped[varchar]
    name: Mapped[str]
    tags: Mapped[list[str]]
    price: Mapped[float]
    quantity: Mapped[int]
