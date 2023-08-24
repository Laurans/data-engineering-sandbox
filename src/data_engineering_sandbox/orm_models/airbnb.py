from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import MetaData
from .types import varchar, TYPE_ANNOTATION_MAP
from .common import _create_tables
from datetime import datetime
from typing import Optional

metadata_obj = MetaData(schema="airbnb")


class Base(DeclarativeBase):
    metadata = metadata_obj
    type_annotation_map = TYPE_ANNOTATION_MAP


class Listing(Base):
    __tablename__ = "listings"

    id: Mapped[varchar] = mapped_column(primary_key=True)
    listing_url: Mapped[str]
    name: Mapped[str]
    summary: Mapped[str]
    space: Mapped[str]
    description: Mapped[str]
    neighborhood_overview: Mapped[Optional[str]] = mapped_column(nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(nullable=True)
    transit: Mapped[Optional[str]] = mapped_column(nullable=True)
    access: Mapped[Optional[str]] = mapped_column(nullable=True)
    interaction: Mapped[Optional[str]] = mapped_column(nullable=True)
    house_rules: Mapped[Optional[str]] = mapped_column(nullable=True)
    property_type: Mapped[Optional[str]] = mapped_column(nullable=True)
    room_type: Mapped[Optional[str]] = mapped_column(nullable=True)
    bed_type: Mapped[Optional[str]] = mapped_column(nullable=True)
    minimum_nights: Mapped[Optional[str]] = mapped_column(nullable=True)
    maximum_nights: Mapped[Optional[str]] = mapped_column(nullable=True)
    cancellation_policy: Mapped[Optional[str]] = mapped_column(nullable=True)
    last_scraped: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    calendar_last_scraped: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    first_review: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    last_review: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    accommodates: Mapped[Optional[int]] = mapped_column(nullable=True)
    bedrooms: Mapped[Optional[int]] = mapped_column(nullable=True)
    beds: Mapped[Optional[int]] = mapped_column(nullable=True)
    number_of_reviews: Mapped[Optional[int]] = mapped_column(nullable=True)
    bathrooms: Mapped[Optional[float]] = mapped_column(nullable=True)
    amenities: Mapped[Optional[list[str]]] = mapped_column(nullable=True)
    price: Mapped[Optional[float]] = mapped_column(nullable=True)
    security_deposit: Mapped[Optional[float]] = mapped_column(nullable=True)
    cleaning_fee: Mapped[Optional[float]] = mapped_column(nullable=True)
    extra_people: Mapped[Optional[float]] = mapped_column(nullable=True)
    guests_included: Mapped[Optional[float]] = mapped_column(nullable=True)
    images: Mapped[Optional[dict]] = mapped_column(nullable=True)
    availability: Mapped[Optional[dict]] = mapped_column(nullable=True)
    review_scores: Mapped[Optional[dict]] = mapped_column(nullable=True)
    address_id: Mapped[int]
    host_id: Mapped[int]
    weekly_price: Mapped[Optional[float]] = mapped_column(nullable=True)
    monthly_price: Mapped[Optional[float]] = mapped_column(nullable=True)


class Host(Base):
    __tablename__ = "hosts"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str]
    name: Mapped[str]
    location: Mapped[str]
    about: Mapped[str]
    response_time: Mapped[Optional[str]] = mapped_column(nullable=True)
    thumbnail_url: Mapped[str]
    picture_url: Mapped[str]
    neighbourhood: Mapped[str]
    response_rate: Mapped[Optional[int]] = mapped_column(nullable=True)
    is_superhost: Mapped[bool]
    has_profile_pic: Mapped[bool]
    identity_verified: Mapped[bool]
    listings_count: Mapped[int]
    total_listings_count: Mapped[int]
    verifications: Mapped[list[str]]


class Address(Base):
    __tablename__ = "adresses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    street: Mapped[str]
    suburb: Mapped[str]
    government_area: Mapped[str]
    market: Mapped[str]
    country: Mapped[str]
    country_code: Mapped[str]
    location: Mapped[dict]


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[str] = mapped_column(primary_key=True)
    date: Mapped[datetime]
    listing_id: Mapped[int]
    reviewer_id: Mapped[int]
    reviewer_name: Mapped[str]
    comments: Mapped[str]


def create_tables(engine):
    _create_tables(engine, Base)
