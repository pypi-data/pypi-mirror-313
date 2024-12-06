from pathlib import Path
import time
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

from ..util import deprecated

from ..models.metric import Metric
from ..models.ingestion import Ingestion
from ..models.property_type import PropertyType
from ..models.property_type_value import PropertyTypeValue
from ..models.subject_type import (
    SubjectType,
    SubjectTypePrimaryLocation,
    SubjectTypePropertyType,
)
from ..models.project import Project, ProjectResources
from ..models.measurement import measurement_adapter
from ..models.property_type_value import property_type_value_adapter
from ..models.ingestion import IngestionIdOverride
from ..models.subject_property import subject_property_adapter
from ..models.subject_property import SubjectProperty
from ..models.subject import Subject
from ..models.series import Series
from ..models.type_hints import (
    PropertyTypeId,
    PropertyValueId,
    SubjectId,
    SubjectExternalId,
    SubjectTypeId,
    MetricId,
    MetricExternalId,
    IngestionId,
    SubjectIdsMode,
    EventTriggerId,
)
from ..models.data_types import Location, BlockbaxNumber
from ..models.event_trigger import (
    EventTrigger,
    EventRule,
    SubjectFilter,
)
from ..models.event import Event
from ..util import conversions
from ..util import ingestion_queuer
from .api import api as bx_api

from datetime import datetime
import logging


logger = logging.getLogger(__name__)


