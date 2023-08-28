from typing import TYPE_CHECKING, Optional

from attrs import define, field

if TYPE_CHECKING:
    from typing import Any, Callable

    from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept


@define
class NestedDataTransformer:
    table_definition: "DeclarativeAttributeIntercept"
    transformation_fn: "Callable[[Any], dict]" = field(default=lambda x: x)
    relationship_key: Optional[str] = field(default=None)
    data_source_key: Optional[str] = field(default="")
    add_relationship_in_nested: bool = field(default=False)

    def __call__(self, record, relationship_value=None):
        new_record = self.transformation_fn(record)
        if self.add_relationship_in_nested:
            new_record[self.relationship_key] = relationship_value
        return new_record


def normalize_id(x: dict):
    x["id"] = str(x.pop("_id"))
    return x
