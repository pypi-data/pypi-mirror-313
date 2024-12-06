from __future__ import annotations
from typing import List, Optional, Any

import logging

from .base import BlockbaxModel

from .type_hints import (
    PropertyTypeId,
    PropertyTypeExternalId,
    BlockbaxDatetime,
)
from .property_type_value import PropertyTypeValue, property_type_value_adapter

logger = logging.getLogger(__name__)


class PropertyType(BlockbaxModel):
    id: PropertyTypeId
    name: str
    external_id: PropertyTypeExternalId
    created_date: BlockbaxDatetime
    data_type: str  # relaxing limitations for cases with new unknown data types
    predefined_values: bool = False
    values: Optional[List[PropertyTypeValue]] = None
    updated_date: Optional[BlockbaxDatetime] = None

    def contains_value(self, value: Any) -> bool:
        """ "Returns `True` if Property type has a Property value with given value"""
        return (
            any(
                property_type_value.get_value() == value
                for property_type_value in self.values
            )
            if self.values
            else False
        )

    def ensure_values_initialized(self):
        """In case PropertyType object is created by the user without values; The values field default is not set to
        match the default arg of the create_property_type method of the Api interface
        """
        if not self.values:
            self.values = []

    def add_value(self, value: Any, caption: Optional[str] = None) -> None:
        self.ensure_values_initialized()
        if not self.predefined_values:
            raise ValueError(
                "You cannot add values to a property type with predefined values set to False"
            )
        if value in self.values:
            logger.warning(
                "Value already in the list of property type values. Skipping."
            )
            return
        self.values.append(
            property_type_value_adapter.validate_python(
                {
                    self.data_type.lower(): value,
                    "caption": caption,
                }
            )
        )

    def change_value(self, old_value: Any, new_value: Any) -> None:
        """Changes the value of an already existing property value"""
        self.ensure_values_initialized()
        if self.predefined_values:
            for property_value in self.values:
                if property_value == old_value:
                    property_value._set_value(new_value=new_value)
        else:
            predefined_values_not_permitted_error = "You cannot change values of a property type with predefined values set to False"
            raise ValueError(predefined_values_not_permitted_error)

    def change_caption(self, value: Any, caption: str):
        self.ensure_values_initialized()
        if self.predefined_values:
            for property_value in self.values:
                if property_value == value:
                    property_value.caption = caption
        else:
            predefined_values_not_permitted_error = "You cannot change captions of a property type with predefined values set to False"
            raise ValueError(predefined_values_not_permitted_error)

    def remove_value(self, value: Any) -> None:
        self.ensure_values_initialized()
        if self.predefined_values:
            for property_value in self.values:
                if property_value.get_value() == value:
                    self.values.remove(property_value)
                    return
        else:
            predefined_values_not_permitted_error = "You cannot remove values from a property type with predefined values set to False"
            raise ValueError(predefined_values_not_permitted_error)
