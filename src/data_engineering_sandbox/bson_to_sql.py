from typing import Any, TYPE_CHECKING
from data_engineering_sandbox.orm_models import mflix, geospatial
from bson.json_util import loads
from sqlalchemy.orm import Session
import sqlalchemy
from json import JSONEncoder
import datetime
import psycopg2
from bson.objectid import ObjectId
from loguru import logger


if TYPE_CHECKING:
    from pathlib import Path
    from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept
    from sqlalchemy.engine.base import Engine


class CustomTypeEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)


def _load_bson_file_in_postgres(
    data_file: Path, table_definition: DeclarativeAttributeIntercept, engine: Engine
):
    with Session(engine) as session:
        session.rollback()
        with open(data_file, "r") as fp:
            logger.info(f"Loading data from {data_file} ...")
            raw_content = fp.readlines()

            for line in raw_content:
                content = loads(line)
                content["id"] = str(content["_id"])
                content.pop("_id")
                content = loads(CustomTypeEncoder().encode(content))
                try:
                    session.add(table_definition(**content))
                    session.commit()
                except sqlalchemy.exc.IntegrityError:
                    continue
                except sqlalchemy.exc.DataError as e:
                    if type(e.orig) == psycopg2.errors.InvalidTextRepresentation:
                        continue
                except sqlalchemy.exc.PendingRollbackError as e:
                    if "psycopg2.errors.InvalidTextRepresentation" in e.args[0]:
                        continue
                    else:
                        raise e
                except Exception as e:
                    breakpoint()
                    raise e


def load_mflix_files(directory: Path, engine: Engine):
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


def load_geospatial_files(directory: Path, engine: Engine):
    geospatial.create_tables(engine)
    for data_file in directory.iterdir():
        match data_file.stem:
            case "shipwrecks":
                table_definition = geospatial.Shipwrecks

        _load_bson_file_in_postgres(data_file, table_definition, engine)
