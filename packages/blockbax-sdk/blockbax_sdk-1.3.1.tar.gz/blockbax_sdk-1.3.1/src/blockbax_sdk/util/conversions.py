from typing import Any, Dict, List, Optional, Tuple, cast, Union
from uuid import UUID

from dateutil import parser as date_parser
from datetime import datetime, timezone

import logging

from ..models import IngestionIdOverride
from ..models.type_hints import BlockbaxId, PropertyValueId

logger = logging.getLogger(__name__)


# date conversions


def convert_any_date_to_unix_millis(date: Union[datetime, int, float, str]) -> int:
    if isinstance(date, int) or isinstance(date, float):
        try:
            datetime.fromtimestamp(date)
            return int(date * 1000)
        except (ValueError, OSError):
            try:
                # Try to parse the numeric date as epoch milliseconds
                datetime.fromtimestamp(date / 1000)
                return int(date)
            except ValueError as exc:
                raise ValueError(
                    "Cannot parse numeric date as a valid datetime"
                ) from exc

    elif isinstance(date, datetime):
        return int(date.timestamp() * 1000)
    elif isinstance(date, str):
        # Parse the string using dateutil.parser
        dt_obj = date_parser.parse(date)
        return int(dt_obj.timestamp() * 1000)
    else:
        raise ValueError("Not a valid type for date")


def convert_any_date_to_iso8601(
    date: Optional[Union[datetime, int, float, str]]
) -> Optional[str]:
    if date is None:
        return None
    unix_millis = convert_any_date_to_unix_millis(date)
    return datetime.fromtimestamp(unix_millis / 1000, tz=timezone.utc).isoformat(
        timespec="milliseconds"
    )


def convert_name_to_external_id(name: str):
    lower_case_name = name.lower()
    external_id = lower_case_name.replace(" ", "-").strip()
    return external_id


def convert_property_value_ids_to_query_filter(
    property_value_ids: Optional[
        Union[
            Tuple[Union[str, PropertyValueId]],
            List[Union[str, PropertyValueId]],
            Union[str, PropertyValueId],
        ]
    ]
) -> Optional[str]:
    if isinstance(property_value_ids, (tuple, list)):
        separator = "," if isinstance(property_value_ids, tuple) else ";"
        return separator.join(
            [
                (
                    str(id_)
                    if isinstance(id_, (str, UUID))
                    else cast(
                        Union[str, PropertyValueId],
                        convert_property_value_ids_to_query_filter(id_),
                    )
                )
                for id_ in property_value_ids
            ]
        )
    elif isinstance(property_value_ids, str):
        return property_value_ids
    elif isinstance(property_value_ids, UUID):
        return str(property_value_ids)
    return None


def convert_ingestion_id_overrides(
    ingestion_id_overrides: Optional[IngestionIdOverride],
) -> List[Dict[str, Any]]:
    ingestion_ids = []
    if ingestion_id_overrides is not None:
        for metric_id, ingestion_id in ingestion_id_overrides.items():
            ingestion_ids.append(
                {
                    "metricId": metric_id,
                    "deriveIngestionId": False,
                    "ingestionId": ingestion_id,
                }
            )
    return ingestion_ids


def convert_id(id: Optional[Union[str, BlockbaxId]]) -> Optional[str]:
    if id is None:
        return None
    return str(id)


def convert_ids(ids: Optional[List[Union[str, BlockbaxId]]]) -> Optional[List[str]]:
    if ids is None:
        return None
    return [str(id) for id in ids]
