from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import MetaData
from .types import varchar, TYPE_ANNOTATION_MAP
from .common import _create_tables
from datetime import datetime

metadata_obj = MetaData(schema="weatherdata")


class Base(DeclarativeBase):
    metadata = metadata_obj
    type_annotation_map = TYPE_ANNOTATION_MAP


def create_tables(engine):
    _create_tables(engine, Base)


class Data(Base):
    id: Mapped[varchar] = mapped_column(primary_key=True)
    st: Mapped[str]
    ts: Mapped[datetime]
    position: Mapped[dict]
    elevation: Mapped[int]
    callLetters: Mapped[str]
    qualityControlProcess: Mapped[str]
    dataSource: Mapped[str]
    type: Mapped[str]
    airTemperature: Mapped[dict]
    dewPoint: Mapped[dict]
    pressure: Mapped[dict]
    wind: Mapped[dict]
    visibility: Mapped[dict]
    skyCondition: Mapped[dict]
    sections: Mapped[list[str]]
    precipitationEstimatedObservation: Mapped[dict]
