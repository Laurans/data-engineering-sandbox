from attrs import define, field
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept
    from typing import Callable


@define
class NestedDataTransformer:
    table_definition: "DeclarativeAttributeIntercept"
    transformation_fn: "Callable" = field(default=lambda x: x)
    relationship_key: Optional[str] = field(default=None)

    def __call__(self, record):
        return self.transformation_fn(record)


def normalize_id(x: dict):
    x["id"] = str(x.pop("_id"))
    return x
