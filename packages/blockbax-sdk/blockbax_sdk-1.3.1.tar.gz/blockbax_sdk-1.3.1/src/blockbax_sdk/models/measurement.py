from datetime import datetime
from typing import List, Union, Optional

from pydantic import TypeAdapter, field_validator

import logging

from .base import BlockbaxModel
from ..util import conversions
from .data_types import (
    NumberTypeMixin,
    TextTypeMixin,
    LocationTypeMixin,
    UnknownTypeMixin,
)

logger = logging.getLogger(__name__)


class MeasurementBase(BlockbaxModel):
    date: Optional[Union[int, float, datetime, str]] = None

    @field_validator("date")
    def convert_to_epoch_ms(cls, date):
        return conversions.convert_any_date_to_unix_millis(date=date)


class NumberMeasurement(NumberTypeMixin, MeasurementBase):
    ...


class LocationMeasurement(LocationTypeMixin, MeasurementBase):
    ...


class TextMeasurement(TextTypeMixin, MeasurementBase):
    ...


class UnknownMeasurement(UnknownTypeMixin, MeasurementBase):
    ...


# Unknown type should be put last to catch any new data types
# see the docs for more info  https://docs.pydantic.dev/latest/concepts/unions/
Measurement = Union[
    NumberMeasurement,
    LocationMeasurement,
    TextMeasurement,
    UnknownMeasurement,
]

measurement_adapter: TypeAdapter[Measurement] = TypeAdapter(Measurement)
measurements_adapter: TypeAdapter[List[Measurement]] = TypeAdapter(List[Measurement])
