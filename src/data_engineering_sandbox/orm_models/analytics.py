from datetime import datetime
from typing import Optional

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from .common import _create_tables
from .types import TYPE_ANNOTATION_MAP, varchar

metadata_obj = MetaData(schema="analytics")


class Base(DeclarativeBase):
    metadata = metadata_obj
    type_annotation_map = TYPE_ANNOTATION_MAP


def create_tables(engine):
    _create_tables(engine, Base)


class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[varchar] = mapped_column(primary_key=True)
    account_id: Mapped[Optional[int]] = mapped_column(nullable=True)
    limit: Mapped[Optional[int]] = mapped_column(nullable=True)
    products: Mapped[list[str]] = mapped_column(nullable=True)


class Customer(Base):
    __tablename__ = "customer"
    id: Mapped[varchar] = mapped_column(primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(nullable=True)
    name: Mapped[Optional[str]] = mapped_column(nullable=True)
    address: Mapped[Optional[str]] = mapped_column(nullable=True)
    birthdate: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    email: Mapped[Optional[str]] = mapped_column(nullable=True)
    active: Mapped[Optional[bool]] = mapped_column(nullable=True)
    tier_and_details: Mapped[Optional[dict]] = mapped_column(nullable=True)


class CustomersXAccount(Base):
    __tablename__ = "customersXaccount"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[Optional[varchar]] = mapped_column(nullable=True)
    account_id: Mapped[Optional[varchar]] = mapped_column(nullable=True)


class TransactionMetadata(Base):
    __tablename__ = "transactionsMetadata"
    id: Mapped[varchar] = mapped_column(primary_key=True)
    account_id: Mapped[Optional[int]] = mapped_column(nullable=True)
    transaction_count: Mapped[Optional[int]] = mapped_column(nullable=True)
    bucket_start_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    bucket_end_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)


class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    account_id: Mapped[Optional[int]] = mapped_column(nullable=True)
    date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    amount: Mapped[Optional[int]] = mapped_column(nullable=True)
    transaction_code: Mapped[Optional[str]] = mapped_column(nullable=True)
    symbol: Mapped[Optional[str]] = mapped_column(nullable=True)
    price: Mapped[Optional[float]] = mapped_column(nullable=True)
    total: Mapped[Optional[float]] = mapped_column(nullable=True)
