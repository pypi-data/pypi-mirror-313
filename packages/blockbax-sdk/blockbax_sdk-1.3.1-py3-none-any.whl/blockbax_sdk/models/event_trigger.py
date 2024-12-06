from decimal import Decimal
from typing import Any, Dict, List, Optional, Literal, Union
from uuid import UUID

from pydantic import ConfigDict, field_validator, model_validator

from ..models.base import BlockbaxModel
from .type_hints import (
    EventTriggerId,
    MetricId,
    SubjectTypeId,
    PropertyTypeId,
    BlockbaxDatetime,
)

from .data_types import Location, Area


class Period(BlockbaxModel):
    unit: Literal["MILLISECOND", "SECOND", "MINUTE", "HOUR", "DAY", "WEEK"]
    amount: int

    @field_validator("amount", mode="before")
    def validate_amount(cls, value):  # pylint: disable=C0116.E0213
        if value < 1:
            raise ValueError(
                "Period amount. Total should be a max of 1 week in whichever period unit."
            )
        return value


class Aggregation(BlockbaxModel):
    function: Literal["MIN", "MAX", "SUM", "COUNT", "AVG"]
    period: Period


class Offset(BlockbaxModel):
    type: Literal["PREVIOUS_VALUE", "PERIOD"]
    period: Optional[Period] = None

    @model_validator(mode="after")
    def validate_offset(cls, values):  # pylint: disable=C0116.E0213
        if values.type == "PERIOD" and values.period is None:
            raise ValueError("Period is required when type is PERIOD.")
        return values


class Operand(BlockbaxModel):
    type: Literal[
        "METRIC", "PROPERTY_TYPE", "STATIC_VALUE", "VALUE_CHANGE", "CALCULATION"
    ]
    id: Optional[Union[MetricId, PropertyTypeId, str]] = None
    number: Optional[Union[int, float, Decimal, str]] = None
    text: Optional[str] = None
    location: Optional[Location] = None
    area: Optional[Area] = None
    aggregation: Optional[Aggregation] = None
    left_operand: Optional["Operand"] = None
    arithmetic_operator: Optional[
        Literal[
            "ADDITION",
            "MULTIPLICATION",
            "DIVISION",
            "DISTANCE",
            "DIFFERENCE",
            "ABSOLUTE_DIFFERENCE",
            "PERCENTAGE_DIFFERENCE",
            "ABSOLUTE_PERCENTAGE_DIFFERENCE",
        ]
    ] = None
    right_operand: Optional["Operand"] = None
    offset: Optional[Offset] = None

    @model_validator(mode="after")
    def validate_value_change_operand(cls, values):  # pylint: disable=C0116.E0213
        if values.type == "VALUE_CHANGE":
            if values.arithmetic_operator not in [
                "DIFFERENCE",
                "ABSOLUTE_DIFFERENCE",
                "PERCENTAGE_DIFFERENCE",
                "ABSOLUTE_PERCENTAGE_DIFFERENCE",
            ]:
                raise ValueError(
                    "Invalid arithmetic operator for VALUE_CHANGE operand."
                )
            # TODO is it wrongly mentioned in the docs?
            # if values.offset is None:
            #     raise ValueError("Offset must be provided for VALUE_CHANGE operand.")
        return values


Operand.model_rebuild()


