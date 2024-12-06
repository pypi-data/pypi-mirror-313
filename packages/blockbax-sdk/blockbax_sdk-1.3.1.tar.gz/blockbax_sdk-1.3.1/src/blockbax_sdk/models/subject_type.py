from __future__ import annotations
from typing import List, Optional, Union
from uuid import UUID
from pydantic import field_validator
from .base import BlockbaxModel
from .type_hints import (
    BlockbaxDatetime,
    PropertyTypeId,
    SubjectTypeId,
    MetricId,
)


class SubjectTypePrimaryLocation(BlockbaxModel):
    # Currently Literal["PROPERTY_TYPE", "METRIC"];
    type: str
    id: Union[PropertyTypeId, MetricId]

    @field_validator("id", mode="before")
    def convert_id_to_uuid(cls, value):  # pylint: disable=C0116.E0213
        if value is not None and isinstance(value, str):
            return UUID(value)
        return value


class SubjectTypePropertyType(BlockbaxModel):
    id: PropertyTypeId
    required: bool
    visible: bool = True

    @field_validator("id", mode="before")
    def convert_id_to_uuid(cls, value):  # pylint: disable=C0116.E0213
        if value is not None and isinstance(value, str):
            return UUID(value)
        return value


class SubjectType(BlockbaxModel):
    id: SubjectTypeId
    name: str
    created_date: BlockbaxDatetime
    updated_date: Optional[BlockbaxDatetime] = None
    parent_subject_type_ids: Optional[List[SubjectTypeId]] = None
    primary_location: Optional[SubjectTypePrimaryLocation] = None
    property_types: Optional[List[SubjectTypePropertyType]] = None

    def add_property_types(self, property_types: List[SubjectTypePropertyType]) -> None:
        """Adds new property types to its property_types attribute."""
        if not self.property_types:
            self.property_types = []
        self.property_types.extend(property_types)

    def remove_property_types(self, property_type_ids: List[Union[UUID, str]]) -> None:
        """Removes property types from its property_types attribute by Id."""
        property_type_ids = [
            UUID(property_type_id)
            if isinstance(property_type_id, str)
            else property_type_id
            for property_type_id in property_type_ids
        ]
        for property_type in self.property_types:
            if property_type.id in property_type_ids:
                self.property_types.remove(property_type)

    def contains_property_type(self, property_type_id: Union[UUID, str]) -> bool:
        if isinstance(property_type_id, str):
            property_type_id = UUID(property_type_id)
        return any(
            property_type_id == property_type.id
            for property_type in self.property_types
        )
