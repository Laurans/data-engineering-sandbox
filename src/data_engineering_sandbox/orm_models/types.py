from typing_extensions import Annotated
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, TEXT, TIMESTAMP
from sqlalchemy import Float, String
from datetime import datetime

varchar = Annotated[str, 24]


TYPE_ANNOTATION_MAP = {
    varchar: String(24),
    dict: JSONB,
    str: TEXT,
    datetime: TIMESTAMP,
    list[str]: ARRAY(TEXT, dimensions=1),
    list[float]: ARRAY(Float, dimensions=1),
}