class InputCondition(BlockbaxModel):
    type: Literal["THRESHOLD", "TEXT_MATCH", "GEOFENCE"]
    left_operand: Operand
    comparison_operator: Literal[
        "LESS_THAN",
        "LESS_THAN_OR_EQUALS",
        "EQUALS",
        "NOT_EQUALS",
        "GREATER_THAN_OR_EQUALS",
        "GREATER_THAN",
        "CONTAINS",
        "NOT_CONTAINS",
        "STARTS_WITH",
        "NOT_STARTS_WITH",
        "ENDS_WITH",
        "NOT_ENDS_WITH",
        "MATCHES_REGEX",
        "NOT_MATCHES_REGEX",
    ]
    right_operand: Operand

    @model_validator(mode="after")
    def validate_comparison_operator(self):
        type = self.type
        allowed_operators = {
            "THRESHOLD": [
                "LESS_THAN",
                "LESS_THAN_OR_EQUALS",
                "EQUALS",
                "NOT_EQUALS",
                "GREATER_THAN_OR_EQUALS",
                "GREATER_THAN",
            ],
            "TEXT_MATCH": [
                "EQUALS",
                "NOT_EQUALS",
                "CONTAINS",
                "NOT_CONTAINS",
                "STARTS_WITH",
                "NOT_STARTS_WITH",
                "ENDS_WITH",
                "NOT_ENDS_WITH",
                "MATCHES_REGEX",
                "NOT_MATCHES_REGEX",
            ],
            "GEOFENCE": ["CONTAINS", "NOT_CONTAINS"],
        }
        if type in allowed_operators:
            if self.comparison_operator not in allowed_operators[type]:
                raise ValueError(
                    f"Invalid comparison operator for {type} condition: {self.comparison_operator}"
                )
        return self


class DurationCondition(BlockbaxModel):
    period: Period


class OccurrenceCondition(BlockbaxModel):
    period: Period
    occurrences: int


class DayTimeConditionRange(BlockbaxModel):
    from_time: str
    to_time: str


def override_datetime_condition_model_config() -> dict:
    """
    The day names in day time input condition should be capitalized; however the default conversion
    of camelCase to snail_case and back results a lower case string.
    Returns:
        dict: New config with upper case alias generator
    """
    override_model_config = BlockbaxModel.model_config.copy()
    override_model_config["alias_generator"] = str.upper
    return override_model_config


class DayTimeCondition(BlockbaxModel):
    # # Inherit parent model_config and override alias_generator
    model_config = ConfigDict(**override_datetime_condition_model_config())

    MONDAY: Optional[List[DayTimeConditionRange]] = None
    TUESDAY: Optional[List[DayTimeConditionRange]] = None
    WEDNESDAY: Optional[List[DayTimeConditionRange]] = None
    THURSDAY: Optional[List[DayTimeConditionRange]] = None
    FRIDAY: Optional[List[DayTimeConditionRange]] = None
    SATURDAY: Optional[List[DayTimeConditionRange]] = None
    SUNDAY: Optional[List[DayTimeConditionRange]] = None

    def to_request(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_none=True, mode="json")


class ConditionSet(BlockbaxModel):
    id: Optional[Union[UUID, str]] = None
    description: str
    input_conditions: List[InputCondition]
    duration_condition: Optional[DurationCondition] = None
    occurrence_condition: Optional[OccurrenceCondition] = None
    day_time_condition: Optional[DayTimeCondition] = None

    @field_validator("id", mode="before")
    def convert_id_to_uuid(cls, value):  # pylint: disable=C0116.E0213
        if value is not None and isinstance(value, str):
            return UUID(value)
        return value


class SubjectPropertyValuesFilter(BlockbaxModel):
    type_id: Union[UUID, str]
    value_ids: List[Union[UUID, str]]


class SubjectFilterItem(BlockbaxModel):
    subject_ids: Optional[List[Union[UUID, str]]] = None
    property_values: Optional[List[SubjectPropertyValuesFilter]] = None


class SubjectFilter(BlockbaxModel):
    include: Optional[SubjectFilterItem] = None
    exclude: Optional[SubjectFilterItem] = None


class EventRule(BlockbaxModel):
    event_level: Literal["OK", "INFORMATION", "WARNING", "PROBLEM"]
    condition_sets: List[ConditionSet]


class EventTrigger(BlockbaxModel):
    created_date: BlockbaxDatetime
    subject_type_id: SubjectTypeId
    name: str
    version: int
    active: bool
    evaluation_trigger: Literal["INPUT_METRICS", "SUBJECT_METRICS"]
    evaluation_constraint: Literal["NONE", "ALL_TIMESTAMPS_MATCH"]
    event_rules: List[EventRule]
    id: Optional[EventTriggerId] = None  # Make it optional for create requests
    updated_date: Optional[BlockbaxDatetime] = None
    subject_filter: Optional[SubjectFilter] = None

    class Config:
        populate_by_name = True
