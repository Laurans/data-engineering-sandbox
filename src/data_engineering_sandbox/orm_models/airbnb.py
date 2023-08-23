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
    neighborhood_overview: Mapped[str]
    notes: Mapped[str]
    transit: Mapped[str]
    access: Mapped[str]
    interaction: Mapped[str]
    house_rules: Mapped[str]
    property_type: Mapped[str]
    room_type: Mapped[str]
    bed_type: Mapped[str]
    minimum_nights: Mapped[str]
    maximum_nights: Mapped[str]
    cancellation_policy: Mapped[str]
    last_scraped: Mapped[datetime]
    calendar_last_scraped: Mapped[datetime]
    first_review: Mapped[datetime]
    last_review: Mapped[datetime]
    accommodates: Mapped[int]
    bedrooms: Mapped[int]
    beds: Mapped[int]
    number_of_reviews: Mapped[int]
    bathrooms: Mapped[float]
    amenities: Mapped[list[str]]
    price: Mapped[float]
    security_deposit: Mapped[float]
    cleaning_fee: Mapped[float]
    extra_people: Mapped[float]
    guests_included: Mapped[float]
    images: Mapped[dict]
    availability: Mapped[dict]
    review_scores: Mapped[dict]
    address_id: Mapped[int]
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
