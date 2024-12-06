from typing import TypeVar
from uuid import UUID
from datetime import datetime
from typing_extensions import Annotated

from .base import BlockbaxEnum
from pydantic import PlainSerializer


T = TypeVar("T")
BlockbaxType = Annotated[T, "BlockbaxType"]
BlockbaxId = Annotated[
    BlockbaxType[UUID],
    "BlockbaxId",
    PlainSerializer(lambda x: str(x), return_type=str, when_used="unless-none"),
]
BlockbaxExternalId = Annotated[BlockbaxType[str], "BlockbaxExternalId"]

# Other ID
IngestionId = Annotated[BlockbaxType[str], "Ingestion"]

# UUID' s
ProjectId = Annotated[BlockbaxId, "Project"]
OrganizationId = Annotated[BlockbaxId, "Project"]
SubjectId = Annotated[BlockbaxId, "Subject"]
MetricId = Annotated[BlockbaxId, "Metric"]
EventTriggerId = Annotated[BlockbaxId, "EventTrigger"]
PropertyTypeId = Annotated[BlockbaxId, "PropertyType"]
SubjectTypeId = Annotated[BlockbaxId, "SubjectType"]
PropertyValueId = Annotated[BlockbaxId, "PropertyValue"]

# External ID' s
SubjectExternalId = Annotated[BlockbaxExternalId, "Subject"]
MetricExternalId = Annotated[BlockbaxExternalId, "Metric"]
PropertyTypeExternalId = Annotated[BlockbaxExternalId, "PropertyType"]

BlockbaxDatetime = Annotated[
    datetime,
    PlainSerializer(
        lambda d: int(d.timestamp() * 1000),
        return_type=int,
        when_used="unless-none",
    ),
]


class SubjectIdsMode(BlockbaxEnum):
    SELF = "SELF"
    CHILDREN = "CHILDREN"
    ALL = "ALL"
