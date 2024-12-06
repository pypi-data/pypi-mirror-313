from collections import OrderedDict, defaultdict
from itertools import groupby
from typing import Dict, List, Union
import logging
from .. import models
from ..errors import BlockbaxError

logger = logging.getLogger(__name__)


class SendMeasurementError(BlockbaxError):
    pass


class IngestionQueuer:
    def __init__(
        self,
    ) -> None:
        # Use OrderedDict for the outer dict to maintain insertion order
        self.timestamp_to_subject_key_to_ingestions: Dict[
            int, Dict[str, List[models.ingestion.Ingestion]]
        ] = OrderedDict()

        self.batch_max_size = 500
        self.total_processed_ingestions = 0

    def add_ingestion(self, ingestion: models.ingestion.Ingestion) -> None:
        if (
            ingestion.measurement.date
            not in self.timestamp_to_subject_key_to_ingestions
        ):
            self.timestamp_to_subject_key_to_ingestions[ingestion.measurement.date] = (
                defaultdict(list)
            )

        self.timestamp_to_subject_key_to_ingestions[ingestion.measurement.date][
            self.get_subject_external_id(ingestion.ingestion_id)
        ].append(ingestion)

        self.total_processed_ingestions += 1

    def clear_stack_and_counts(self):
        self.timestamp_to_subject_key_to_ingestions = OrderedDict()

    def queue_ingestions(
        self, ingestions: List[Union[dict, models.ingestion.Ingestion]]
    ):
        for ingestion in ingestions:
            self.add_ingestion(ingestion=ingestion)

    @classmethod
    def get_subject_external_id(cls, ingestion_id: str):
        return ingestion_id.split("$")[0]

    def create_ingestion_batches(self) -> List[List[models.ingestion.Ingestion]]:
        ingestion_batches: List[List[models.ingestion.Ingestion]] = []
        current_ingestion_batch: List[models.ingestion.Ingestion] = []

        # Sort the timestamps before iterating
        sorted_timestamp_to_subject_key = OrderedDict(
            sorted(self.timestamp_to_subject_key_to_ingestions.items())
        )

        for subject_key_to_ingestions in sorted_timestamp_to_subject_key.values():
            for ingestions in subject_key_to_ingestions.values():
                for i in range(0, len(ingestions), self.batch_max_size):
                    ingestion_batch = ingestions[i : i + self.batch_max_size]
                    if (
                        len(ingestion_batch) + len(current_ingestion_batch)
                        > self.batch_max_size
                    ):
                        # The priority is that the measurements of the same subject be pushed
                        # together. This if statement would be True only at the start of measurement
                        # of a new subject. So even if the measurements from last batch of the previous
                        # subject does not fill a full batch of 500, it would be pushed to keep room
                        # for the new subject measurements at this timestamp to be pushed as closely
                        # as possible together
                        ingestion_batches.append(current_ingestion_batch)
                        current_ingestion_batch = []
                    current_ingestion_batch.extend(ingestion_batch)
        # Add the remainder measurements from the last batch
        ingestion_batches.append(current_ingestion_batch)

        return ingestion_batches

    def create_series_to_send(self):
        ingestion_batches = self.create_ingestion_batches()
        for batch in ingestion_batches:
            series_list: List[models.ingestion.IngestionCollection] = []
            batch = sorted(batch, key=lambda s: s.ingestion_id)
            grouped_by_ingestion_id = groupby(batch, key=lambda s: s.ingestion_id)
            for ingestion_id, ingestion_group in grouped_by_ingestion_id:
                measurements: List[models.Measurement] = []
                for ing in ingestion_group:
                    measurements.append(ing.measurement)
                series_list.append(
                    models.ingestion.IngestionCollection(
                        ingestion_id=ingestion_id,
                        measurements=measurements,
                    )
                )
            yield models.ingestion.IngestedSeries(series=series_list)

    def get_total_processed_ingestions_count(self) -> int:
        """
        Get the total number of measurements added as ingestions.
        Note that it does NOT directly translate to the number of measurements ended up in Blockbax.
        But the ones for which sending measurements is attempted.
        Returns:
            int: _description_
        """
        return self.total_processed_ingestions
