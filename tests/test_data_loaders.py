import pytest
from sqlalchemy import create_engine, inspect, text

from data_engineering_sandbox.connectors import get_postgres_url
from data_engineering_sandbox.data_loaders import FromCSVtoPostgres
from tests import data_folder


@pytest.fixture(scope="module")
def get_engine():
    yield create_engine(get_postgres_url(), echo=True, isolation_level="AUTOCOMMIT")


@pytest.fixture()
def clear_database(get_engine):
    yield get_engine
    engine = get_engine

    with engine.connect() as connection:
        inspector = inspect(engine)
        schema = inspector.get_table_names()
        for table in schema:
            # Delete all rows from each table
            connection.execute(text(f"DROP TABLE {table} CASCADE"))


@pytest.fixture()
def clear_database_only_rows(get_engine):
    yield get_engine
    engine = get_engine

    with engine.connect() as connection:
        inspector = inspect(engine)
        schema = inspector.get_table_names()
        for table in schema:
            # Delete all rows from each table
            connection.execute(text(f"TRUNCATE TABLE {table} CASCADE"))


def test_table_is_populated_with_data_replace(clear_database):
    data_path = data_folder / "goodreads_data.csv"
    table_name = "books"
    loader = FromCSVtoPostgres(csv_file=data_path, table_name=table_name)
    total_inserted = loader.populate_table_from_csv()

    assert total_inserted == 10000
