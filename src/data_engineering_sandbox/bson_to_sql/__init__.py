import datetime
from json import JSONEncoder
from typing import TYPE_CHECKING, Any

import psycopg2
import sqlalchemy
import tqdm
from bson.decimal128 import Decimal128
from bson.json_util import loads
from bson.objectid import ObjectId
from loguru import logger
from sqlalchemy.orm import Session

from data_engineering_sandbox.orm_models import (
    airbnb,
    analytics,
    geospatial,
    mflix,
    supplies,
    weatherdata,
)

if TYPE_CHECKING:
    from pathlib import Path
    from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept
    from sqlalchemy.engine.base import Engine

from ._transformations import NestedDataTransformer, normalize_id


class CustomTypeEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        elif isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, Decimal128):
            return float(o.to_decimal())

        return super().default(o)


def _load_record(
    session: Session, content: dict, table_definition: "DeclarativeAttributeIntercept"
):
    try:
        datapoint = table_definition(**content)
        session.add(datapoint)  # TODO: look if we can do a on conflict to nothing
        session.flush()
        session.commit()
    except sqlalchemy.exc.IntegrityError:
        pass
    except sqlalchemy.exc.DataError as e:
        if type(e.orig) == psycopg2.errors.InvalidTextRepresentation:
            pass
    except sqlalchemy.exc.PendingRollbackError as e:
        if (
            "psycopg2.errors.InvalidTextRepresentation" in e.args[0]
            or "psycopg2.errors.UniqueViolation" in e.args[0]
        ):
            pass
        else:
            raise e
    except Exception as e:
        breakpoint()
        raise e
    return datapoint.id


def _load_nested_table(
    session: Session,
    content: dict,
    nested_table_definition: dict[str, NestedDataTransformer] = {},
):
    for key, record_transformation in nested_table_definition.items():
        if key in content.keys() and isinstance(content[key], list):
            [
                _load_record(
                    session,
                    record_transformation(
                        subsubcontent,
                        content.get(record_transformation.data_source_key),
                    ),
                    record_transformation.table_definition,
                )
                for subsubcontent in content.pop(key)
            ]
        elif key in content.keys() and isinstance(content[key], dict):
            datapoint_id = _load_record(
                session,
                record_transformation(
                    content.pop(key),
                    content.get(record_transformation.data_source_key),
                ),
                record_transformation.table_definition,
            )

            if (
                record_transformation.relationship_key
                and not record_transformation.add_relationship_in_nested
            ):
                content[record_transformation.relationship_key] = datapoint_id
    return content


def _load_bson_file_in_postgres(
    data_file: "Path",
    table_definition: "DeclarativeAttributeIntercept",
    engine: "Engine",
    nested_table_definition: dict[str, NestedDataTransformer] = {},
):
    with Session(engine) as session:
        session.rollback()
        with open(data_file, "r") as fp:
            logger.info(f"Loading data from {data_file} ...")
            raw_content = fp.readlines()

            for line in tqdm.tqdm(raw_content):
                content = loads(line)
                content = normalize_id(content)

                content = loads(CustomTypeEncoder().encode(content))

                content = _load_nested_table(session, content, nested_table_definition)
                _load_record(session, content, table_definition)


def load_mflix_files(directory: "Path", engine: "Engine"):
    mflix.create_tables(engine)
    for data_file in directory.iterdir():
        match data_file.stem:
            case "sessions":
                table_definition = mflix.Session
            case "comments":
                table_definition = mflix.Comment
            case "movies":
                table_definition = mflix.Movie
            case "theaters":
                table_definition = mflix.Theater
            case "users":
                table_definition = mflix.User

        _load_bson_file_in_postgres(data_file, table_definition, engine)


def load_geospatial_files(directory: "Path", engine: "Engine"):
    geospatial.create_tables(engine)
    for data_file in directory.iterdir():
        match data_file.stem:
            case "shipwrecks":
                table_definition = geospatial.Shipwreck

        _load_bson_file_in_postgres(data_file, table_definition, engine)


def load_airbnb_files(directory: "Path", engine: "Engine"):
    airbnb.create_tables(engine)
    for data_file in directory.iterdir():
        match data_file.stem:
            case "listingsAndReviews":
                table_definition = airbnb.Listing
                nested_table_definitions = {
                    "host": NestedDataTransformer(
                        airbnb.Host,
                        lambda x: {k.replace("host_", ""): v for k, v in x.items()},
                        relationship_key="host_id",
                    ),
                    "address": NestedDataTransformer(
                        airbnb.Address, relationship_key="address_id"
                    ),
                    "reviews": NestedDataTransformer(airbnb.Review, normalize_id),
                }

        _load_bson_file_in_postgres(
            data_file, table_definition, engine, nested_table_definitions
        )


def load_analytics_files(directory: "Path", engine: "Engine"):
    analytics.create_tables(engine)
    nested_table_definitions = {}
    for data_file in directory.iterdir():
        match data_file.stem:
            case "accounts":
                table_definition = analytics.Account
            case "customers":
                table_definition = analytics.Customer
                nested_table_definitions = {
                    "accounts": NestedDataTransformer(
                        analytics.CustomersXAccount,
                        lambda x: {"account_id": x},
                        relationship_key="customer_id",
                        add_relationship_in_nested=True,
                        data_source_key="id",
                    )
                }
            case "transactions":
                table_definition = analytics.TransactionMetadata
                nested_table_definitions = {
                    "transactions": NestedDataTransformer(
                        analytics.Transaction,
                        relationship_key="account_id",
                        add_relationship_in_nested=True,
                        data_source_key="account_id",
                    )
                }
        _load_bson_file_in_postgres(
            data_file, table_definition, engine, nested_table_definitions
        )


def load_supplies_files(directory: "Path", engine: "Engine"):
    supplies.create_tables(engine)
    nested_table_definitions = {}
    for data_file in directory.iterdir():
        match data_file.stem:
            case "sales":
                table_definition = supplies.Sale
                nested_table_definitions = {
                    "items": NestedDataTransformer(
                        supplies.Item,
                        relationship_key="sale_id",
                        add_relationship_in_nested=True,
                        data_source_key="id",
                    )
                }

        _load_bson_file_in_postgres(
            data_file, table_definition, engine, nested_table_definitions
        )


def load_weatherdata_files(directory: "Path", engine: "Engine"):
    weatherdata.create_tables(engine)
    for data_file in directory.iterdir():
        match data_file.stem:
            case "data":
                table_definition = weatherdata.Data

        _load_bson_file_in_postgres(data_file, table_definition, engine)
