import os

from sqlalchemy import create_engine, TextClause
from sqlalchemy.engine.url import URL


def get_postgres_url(env_var_suffix="POSTGRES") -> URL:
    """Return URL to connect to postgres

    Returns
    -------
    URL
        sqlalchemy url object
    """
    database_host = os.getenv(f"{env_var_suffix}_HOST", "localhost")
    database_port = os.getenv(f"{env_var_suffix}_PORT", "5432")
    database_username = os.getenv(f"{env_var_suffix}_USER", "postgres")
    database_password = os.getenv(f"{env_var_suffix}_PASSWORD", "postgres")
    database_name = os.getenv(f"{env_var_suffix}_DB", "mydb")

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
