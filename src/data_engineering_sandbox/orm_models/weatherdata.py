from datetime import datetime
from typing import Optional

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from .common import _create_tables
from .types import TYPE_ANNOTATION_MAP, varchar

metadata_obj = MetaData(schema="weatherdata")


class Base(DeclarativeBase):
    metadata = metadata_obj
    type_annotation_map = TYPE_ANNOTATION_MAP


def create_tables(engine):
    _create_tables(engine, Base)


class Data(Base):
    __tablename__ = "data"
    id: Mapped[varchar] = mapped_column(primary_key=True)
    st: Mapped[Optional[str]] = mapped_column(nullable=True)
    ts: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    position: Mapped[Optional[dict]] = mapped_column(nullable=True)
    elevation: Mapped[Optional[int]] = mapped_column(nullable=True)
    callLetters: Mapped[Optional[str]] = mapped_column(nullable=True)
    qualityControlProcess: Mapped[Optional[str]] = mapped_column(nullable=True)
    dataSource: Mapped[Optional[str]] = mapped_column(nullable=True)
    type: Mapped[Optional[str]] = mapped_column(nullable=True)
    airTemperature: Mapped[Optional[dict]] = mapped_column(nullable=True)
    dewPoint: Mapped[Optional[dict]] = mapped_column(nullable=True)
    pressure: Mapped[Optional[dict]] = mapped_column(nullable=True)
    wind: Mapped[Optional[dict]] = mapped_column(nullable=True)
    visibility: Mapped[Optional[dict]] = mapped_column(nullable=True)
    skyCondition: Mapped[Optional[dict]] = mapped_column(nullable=True)
    sections: Mapped[Optional[list[str]]] = mapped_column(nullable=True)
    precipitationEstimatedObservation: Mapped[Optional[dict]] = mapped_column(
        nullable=True
    )
    atmosphericPressureChange: Mapped[Optional[dict]] = mapped_column(nullable=True)
    seaSurfaceTemperature: Mapped[Optional[dict]] = mapped_column(nullable=True)
    waveMeasurement: Mapped[Optional[dict]] = mapped_column(nullable=True)
    pastWeatherObservationManual: Mapped[Optional[dict]] = mapped_column(nullable=True)
    skyConditionObservation: Mapped[Optional[dict]] = mapped_column(nullable=True)
    presentWeatherObservationManual: Mapped[Optional[dict]] = mapped_column(
        nullable=True
    )
    atmosphericPressureObservation: Mapped[Optional[dict]] = mapped_column(
        nullable=True
    )
    skyCoverLayer: Mapped[Optional[dict]] = mapped_column(nullable=True)
    liquidPrecipitation: Mapped[Optional[dict]] = mapped_column(nullable=True)
    extremeAirTemperature: Mapped[Optional[dict]] = mapped_column(nullable=True)
