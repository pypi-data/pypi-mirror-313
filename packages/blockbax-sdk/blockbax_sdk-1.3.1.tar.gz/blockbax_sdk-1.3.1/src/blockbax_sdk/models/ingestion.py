from typing import List, TypedDict

from .base import BlockbaxModel
from .type_hints import IngestionId
from .measurement import Measurement

import logging

logger = logging.getLogger(__name__)


import logging

from .measurement import Measurement


logger = logging.getLogger(__name__)


class Ingestion(BlockbaxModel):
    ingestion_id: IngestionId
    measurement: Measurement


class IngestionCollection(BlockbaxModel):
    ingestion_id: IngestionId
    measurements: List[Measurement]


class IngestedSeries(BlockbaxModel):
    series: List[IngestionCollection]


class IngestionIdOverride(TypedDict):
    metric_id: IngestionId
