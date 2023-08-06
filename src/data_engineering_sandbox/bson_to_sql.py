from typing import Any
from data_engineering_sandbox.orm_models import mflix
from bson.json_util import loads
from sqlalchemy.orm import Session
import sqlalchemy
from json import JSONEncoder
import datetime
import psycopg2
from bson.objectid import ObjectId


class CustomTypeEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)


def load_mflix_files(directory, engine):
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

        columns_keys = sorted(table_definition.__table__.columns.keys())
        with Session(engine) as session:
            session.rollback()
            with open(data_file, "r") as fp:
                raw_content = fp.readlines()

                for line in raw_content:
                    content = loads(line)
                    content["id"] = str(content["_id"])
                    content.pop("_id")
                    content = loads(CustomTypeEncoder().encode(content))
                    keys = sorted(list(content.keys()))
                    # if columns_keys != keys:
                    #    breakpoint()
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
