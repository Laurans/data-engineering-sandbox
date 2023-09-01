from datetime import datetime
from typing import Optional

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from .common import _create_tables
from .types import TYPE_ANNOTATION_MAP, varchar

metadata_obj = MetaData(schema="supplies")


class Base(DeclarativeBase):
    metadata = metadata_obj
    type_annotation_map = TYPE_ANNOTATION_MAP


def create_tables(engine):
    _create_tables(engine, Base)


class Sale(Base):
    __tablename__ = "sales"
    id: Mapped[varchar] = mapped_column(primary_key=True)
    saleDate: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    storeLocation: Mapped[Optional[str]] = mapped_column(nullable=True)
    customer: Mapped[Optional[dict]] = mapped_column(nullable=True)
    couponUsed: Mapped[Optional[bool]] = mapped_column(nullable=True)
    purchaseMethod: Mapped[Optional[str]] = mapped_column(nullable=True)


class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sale_id: Mapped[Optional[varchar]] = mapped_column(nullable=True)
    name: Mapped[Optional[str]] = mapped_column(nullable=True)
    tags: Mapped[Optional[list[str]]] = mapped_column(nullable=True)
    price: Mapped[Optional[float]] = mapped_column(nullable=True)
    quantity: Mapped[Optional[int]] = mapped_column(nullable=True)
