from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.schema import CreateSchema


def _create_tables(engine, base: DeclarativeBase):
    _drop_tables(engine, base)
    with engine.connect() as connection:
        connection.execute(CreateSchema(base.metadata.schema, if_not_exists=True))
        connection.commit()
    base.metadata.create_all(engine)


def _drop_tables(engine, base: DeclarativeBase):
    base.metadata.drop_all(engine)
