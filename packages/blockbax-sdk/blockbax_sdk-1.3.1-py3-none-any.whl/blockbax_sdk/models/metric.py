from typing import Optional

from ..models.base import BlockbaxModel
from .type_hints import (
    MetricId,
    MetricExternalId,
    BlockbaxDatetime,
    SubjectTypeId,
)


class Metric(BlockbaxModel):
    id: MetricId
    created_date: BlockbaxDatetime
    subject_type_id: SubjectTypeId
    name: str
    # Usually Literal["NUMBER", "TEXT", "LOCATION"]; relaxed type for cases with new unknown data types
    data_type: str
    # Usually Literal["INGESTED", "CALCULATED", "SIMULATED"]; relaxed type for cases with new unknown data types
    type: str
    updated_date: Optional[BlockbaxDatetime] = None
    unit: Optional[str] = None
    precision: Optional[int] = None
    visible: Optional[bool] = None
    discrete: Optional[bool] = None
    preferred_color: Optional[str] = None
    external_id: Optional[MetricExternalId] = None
    # Usually Literal["OWN", "CHILD"]; relaxed type for cases with new mapping levels
    mapping_level: Optional[str] = None
