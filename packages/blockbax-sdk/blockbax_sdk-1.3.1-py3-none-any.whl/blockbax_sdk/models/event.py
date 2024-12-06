from typing import List, Literal, Optional
from uuid import UUID

from ..models.base import BlockbaxModel
from .type_hints import BlockbaxDatetime, EventTriggerId, SubjectId


class Event(BlockbaxModel):
    id: UUID
    event_trigger_id: EventTriggerId
    event_trigger_version: int
    event_level: Literal["OK", "INFORMATION", "WARNING", "PROBLEM"]
    subject_id: SubjectId
    condition_set_ids: List[UUID]
    start_date: BlockbaxDatetime
    end_date: Optional[BlockbaxDatetime] = None
    suppressed: bool
