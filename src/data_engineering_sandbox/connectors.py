import os

from sqlalchemy import TextClause, create_engine
from sqlalchemy.engine.url import URL


def get_database_values(
    env_var_suffix,
    default_host,
    default_port,
    default_username,
    default_password,
    default_db,
):
    database_host = os.getenv(f"{env_var_suffix}_HOST", default_host)
    database_port = os.getenv(f"{env_var_suffix}_PORT", default_port)
    database_username = os.getenv(f"{env_var_suffix}_USER", default_username)
    database_password = os.getenv(f"{env_var_suffix}_PASSWORD", default_password)
    database_name = os.getenv(f"{env_var_suffix}_DB", default_db)

    return (
        database_host,
        database_port,
        database_username,
        database_password,
        database_name,
    )


def get_values_postgres_env(env_var_suffix="POSTGRES"):
    return get_database_values(
        env_var_suffix, "localhost", "5432", "postgres", "postgres", "mydb"
    )


def get_values_mongo_env(env_var_suffix="MONGO"):
    return get_database_values(
        env_var_suffix, "localhost", "27017", "mongo", "mongo", "mydb"
    )


def get_postgres_url(env_var_suffix="POSTGRES") -> URL:
    """Return URL to connect to postgres

    Returns
    -------
    URL
        sqlalchemy url object
    """
    (
        database_host,
        database_port,
        database_username,
        database_password,
        database_name,
    ) = get_values_postgres_env(env_var_suffix)

    db_url = URL.create(
        drivername="postgresql",
        username=database_username,
        password=database_password,
        host=database_host,
        port=database_port,
        database=database_name,
    )
    return db_url


class PostgresConnector:
    def __init__(self) -> None:
        self.engine = create_engine(get_postgres_url(), echo=True)

    def execute_query(self, query: TextClause):
        with self.engine.execution_options(
            isolation_level="AUTOCOMMIT"
        ).connect() as connection:
            result = connection.execute(query)
            return result
