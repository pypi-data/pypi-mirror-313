import enum
from typing import List, Type, TypeVar

from truefoundry.ml.autogen.client import (  # type: ignore[attr-defined]
    ModelSchemaDto,
)
from truefoundry.ml.exceptions import MlFoundryException
from truefoundry.pydantic_v1 import BaseModel

T = TypeVar("T")


class BaseEnum(enum.Enum):
    @classmethod
    def values(cls: Type[T]) -> List[T]:
        return [member.value for member in cls]

    @classmethod
    def _missing_(cls: Type[T], value: object):
        raise MlFoundryException(
            f"Unknown value for type {cls.__name__}: {value}", status_code=400
        )


@enum.unique
class CustomMetricValueType(str, BaseEnum):
    FLOAT = "float"


@enum.unique
class CustomMetricType(str, BaseEnum):
    METRIC = "metric"
    PROJECTION = "projection"


class CustomMetric(BaseModel):
    class Config:
        validate_assignment = True
        use_enum_values = True
        extra = "allow"

    name: str
    value_type: CustomMetricValueType
    type: CustomMetricType


class ModelSchema(ModelSchemaDto):
    pass