class HttpClient:
    api: bx_api.Api
    project_id: Optional[str]
    project: Optional[Project]
    endpoint: Optional[str]

    def __init__(
        self, access_token: str, project_id: str, endpoint: Optional[str] = None
    ):
        if access_token and project_id:
            self.project_id = project_id
            self.api = bx_api.Api(
                access_token=access_token, project_id=project_id, endpoint=endpoint
            )
        else:
            raise ValueError("Please provide both project ID and Access token!")
        self.ingestion_queuer = ingestion_queuer.IngestionQueuer()

    def load_project(self, directory_path: Union[str, Path]):
        directory_path = Path(directory_path)
        if directory_path.exists() and not directory_path.is_dir():
            raise ValueError(f"{directory_path} is not a directory")

        self.project = self.get_project_details()
        if self.project is None:
            raise RuntimeError("No project found")
        resources = ProjectResources(
            project=self.project,
            subjects=self.get_subjects(),
            metrics=self.get_metrics(),
            subject_types=self.get_subject_types(),
            property_types=self.get_property_types(),
        )

        return resources

    def get_user_agent(self) -> str:
        return self.api.get_user_agent()  # type: ignore

    def get_project_details(self) -> Optional[Project]:
        project_api_response = self.api.get_project()
        return Project.from_response(project_api_response)

    # Methods to create, update, delete and get property types.

    def get_property_types(
        self,
        name: Optional[str] = None,
        external_id: str = None,
    ) -> List[PropertyType]:
        """Gets property types, optionally with arguments for filtering.

        Arguments:
            name [optional, default=None]: The name of the property type to filter on.

        Returns:
            List of `PropertyType`
        """
        property_type_responses = self.api.get_property_types(
            name=name,
            external_id=external_id,
        )
        property_types = [
            PropertyType.from_response(property_type_response)
            for property_type_response in property_type_responses
        ]
        return [p for p in property_types if p is not None]

    def get_property_type(self, id_: str) -> Optional[PropertyType]:
        """Gets a specific property type.

        Arguments:
            id_ [required]: Property type ID to fetch.

        Returns: `PropertyType`
        """
        property_type_response = self.api.get_property_type(property_type_id=str(id_))
        return PropertyType.from_response(property_type_response)

    def create_property_type(
        self,
        name: str,
        external_id: str,
        data_type: Literal["NUMBER", "TEXT", "LOCATION", "MAP_LAYER", "IMAGE", "AREA"],
        predefined_values: bool,
        values: Optional[List[Union[Dict[str, Any], PropertyTypeValue]]] = None,
    ) -> PropertyType:
        """Creates a property type

        Arguments:
            name [required]:
                The name of the property type.
            data_type [required]:
                The type of the property type. Can be “TEXT”, “NUMBER” or “LOCATION”.
            predefined_values [required]:
                Defines whether it is possible to create values for this property type in the resource itself (for value true) or they are automatically created when adding a value to a subject (for value false).
            values [optional, default=[] ]:
                List of predefined values. A property type can be created with or without predefined values.
        Returns:
            `PropertyType`
        """
        if not predefined_values and values:
            raise ValueError(
                "Values can only be added to a property type with predefined values"
            )
        formatted_values = (
            [
                property_type_value_adapter.validate_python(v).to_request()
                for v in values
            ]
            if values is not None
            else None
        )

        property_type_response = self.api.create_property_type(
            name=name,
            external_id=external_id,
            data_type=data_type,
            predefined_values=predefined_values,
            values=formatted_values,
        )
        return PropertyType.from_response(property_type_response)

    def update_property_type(
        self,
        property_type: Union[dict, PropertyType],
    ) -> Optional[PropertyType]:
        """Updates a property type.
        Arguments:
            property_type [required]: Updated `PropertyType`
        Returns:
            `PropertyType`
        """
        if isinstance(property_type, dict):
            property_type = PropertyType(**property_type)  # TODO add test for this
        property_type_response = self.api.update_property_type(
            property_type_id=str(property_type.id),
            json=property_type.to_request(),
        )
        return PropertyType.from_response(property_type_response)

    def delete_property_type(self, id_: Union[str, PropertyTypeId]) -> None:
        """Deletes a property type.

        Arguments:
            id_ [required]: Property type ID to delete.

        Returns: `None`
        """
        self.api.delete_property_type(property_type_id=str(id_))

    # Methods to create, update, delete and get subject types.

    def get_subject_types(
        self,
        name: Optional[str] = None,
        property_type_ids: Optional[List[Union[str, PropertyTypeId]]] = None,
    ) -> List[SubjectType]:
        """Gets subject types, optionally with arguments for filtering.

        Arguments:
            name [optional, default=None]:
                Filter subject types by name.
            property_types_ids [optional, default=None]:
                A list of strings that contain property type IDs to filter on.

        Returns:
            List of `SubjectType`
        """

        subject_type_responses = self.api.get_subject_types(
            name=name, property_type_ids=conversions.convert_ids(property_type_ids)
        )
        subject_types = [
            SubjectType.from_response(subject_type_response)
            for subject_type_response in subject_type_responses
        ]
        return [st for st in subject_types if st is not None]

    def get_subject_type(
        self,
        id_: Union[str, SubjectTypeId],
    ) -> Optional[SubjectType]:
        """Gets a specific subject type.

        Arguments
            id_ [required]: Subject Type ID to fetch.
        Returns: `SubjectType`
        """

        subject_type_response = self.api.get_subject_type(subject_type_id=str(id_))
        if subject_type_response is None:
            return None
        return SubjectType.from_response(subject_type_response)

    def create_subject_type(
        self,
        name: str,
        parent_ids: Optional[List[str]] = None,  # TODO deprecate in the next version
        parent_subject_type_ids: Optional[List[Union[str, SubjectTypeId]]] = None,
        primary_location: Optional[
            Union[SubjectTypePrimaryLocation, Dict[str, Any]]
        ] = None,
        property_types: Optional[
            List[Union[SubjectTypePropertyType, Dict[str, Any]]]
        ] = None,
    ) -> SubjectType:
        """Creates a subject type

        Arguments:
            name [required]:
                The name of the subject type.
            primary_location [optional, default=None ]:
                The primary location metric or property type of this subject type, for displaying the location of subjects on the map.
            property_types [optional, default=None ]:
                List of property type dictionary's associated with this subject type.

        Returns: `SubjectType`
        """
        if parent_ids is not None:
            deprecated.deprecation_warning(
                'Argument "parent_ids" is deprecated and will be removed in future \
                    versions. Use "parent_subject_type_ids" instead.'
            )
            if parent_subject_type_ids is not None:
                logger.warning(
                    'Providing values for both "parent_subject_type_ids" and "parent_ids"\
                          is redundant. "parent_ids" is deprecated and will be discarded'
                )
            else:
                parent_subject_type_ids = parent_ids
        validated_property_types: List[SubjectTypePropertyType] = []

        if property_types is not None:
            for p in property_types:
                validated_property_types.append(
                    SubjectTypePropertyType.model_validate(p)
                )

        validated_primary_location = None
        if primary_location is not None:
            if isinstance(primary_location, dict):
                validated_primary_location = SubjectTypePrimaryLocation(
                    **primary_location
                )
            elif isinstance(primary_location, SubjectTypePrimaryLocation):
                validated_primary_location = primary_location
            else:
                raise TypeError("Not a supported primary_location type")
            # Automatically add primary location property type to the list of property types
            if validated_primary_location.type == "PROPERTY_TYPE":
                for validated_property_type in validated_property_types:
                    if validated_primary_location.id == validated_property_type.id:
                        break
                else:
                    validated_property_types.append(
                        SubjectTypePropertyType(
                            id=validated_primary_location.id,
                            required=True,
                        )
                    )

        subject_type_response = self.api.create_subject_type(
            name=name,
            parent_subject_type_ids=conversions.convert_ids(parent_subject_type_ids),
            primary_location=(
                validated_primary_location.to_request()
                if validated_primary_location is not None
                else None
            ),
            property_types=(
                [p.to_request() for p in validated_property_types]
                if validated_property_types
                else None
            ),
        )

        return SubjectType.from_response(subject_type_response)

    def update_subject_type(
        self,
        subject_type: SubjectType,
    ) -> Optional[SubjectType]:
        """Updates a subject type.

        Arguments:
            subject_type [required]: Updated `SubjectType`

        Returns: `SubjectType`
        """
        subject_type_response = self.api.update_subject_type(
            subject_type_id=str(subject_type.id),
            json=subject_type.to_request(),
        )

        return SubjectType.from_response(subject_type_response)

    def delete_subject_type(
        self,
        id_: Union[str, SubjectTypeId],
    ) -> None:
        """Deletes a subject type.

        Arguments:
            id_ [required]: Subject type ID to delete.
        Returns: `None`
        """

        self.api.delete_subject_type(subject_type_id=str(id_))

    # Methods to create, update, delete and get metrics.

    def get_metrics(
        self,
        name: Optional[str] = None,
        metric_external_id: Optional[Union[str, MetricExternalId]] = None,
        subject_type_ids: Optional[List[Union[str, SubjectTypeId]]] = None,
    ) -> List[Metric]:
        """Gets metrics, optionally with arguments for filtering.

        Arguments:
            name [optional, default=None]:
                Filter property types by name.
            external_id [optional, default=None]:
                Filter metrics by external ID.
            subject_type_ids [optional, default=None]:
                Filter on a list of subject type IDs.
        Returns:
            List of `Metric`
        """

        metric_responses = self.api.get_metrics(
            name=name,
            metric_external_id=metric_external_id,
            subject_type_ids=conversions.convert_ids(subject_type_ids),
        )
        metrics = [
            Metric.from_response(metric_response)
            for metric_response in metric_responses
            if Metric.from_response(metric_response) is not None
        ]
        return [metric for metric in metrics if metric is not None]

    def get_metric(
        self,
        id_: Union[str, MetricId],
    ) -> Optional[Metric]:
        """Gets a specific metric.

        Arguments:
            id_ [required]: Metric ID to fetch.

        Returns: `Metric`
        """
        metric_response = self.api.get_metric(metric_id=str(id_))

        return Metric.from_response(metric_response)

    def create_metric(
        self,
        subject_type_id: str,
        name: str,
        data_type: Literal["NUMBER", "TEXT", "LOCATION"],
        type_: Literal["INGESTED"],  # type: ignore
        mapping_level: Literal["OWN", "CHILD"],
        external_id: Optional[str] = None,
        unit: Optional[str] = None,
        precision: Optional[int] = None,
        visible: Optional[bool] = True,
        discrete: Optional[bool] = False,
        preferred_color: Optional[str] = None,
    ) -> Metric:
        """Creates a metric.

        Arguments:
            subject_type_id [required]:
                Subject type ID that this metric belongs to. Determines which subjects, property types and metrics are connected.
            name [required]:
                The name of the metric.
            data_type [required]:
                The data type of the metric. Choose from: NUMBER or LOCATION.
            type_ [required]:
                The type of the metric. Currently only the INGESTED type is supported.
            mapping_level [required]:
                The level on which the ingestion ID mappings are set. Choose from: OWN or CHILD. In most cases the ingestion ID for a metric is configured on the type's own level, meaning at the subjects containing the metric. However, in some cases it might be useful to do this at child level. If ingestion IDs are derived from the external IDs of a subject and a metric, this makes it possible to move a subject to another parent without having to update the ingestion ID.
            discrete [optional, default=False]
                Whether this metric has discrete values. This is used by the web app to optimize visualization.
            unit [optional, default=None]:
                The unit of the metric.
            precision [optional, default=None]:
                The precision to show in the client for the metric, from 0 to 8.
            visible [optional, default=True]:
                Whether this metric is visible in the client.
            external_id [optional, default=None]:
                The external ID of the subject. This can be used when sending measurements to avoid the source systems (e.g. sensors) need to know which IDs are internally used in the Blockbax Platform. If left empty the external ID will be derived from the given name but it is recommended that one is given.

        Returns: `Metric`
        """

        metric_type = type_.upper()

        if metric_type == "SIMULATED" or metric_type == "CALCULATED":
            metric_type_not_implemented_error = (
                f"Creating metric with type: {type_} is not yet implemented!"
            )
            raise NotImplementedError(metric_type_not_implemented_error)

        if external_id is None:
            external_id = conversions.convert_name_to_external_id(name=name)

        return Metric.from_response(
            self.api.create_metric(
                subject_type_id=str(subject_type_id),
                name=name,
                data_type=data_type.upper(),
                type_=metric_type,
                external_id=external_id,
                mapping_level=mapping_level.upper(),
                unit=unit,
                precision=precision,
                visible=visible,
                discrete=discrete,
                preferred_color=preferred_color,
            )
        )

    def update_metric(
        self,
        metric: Metric,
    ) -> Optional[Metric]:
        """Updates a metric.

        Arguments:
            metric [required]: Updated `Metric`

        Returns: `Metric`
        """
        metric_api_response = self.api.update_metric(
            metric_id=str(metric.id),
            json=metric.to_request(),
        )

        return Metric.from_response(metric_api_response)

    def delete_metric(
        self,
        id_: Union[str, MetricId],
    ):
        """Deletes a metric.

        Arguments:
            id_ [required]: Metric ID to delete

        Returns: `None`
        """
        self.api.delete_metric(metric_id=str(id_))

    # Methods to create, update, delete and get subjects.

    def get_subjects(
        self,
        name: Optional[str] = None,
        subject_ids: Optional[List[Union[str, SubjectId]]] = None,
        external_id: Optional[Union[str, SubjectExternalId]] = None,
        subject_external_id: Optional[
            Union[str, SubjectExternalId]
        ] = None,  # TODO deprecate in newer version
        subject_ids_mode: Optional[Union[str, SubjectIdsMode]] = None,
        subject_type_ids: Optional[List[Union[str, SubjectTypeId]]] = None,
        property_value_ids: Optional[
            Union[
                Tuple[Union[str, PropertyValueId]],
                List[Union[str, PropertyValueId]],
                Union[str, PropertyValueId],
            ]
        ] = None,
    ) -> List[Subject]:
        """Gets subjects, optionally with arguments for filtering.

        Arguments:
            name: Filter subjects by name.
            external_id: Filter subjects by external ID.
            subject_type_ids: Filter on a list of subject type IDs.
            property_value_ids: Filter property value IDs using a string or a combination of a list with tuples.
                For strings use a ',' separator for OR and ';' for AND, e.g. <A>,<B>;<C> translates to (A OR B) AND C.
                Instead of a string IDs can be encapsulate in a tuple for OR and encapsulate IDs in a list for AND.
                e.g. [('A', 'B'),'C'] translates to <A>,<B>;<C> a.k.a (A OR B) AND C.

        Returns: `Subject`
        """
        if subject_external_id is not None:
            deprecated.deprecation_warning(
                'Argument "subject_external_id" is deprecated and will be removed in future \
                    versions. Use "external_id" instead.'
            )
            if external_id is not None:
                logger.warning(
                    'Providing values for both "external_id" and "subject_external_id"\
                        is redundant. "subject_external_id" is deprecated and will be discarded'
                )
            else:
                external_id = subject_external_id
        property_value_ids = conversions.convert_property_value_ids_to_query_filter(
            property_value_ids
        )

        subject_responses = self.api.get_subjects(
            name=name,
            subject_ids=conversions.convert_ids(subject_ids),
            subject_ids_mode=subject_ids_mode,
            subject_external_id=external_id,
            subject_type_ids=subject_type_ids,
            property_value_ids=property_value_ids,
        )

        subject_list: List[Subject] = []
        for subject_response in subject_responses:
            subject = Subject.from_response(subject_response)
            if subject is not None:
                subject_list.append(subject)
        return subject_list

    def get_subject(self, id_: Union[str, SubjectId]) -> Optional[Subject]:
        """Gets a specific subject.

        Arguments:
            id_ [required]: Subject ID to fetch.

        Returns: `Subject`
        """

        subject_response = self.api.get_subject(subject_id=str(id_))
        return Subject.from_response(subject_response)

    def create_subject(
        self,
        name: str,
        subject_type_id: Union[str, SubjectTypeId],
        parent_id: Optional[str] = None,  # TODO deprecate in newer version
        parent_subject_id: Optional[Union[str, SubjectId]] = None,
        properties: Optional[List[Union[Dict[str, Any], SubjectProperty]]] = None,
        ingestion_id_overrides: Optional[IngestionIdOverride] = None,
        external_id: Optional[Union[str, SubjectExternalId]] = None,
    ) -> Subject:
        """Creates a subject.

        Arguments:
            subject_type_id [required]:
                Subject type that this subjects belongs to. Determines which subjects, property types and metrics are connected.
            name [required]:
                The name of the subject.
            parent_subject_id [optional, default=None]:
                The ID of the parent subject of this subject. Required if the subject type has a parent subject type. Not allowed otherwise.
            properties [optional, default=None]:
                List of the properties of this subject.
            ingestion_id_overrides [optional, default={} ]:
                Dictionary of metric ID ingestion ID pairs, ingestion ID’s belonging to metrics that are defined in the Subject Type but are not defined here will be automatically derived from the subject and metric external ID.
            external_id [optional, default=None]:
                The external ID of the subject. This can be used when sending measurements to avoid the source systems (e.g. sensors) need to know which IDs are internally used in the Blockbax Platform. If left empty the external ID will be derived from the given name but it is recommended that one is given.

        Returns: `Subject`
        """
        if parent_id is not None:
            deprecated.deprecation_warning(
                'Argument "parent_id" is deprecated and will be removed in future \
                    versions. Use "parent_subject_id" instead.'
            )
            if parent_subject_id is not None:
                logger.warning(
                    'Providing values for both "parent_subject_id" and "parent_id"\
                          is redundant. "parent_id" is deprecated and will be discarded'
                )
            else:
                parent_subject_id = parent_id
        subject_response = self.api.create_subject(
            name=name,
            parent_subject_id=(
                str(parent_subject_id) if parent_subject_id is not None else None
            ),
            subject_type_id=(
                str(subject_type_id) if subject_type_id is not None else None
            ),
            external_id=(
                external_id
                if external_id is not None
                else conversions.convert_name_to_external_id(name=name)
            ),
            ingestion_ids=conversions.convert_ingestion_id_overrides(
                ingestion_id_overrides
            ),  # TODO replace with pydantic method
            properties=(
                [
                    subject_property_adapter.validate_python(p).to_request()
                    for p in properties
                ]
                if properties is not None
                else None
            ),
        )
        # If successful this cannot be 'None'
        return Subject.from_response(subject_response)

    def update_subject(
        self,
        subject: Subject,
    ) -> Optional[Subject]:
        """Updates a subject.

        Arguments:
            subject [required]: Updated `Subject`

        Returns: `Subject`
        """

        subject_response = self.api.update_subject(
            subject_id=str(subject.id),
            json=subject.to_request(),
        )

        return Subject.from_response(subject_response)

    def delete_subject(self, id_: Union[str, SubjectId]) -> None:
        """Deletes a subject.

        Arguments:
            id_ [required]: Subject ID to delete.

        Returns: `None`
        """

        self.api.delete_subject(subject_id=str(id_))

    # Methods to queue, send and get measurements

    def queue_measurement(
        self,
        ingestion_id: Union[str, IngestionId],
        date: Optional[Union[int, float, datetime, str]] = None,
        number: Optional[BlockbaxNumber] = None,
        location: Optional[Union[Dict[str, Any], Location]] = None,
        text: Optional[str] = None,
        generate_date: bool = None,
    ):
        """Queues measurements to send.

        Arguments:
            ingestion_id [required]:
                Ingestion ID
            date [required]:
                `datetime`, Unix timestamp or string parsable by the dateutil.parser, or integer of unix seconds.
                If numeric value is passed it will initially be interpreted as epoch seconds.
                If parsing that value fails because it is too large, it will then be interpreted as epoch milliseconds.
            number [optional, default=None]:
                Decimal number, must be filled if location = None.
            location [optional, default=None]:
                Location dictionary, must be filled if number = None.

        Returns: `None`
        """
        if generate_date is not None:
            deprecated.deprecation_warning(
                "The `generate_date` argument is deprecated and will be removed in future versions."
                " As of this version, it has no effect; measurements without a date will"
                " automatically use the current date."
            )
        if date is None:
            date = int(time.time() * 1000)

        measurement_dict = {
            "date": date,
            "number": number,
            "location": location,
            "text": text,
        }
        measurement_dict = {k: v for k, v in measurement_dict.items() if v is not None}
        measurement = measurement_adapter.validate_python(measurement_dict)
        self.ingestion_queuer.add_ingestion(
            Ingestion(ingestion_id=ingestion_id, measurement=measurement)
        )

    def send_measurements(
        self,
    ):
        """Sends queued measurements.

        Returns: `None`
        """

        for series_batch in self.ingestion_queuer.create_series_to_send():
            self.api.send_measurements(series=series_batch.to_request())
        self.ingestion_queuer.clear_stack_and_counts()

    def get_measurements(
        self,
        subject_ids: Optional[List[Union[str, SubjectId]]] = None,
        metric_ids: Optional[List[Union[str, MetricId]]] = None,
        from_date: Optional[Union[datetime, int, float, str]] = None,
        to_date: Optional[Union[datetime, int, float, str]] = None,
        size: int = None,
        order: str = None,
    ) -> List[Series]:
        """Gets measurements with arguments for filtering.

        Arguments:
            subject_ids [optional, default=[] ]:
                List of IDs of the subjects. When passing a fromDate or toDate, this must only contain one subject ID.
            metric_ids [optional, default=[] ]:
                List of IDs of the metrics. When passing a fromDate or toDate, this must only contain one metric ID.
            from_date [optional, default=None]:
                `datetime`, integer unix timestamp or string parsable by the dateutil.parser
            to_date [optional, default=None]:
                `datetime`, integer unix timestamp or string parsable by the dateutil.parser
            order [optional, default=asc]:
                Ordering of measurements based on the date ("asc" or "desc").

        Returns: List of `Series`
        """

        measurements_responses = self.api.get_measurements(
            subject_ids=conversions.convert_ids(subject_ids),
            metric_ids=conversions.convert_ids(metric_ids),
            from_date=conversions.convert_any_date_to_iso8601(from_date),
            to_date=conversions.convert_any_date_to_iso8601(to_date),
            size=size,
            order=order,
        )
        series = []
        if measurements_responses is not None:
            for series_response in measurements_responses.get("series") or []:
                s = Series.from_response(series_response)
                if s is not None:
                    series.append(s)
        return series

    # Event triggers
    def get_event_triggers(
        self,
        name: Optional[str] = None,
    ) -> List[EventTrigger]:
        """Gets event triggers, optionally filtered by name.

        Arguments:
            name [optional, default=None]:
                Filter event triggers by name.

        Returns:
            List of `EventTrigger`
        """
        event_trigger_response_items = self.api.get_event_triggers(
            name=name,
        )
        event_triggers = [
            EventTrigger.from_response(event_trigger_response)
            for event_trigger_response in event_trigger_response_items
            if EventTrigger.from_response(event_trigger_response) is not None
        ]
        return [
            event_trigger
            for event_trigger in event_triggers
            if event_trigger is not None
        ]

    def get_event_trigger(
        self,
        id_: Union[str, EventTriggerId],
    ) -> Optional[EventTrigger]:
        """Gets a specific event trigger by ID.

        Arguments:
            id_ [required]:
                Event trigger ID to fetch.

        Returns:
            `EventTrigger`
        """
        event_trigger_response = self.api.get_event_trigger(event_trigger_id=str(id_))

        return EventTrigger.from_response(event_trigger_response)

    def create_event_trigger(
        self,
        subject_type_id: str,
        name: str,
        active: bool,
        evaluation_trigger: str,
        evaluation_constraint: str,
        event_rules: List[Union[EventRule, dict]],
        subject_filter: List[Union[SubjectFilter, dict]] = None,
    ) -> EventTrigger:
        """Creates an event trigger.

        Arguments:
            subject_type_id [required]:
                The ID of the subject type the event trigger applies to.
            name [required]:
                The name of the event trigger.
            active [required]:
                Whether the event trigger is active.
            evaluation_trigger [required]:
                The trigger condition for the event evaluation.
            evaluation_constraint [required]:
                Constraints for the event evaluation.
            event_rules [required]:
                List of event rules as dictionaries.
            subject_filter [optional, default=None]:
                Dictionary for filtering subjects.

        Returns:
            `Dict[str, Any]`
        """
        event_rules_as_dict = [
            (
                # er.model_dump(by_alias=True, exclude_none=True, exclude_unset=True)
                er.to_request()
                if isinstance(er, EventRule)
                else er
            )
            for er in event_rules
        ]
        subject_filter_as_dict = (
            subject_filter.to_request()
            if isinstance(subject_filter, SubjectFilter)
            else subject_filter
        )
        return EventTrigger.from_response(
            self.api.create_event_trigger(
                subject_type_id=str(subject_type_id),
                name=name,
                active=active,
                evaluation_trigger=evaluation_trigger,
                evaluation_constraint=evaluation_constraint,
                event_rules=event_rules_as_dict,
                subject_filter=subject_filter_as_dict,
            )
        )

    def update_event_trigger(
        self,
        event_trigger: EventTrigger,
    ) -> Dict[str, Any]:
        """Updates an existing event trigger.

        Arguments:
            event_trigger [required]:
                The `EventTrigger` object with updated information.

        Returns:
            `Dict[str, Any]`
        """
        update_event_trigger__api_response = self.api.update_event_trigger(
            event_trigger_id=str(event_trigger.id),
            json=event_trigger.to_request(),
        )

        return EventTrigger.from_response(update_event_trigger__api_response)

    def delete_event_trigger(self, id_: Union[str, EventTriggerId]) -> None:
        """Deletes an event trigger.

        Arguments:
            id_ [required]: Event trigger ID to delete.

        Returns: `None`
        """
        self.api.delete_event_trigger(event_trigger_id=str(id_))

    # Event
    def get_events(
        self,
        active: Optional[bool] = None,
        suppressed: Optional[bool] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        only_new: Optional[bool] = None,
        property_value_ids: Optional[List[Union[str, PropertyValueId]]] = None,
        subject_ids: Optional[List[Union[str, SubjectId]]] = None,
        event_trigger_ids: Optional[List[Union[str, EventTriggerId]]] = None,
        event_levels: Optional[
            List[Literal["OK", "INFORMATION", "WARNING", "PROBLEM"]]
        ] = None,
        sort: str = "startDate,desc",
    ) -> List[Event]:
        events_response = self.api.get_events(
            active=active,
            suppressed=suppressed,
            from_date=conversions.convert_any_date_to_iso8601(from_date),
            to_date=conversions.convert_any_date_to_iso8601(to_date),
            only_new=only_new,
            property_value_ids=conversions.convert_ids(property_value_ids),
            subject_ids=conversions.convert_ids(subject_ids),
            event_trigger_ids=conversions.convert_ids(event_trigger_ids),
            event_levels=event_levels,
            sort=sort,
        )
        return [Event.from_response(event_data) for event_data in events_response]

    def get_event(self, id_: Union[str, SubjectId]) -> Optional[Event]:
        event_response = self.api.get_event(event_id=id_)
        return Event.from_response(event_response) if event_response else None
