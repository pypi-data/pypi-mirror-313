from typing import List, Optional
from .base import BlockbaxModel
from .type_hints import ProjectId, OrganizationId, BlockbaxDatetime
from . import Subject, Metric, SubjectType, PropertyType


class Project(BlockbaxModel):
    id: ProjectId
    created_date: BlockbaxDatetime
    name: str
    description: str
    timezone_id: str
    organization_id: OrganizationId
    updated_date: Optional[BlockbaxDatetime] = None


class ProjectResources(BlockbaxModel):
    project: Project
    subjects: List[Subject]
    metrics: List[Metric]
    subject_types: List[SubjectType]
    property_types: List[PropertyType]
