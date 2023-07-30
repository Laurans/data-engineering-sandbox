from data_engineering_sandbox.orm_models import mflix
from sqlalchemy.schema import CreateTable


def test_user():
    print(CreateTable(mflix.User.__table__))
    breakpoint()
