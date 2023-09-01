from sqlalchemy.schema import CreateTable

from data_engineering_sandbox.orm_models import mflix


def test_user():
    print(CreateTable(mflix.User.__table__))
    breakpoint()
