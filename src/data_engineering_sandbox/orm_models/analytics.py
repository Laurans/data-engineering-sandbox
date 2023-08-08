from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import MetaData
from .types import varchar, TYPE_ANNOTATION_MAP
from .common import _create_tables
from datetime import datetime

metadata_obj = MetaData(schema="analytics")


class Base(DeclarativeBase):
    metadata = metadata_obj
    type_annotation_map = TYPE_ANNOTATION_MAP


def create_tables(engine):
    _create_tables(engine, Base)


class Accounts(Base):
    id: Mapped[varchar] = mapped_column(primary_key=True)
    account_id: Mapped[int]
    limit: Mapped[int]
    products: Mapped[list[str]]


class Customers(Base):
    id: Mapped[varchar] = mapped_column(primary_key=True)
    username: Mapped[str]
    name: Mapped[str]
    address: Mapped[str]
    birthdate: Mapped[datetime]
    email: Mapped[str]
    active: Mapped[bool]
    tier_and_details: Mapped[dict]


class CustomersXAccounts(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[varchar]
    account_id: Mapped[varchar]


class TransactionsMetadata(Base):
    id: Mapped[varchar] = mapped_column(primary_key=True)
    account_id: Mapped[int]
    transaction_count: Mapped[int]
    bucket_start_date: Mapped[datetime]
    bucket_end_date: Mapped[datetime]


class Transactions(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    account_id = Mapped[int]
    date: Mapped[datetime]
    amount: Mapped[int]
    transaction_code: Mapped[str]
    symbol: Mapped[str]
    price: Mapped[float]
    total: Mapped[float]
