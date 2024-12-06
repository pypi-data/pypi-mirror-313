from __future__ import annotations
from typing_extensions import TypeAlias
from typing import Optional, Union

import logging
from uuid import UUID


from .base import BlockbaxModel

from .data_types import (
    NumberTypeMixin,
    TextTypeMixin,
    LocationTypeMixin,
    MapLayerTypeMixin,
    ImageTypeMixin,
    AreaTypeMixin,
    UnknownTypeMixin,
)

from pydantic import TypeAdapter, field_validator

logger = logging.getLogger(__name__)


class SubjectPropertyBase(BlockbaxModel):
    type_id: Union[UUID, str]
    value_id: Optional[Union[UUID, str]] = None
    caption: Optional[str] = None
    inherit: Optional[bool] = None

    @field_validator("type_id", "value_id", mode="before")
    def convert_id_to_uuid(cls, value):  # pylint: disable=C0116.E0213
        if value is not None and isinstance(value, str):
            return UUID(value)
        return value


class PreDefinedSubjectProperty(SubjectPropertyBase):
    value_id: Optional[
        Union[UUID, str]
    ]  # Should be required in pre-defined subject properties

    @field_validator("value_id", mode="before")
    def ensure_value_id_exists(cls, value):  # pylint: disable=C0116.E0213
        if value is None:
            raise ValueError("Value id cannot be empty in a PreDefinedSubjectProperty.")
        return value


class NumberSubjectProperty(NumberTypeMixin, SubjectPropertyBase): ...


class TextSubjectProperty(TextTypeMixin, SubjectPropertyBase): ...


class LocationSubjectProperty(LocationTypeMixin, SubjectPropertyBase): ...


class MapLayerSubjectProperty(MapLayerTypeMixin, SubjectPropertyBase): ...


class ImageSubjectProperty(ImageTypeMixin, SubjectPropertyBase): ...


class AreaSubjectProperty(AreaTypeMixin, SubjectPropertyBase): ...


class UnknownDataTypeSubjectProperty(UnknownTypeMixin, SubjectPropertyBase): ...


SubjectProperty: TypeAlias = Union[
    NumberSubjectProperty,
    TextSubjectProperty,
    LocationSubjectProperty,
    MapLayerSubjectProperty,
    ImageSubjectProperty,
    PreDefinedSubjectProperty,
    UnknownDataTypeSubjectProperty,  # put last to catch any new data types
]

subject_property_adapter: TypeAdapter[SubjectProperty] = TypeAdapter(SubjectProperty)
