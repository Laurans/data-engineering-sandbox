from typing import Any, TYPE_CHECKING
from data_engineering_sandbox.orm_models import airbnb, mflix, geospatial
from bson.json_util import loads
from sqlalchemy.orm import Session
import sqlalchemy
from json import JSONEncoder
import datetime
import psycopg2
from bson.objectid import ObjectId
from bson.decimal128 import Decimal128
from loguru import logger


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
        session.add(table_definition(**content))
        breakpoint()
        session.commit()
        # TODO: Get the inserted id
    except sqlalchemy.exc.IntegrityError:
        pass
    except sqlalchemy.exc.DataError as e:
        if type(e.orig) == psycopg2.errors.InvalidTextRepresentation:
            pass
    except sqlalchemy.exc.PendingRollbackError as e:
        if "psycopg2.errors.InvalidTextRepresentation" in e.args[0]:
            pass
        else:
            raise e
    except Exception as e:
        breakpoint()
        raise e


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
                    record_transformation(subsubcontent),
                    record_transformation.table_definition,
                )
                for subsubcontent in content.pop(key)
            ]
        elif key in content.keys() and isinstance(content[key], dict):
            _load_record(
                session,
                record_transformation(content.pop(key)),
                record_transformation.table_definition,
            )
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

            for line in raw_content:
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
                    ),
                    "address": NestedDataTransformer(airbnb.Address),
                    "reviews": NestedDataTransformer(airbnb.Review, normalize_id),
                }

        _load_bson_file_in_postgres(
            data_file, table_definition, engine, nested_table_definitions
        )
