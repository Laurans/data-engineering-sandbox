from typing import TYPE_CHECKING, Optional

from attrs import define, field

if TYPE_CHECKING:
    from typing import Any, Callable

    from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept


@define
class NestedDataTransformer:
    """Hold sqlalchemy table definition, relationship and data transformation for nested records.

    Parameters
    ----------
    table_definition
        Sqlalchemy table definition
    transformation_fn
        data transformation to apply on the extracted sub record
    relationship_key
        column name of the foreign key between the parent and child data points
    data_source_key
        if relationship_key must be added in the child data point,
        we need the origin key from the parent to populate the child with a value.
    add_relationship_in_nested
        boolean to indicate if the foreign key is in the child data point or parent data point.
    """

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
    """Rename the key `_id` to `id`and cast it into string."""
    x["id"] = str(x.pop("_id"))
    return x
