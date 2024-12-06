from typing import Any, Dict, Generator, List, Optional, ClassVar, Union

import logging
import math
import platform
import sys
from uuid import UUID

import httpx
from urllib.parse import urljoin
from tenacity import Retrying, TryAgain, RetryCallState
from tenacity.wait import wait_exponential
from tenacity.stop import stop_after_attempt


import blockbax_sdk as bx
from . import api_utils


log = logging.getLogger(__name__)


class BlockbaxAuth(httpx.Auth):
    def __init__(self, token: str):
        self.token = token

    # Override
    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        request.headers["Authorization"] = f"ApiKey {self.token}"
        yield request


BASE_URL = "https://api.blockbax.com"
DEFAULT_API_VERSION = "v1"
PROJECTS_ENDPOINT = "projects"


def get_base_project_url(
    project_id: Union[str, UUID],
    base_url: str = BASE_URL,
    api_version: str = DEFAULT_API_VERSION,
    projects_endpoint: str = PROJECTS_ENDPOINT,
) -> str:
    """
    Constructs the complete URL for accessing a specific project in the Blockbax API.
    This approach also handles trailing slashes in the endpoint args.
    Args:
        project_id (Union[str,UUID]): The unique identifier for the project.
        base_url (str, optional): The base URL of the API. Defaults to BASE_URL, which is "https://api.blockbax.com".
        api_version (str, optional): The API version to be used. Defaults to DEFAULT_API_VERSION, which is "v1".
        projects_endpoint (str, optional): The endpoint for projects in the API. Defaults to PROJECTS_ENDPOINT, which is "projects".

    Returns:
        str: The complete URL for the specified project in the Blockbax API.
    """
    if isinstance(project_id, UUID):
        project_id = str(project_id)

    # Ensure no leading slashes and consistent structure
    base_url = base_url.rstrip("/") + "/"
    api_version = api_version.strip("/") + "/"
    projects_endpoint = projects_endpoint.strip("/") + "/"

    return urljoin(
        urljoin(urljoin(base_url, api_version), projects_endpoint), project_id
    )


class BlockbaxHTTPSession(httpx.Client):
    user_agent: ClassVar[str] = (
        f"Blockbax Python SDK/{bx.__version__} HTTPX/{httpx.__version__} Python/{sys.version} {platform.platform()}".replace(
            "\n", ""
        )
    )
    tries: ClassVar[int] = 3
    back_off_factor: ClassVar[int] = 1
    status_force_list: ClassVar[List[int]] = [
        httpx.codes.BAD_GATEWAY,
        httpx.codes.SERVICE_UNAVAILABLE,
        httpx.codes.GATEWAY_TIMEOUT,
    ]
    timeout_seconds: ClassVar[float] = 10.0
    _sleep_buffer: ClassVar[int] = 1

    retryer: Retrying
    rate_limit_option: api_utils.RateLimitOption

    def __init__(
        self,
        token: str,
        project_id: str,
        endpoint: str,
        rate_limit_option: api_utils.RateLimitOption = api_utils.RateLimitOption.SLEEP,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.rate_limit_option = rate_limit_option
        self.retryer = Retrying(
            # Reraise the original error after the last attempt failed
            reraise=True,
            # Return the result of the last call attempt
            retry_error_callback=self.__retry_error_callback,
            # Exponential backoff
            wait=wait_exponential(multiplier=self.back_off_factor, min=1, max=10),
            # Stop retrying after the defined number of tries
            stop=stop_after_attempt(self.tries),
        )
        headers = httpx.Headers(
            {
                "Content-Type": "application/json",
                "User-Agent": self.user_agent,
            }
        )

        super(BlockbaxHTTPSession, self).__init__(
            trust_env=False,
            event_hooks={
                "request": [self.request_hook],
                "response": [self.response_hook],
            },
            headers=headers,
            auth=BlockbaxAuth(token),
            base_url=httpx.URL(
                get_base_project_url(base_url=endpoint, project_id=project_id)
            ),
            timeout=httpx.Timeout(self.timeout_seconds),
            *args,
            **kwargs,
        )

    # Overwrite
    def request(self, *args: Any, **kwargs: Any) -> httpx.Response:
        try:
            return self.retryer(
                super(BlockbaxHTTPSession, self).request, *args, **kwargs
            )

        except TryAgain as exc:
            # Internally raised by the rate limit handler
            # If for some reason this fails after the amount of tries 'TryAgain' would be re-raised.
            raise RuntimeError(
                f"Unexpected error, retrying requests due to rate limiter failed after {self.tries} tries."
            ) from exc

    def __retry_error_callback(self, retry_state: RetryCallState) -> httpx.Response:
        retry_outcome = retry_state.outcome
        if retry_outcome is not None:
            return retry_outcome.result()
        raise RuntimeError(
            "Unexpected error, retry failed but the last outcome is 'None'. Expecting at least one "
            "outcome with a response."
        )

    def request_hook(self, request: httpx.Request):
        """Request hook is called right before the request is made"""

    def response_hook(self, response: httpx.Response):
        """Response hook is called right after a request has been made"""

        # Immediately raise error if the access token is not unauthorized
        api_utils.raise_for_unauthorized_error(response)

        # Force a retry if the status code is in the 'status_force_list'
        if response.status_code in self.status_force_list:
            raise TryAgain(response.text)

        # Handle rate limits retries
        api_utils.handle_rate_limiter(
            response, self.rate_limit_option, self._sleep_buffer
        )
        # Handles different HTTP error cases, either log errors or raises new Blockbax Errors
        client_error_codes = (
            [400, 402, 403] + list(range(405, 429)) + list(range(430, 500))
        )

        api_utils.raise_client_error(response, client_error_codes)
        server_error_codes = list(range(500, 600))
        api_utils.raise_server_error(response, server_error_codes)

        # Handles HTTP status codes that are not an error or not found
        api_utils.notify_partial_accepted(response)
        api_utils.notify_not_found(response)


class Api:
    # settings
    access_token: str
    project_id: str
    default_page_size: int = 200
    # endpoints
    property_types_endpoint: str = "propertyTypes"
    subject_types_endpoint: str = "subjectTypes"
    subjects_endpoint: str = "subjects"
    metrics_endpoint: str = "metrics"
    measurements_endpoint: str = "measurements"
    event_triggers_endpoint = "eventTriggers"
    events_endpoint = "events"

    def __init__(self, access_token: str, project_id: str, endpoint: str = None):
        self.access_token = access_token
        self.project_id = project_id
        self.endpoint = endpoint or BASE_URL

    def session(self) -> BlockbaxHTTPSession:
        return BlockbaxHTTPSession(self.access_token, self.project_id, self.endpoint)

    def get_user_agent(self) -> str:
        return BlockbaxHTTPSession.user_agent

    # http requests
    def get(
        self,
        endpoint: str = "",
        params: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        """get a single instance from the API using ID"""
        if params is None:
            params = {}
        params = {k: v for k, v in params.items() if v is not None}
        with self.session() as session:
            return api_utils.parse_response(session.get(url=endpoint, params=params))  # type: ignore

    def search(
        self, endpoint: str = "", params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """search multiple instances from the API using automatic paging, returns a list of results"""

        if not params:
            params = {}
        params = {k: v for k, v in params.items() if v is not None}
        params["size"] = self.default_page_size

        current_page_index = 0
        last_page_number = None
        results: List[Dict[str, Any]] = []
        done = False
        # while the previous page is not equal to the last page index get the current page index

        with self.session() as session:
            while not done:
                params["page"] = current_page_index
                response = api_utils.parse_response(
                    session.get(url=endpoint, params=params)
                )
                if response is None:
                    return results
                result = response.get("result")
                results.extend(result if result is not None else [])
                if response.get("count") is None:
                    return results  # return because we do not know when to stop

                if last_page_number is None:
                    last_page_number = math.ceil(
                        response["count"] / params["size"]
                    )  # page index starts from 0
                current_page_index += 1

                if current_page_index >= last_page_number:
                    done = True
        return results

    def post(self, endpoint: str, json: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        with self.session() as session:
            return api_utils.parse_response(  # type: ignore
                session.post(
                    url=endpoint,
                    json=json,
                )
            )

    def put(self, endpoint: str, json: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        with self.session() as session:
            return api_utils.parse_response(  # type: ignore
                session.put(
                    url=endpoint,
                    json=json,
                )
            )

    def delete(self, endpoint: str):
        with self.session() as session:
            session.delete(endpoint)

    # project

    def get_project(self) -> Optional[Dict[str, Any]]:
        return self.get(
            f"{BASE_URL}{DEFAULT_API_VERSION}{PROJECTS_ENDPOINT}{self.project_id}"
        )

    # property types

    def get_property_type(self, property_type_id: str) -> Optional[Dict[str, Any]]:
        return self.get(endpoint=f"{self.property_types_endpoint}/{property_type_id}")

    def get_property_types(
        self, name: Optional[str] = None, external_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        params = {"name": name, "externalId": external_id}
        return self.search(self.property_types_endpoint, params=params)

    def create_property_type(
        self,
        name: str,
        external_id: str,
        data_type: str,
        predefined_values: bool = False,
        values: Optional[List[Dict[str, Any]]] = None,
    ) -> Optional[Dict[str, Any]]:
        body = {
            "name": name,
            "externalId": external_id,
            "dataType": data_type,
            "predefinedValues": predefined_values,
            "values": values,
        }
        response = self.post(endpoint=self.property_types_endpoint, json=body)
        return response

    def update_property_type(
        self, property_type_id: str, json: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        response = self.put(
            endpoint=f"{self.property_types_endpoint}/{property_type_id}", json=json
        )
        return response

    def delete_property_type(self, property_type_id: str):
        self.delete(endpoint=f"{self.property_types_endpoint}/{property_type_id}")

    # subject types

    def get_subject_type(self, subject_type_id: str):
        return self.get(endpoint=f"{self.subject_types_endpoint}/{subject_type_id}")

    def get_subject_types(
        self,
        name: Optional[str] = None,
        property_type_ids: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        params = {"name": name, "propertyTypes": property_type_ids}
        return self.search(endpoint=f"{self.subject_types_endpoint}", params=params)

    def create_subject_type(
        self,
        name: str,
        parent_subject_type_ids: Optional[List[str]] = None,
        primary_location: Optional[Dict[str, Any]] = None,
        property_types: Optional[List[Dict[str, Any]]] = None,
    ) -> Optional[Dict[str, Any]]:
        body = {
            "name": name,
            "parentSubjectTypeIds": parent_subject_type_ids,
            "primaryLocation": primary_location,
            "propertyTypes": property_types,
        }
        response = self.post(endpoint=self.subject_types_endpoint, json=body)
        return response

    def update_subject_type(
        self,
        subject_type_id: str,
        json: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        return self.put(
            endpoint=f"{self.subject_types_endpoint}/{subject_type_id}", json=json
        )

    def delete_subject_type(self, subject_type_id: str):
        self.delete(endpoint=f"{self.subject_types_endpoint}/{subject_type_id}")

    # subjects

    def get_subject(self, subject_id: str) -> Optional[Dict[str, Any]]:
        return self.get(endpoint=f"{self.subjects_endpoint}/{subject_id}")

    def get_subjects(
        self,
        name: Optional[str] = None,
        subject_ids: Optional[List[str]] = None,
        subject_type_ids: Optional[List[Any]] = None,
        subject_ids_mode: Optional[str] = None,
        subject_external_id: Optional[str] = None,
        property_value_ids: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        return self.search(
            endpoint=self.subjects_endpoint,
            params={
                "name": name,
                "subjectIds": subject_ids,
                "subjectTypeIds": subject_type_ids,
                "subjectIdsMode": subject_ids_mode,
                "externalId": subject_external_id,
                "propertyValueIds": property_value_ids,
            },
        )

    def create_subject(
        self,
        name: str,
        subject_type_id: str,
        external_id: str,
        ingestion_ids: List[Any],
        parent_subject_id: Optional[str] = None,
        properties: Optional[List[Dict[str, Any]]] = None,
    ) -> Optional[Dict[str, Any]]:
        body = {
            "name": name,
            "subjectTypeId": subject_type_id,
            "parentSubjectId": parent_subject_id,
            "externalId": external_id,
            "ingestionIds": ingestion_ids,
            "properties": properties,
        }
        return self.post(endpoint=self.subjects_endpoint, json=body)

    def update_subject(
        self, subject_id: str, json: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        return self.put(
            endpoint=f"{self.subjects_endpoint}/{subject_id}",
            json=json,
        )

    def delete_subject(self, subject_id: str):
        self.delete(endpoint=f"{self.subjects_endpoint}/{subject_id}")

    # metrics

    def get_metric(self, metric_id: str) -> Optional[Dict[str, Any]]:
        return self.get(endpoint=f"{self.metrics_endpoint}/{metric_id}")

    def get_metrics(
        self,
        name: Optional[str] = None,
        subject_type_ids: Optional[List[str]] = None,
        metric_external_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        params = {
            "name": name,
            "subjectTypeIds": subject_type_ids,
            "externalId": metric_external_id,
        }
        return self.search(endpoint=self.metrics_endpoint, params=params)

    def create_metric(
        self,
        subject_type_id: str,
        name: str,
        data_type: str,
        type_: str,
        external_id: str,
        mapping_level: str,
        unit: Optional[str] = None,
        precision: Optional[int] = None,
        visible: Optional[bool] = None,
        discrete: Optional[bool] = None,
        preferred_color: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        body = {
            "name": name,
            "externalId": external_id,
            "subjectTypeId": subject_type_id,
            "dataType": data_type,
            "unit": unit,
            "preferredColor": preferred_color,
            "precision": precision,
            "visible": visible,
            "type": type_,
            "discrete": discrete,
            "mappingLevel": mapping_level,
        }
        response = self.post(endpoint=self.metrics_endpoint, json=body)
        return response

    def update_metric(
        self,
        metric_id: str,
        json: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        return self.put(endpoint=f"{self.metrics_endpoint}/{metric_id}", json=json)

    def delete_metric(self, metric_id: str):
        self.delete(endpoint=f"{self.metrics_endpoint}/{metric_id}")

    # measurements

    def get_measurements(
        self,
        subject_ids: Optional[List[str]] = None,
        metric_ids: Optional[List[str]] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        size: Optional[int] = None,
        order: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        # TODO is string join necessary?
        params = {
            "subjectIds": ",".join(subject_ids) if subject_ids is not None else None,
            "metricIds": ",".join(metric_ids) if metric_ids is not None else None,
            "fromDate": from_date,
            "toDate": to_date,
            "size": size,
            "order": order,
        }
        return self.get(endpoint=self.measurements_endpoint, params=params)

    def send_measurements(self, series: Dict[str, Any]):
        response = self.post(endpoint=self.measurements_endpoint, json=series)
        return response

    ## event triggers

    def get_event_trigger(self, event_trigger_id: str) -> Optional[Dict[str, Any]]:
        return self.get(endpoint=f"{self.event_triggers_endpoint}/{event_trigger_id}")

    def get_event_triggers(
        self,
        name: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        params = {
            "name": name,
        }
        return self.search(endpoint=self.event_triggers_endpoint, params=params)

    def create_event_trigger(
        self,
        name: str,
        subject_type_id: str,
        active: bool,
        evaluation_trigger: dict,
        evaluation_constraint: dict,
        event_rules: List[Dict[str, Any]],
        subject_filter: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        body = {
            "name": name,
            "subjectTypeId": subject_type_id,
            "active": active,
            "evaluationTrigger": evaluation_trigger,
            "evaluationConstraint": evaluation_constraint,
            "eventRules": event_rules,
            "subjectFilter": subject_filter,
        }
        return self.post(endpoint=self.event_triggers_endpoint, json=body)

    def update_event_trigger(
        self, event_trigger_id: str, json: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        return self.put(
            endpoint=f"{self.event_triggers_endpoint}/{event_trigger_id}", json=json
        )

    def delete_event_trigger(self, event_trigger_id: str):
        self.delete(endpoint=f"{self.event_triggers_endpoint}/{event_trigger_id}")

    # Events:
    def get_event(self, event_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single event by its ID.

        Args:
            event_id (str): The ID of the event.

        Returns:
            Optional[Dict[str, Any]]: The event data if found, else None.
        """
        return self.get(endpoint=f"{self.events_endpoint}/{event_id}")

    def get_events(
        self,
        active: Optional[bool] = None,
        suppressed: Optional[bool] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        only_new: Optional[bool] = None,
        property_value_ids: Optional[str] = None,
        subject_ids: Optional[str] = None,
        event_trigger_ids: Optional[str] = None,
        event_levels: Optional[str] = None,
        sort: Optional[str] = "startDate,desc",
    ) -> List[Dict[str, Any]]:
        """
        Get events based on various criteria.

        Args:
            active (Optional[bool]): True to fetch only active events.
            suppressed (Optional[bool]): True to only fetch events that are suppressed, False to only fetch events that are not suppressed.
            from_date (Optional[str]): Inclusive from date as ISO 8601 string with millisecond precision.
            to_date (Optional[str]): Exclusive end date as ISO 8601 string with millisecond precision.
            only_new (Optional[bool]): True to fetch only events occurred in the given date range.
            property_value_ids (Optional[str]): Filter on a list of property value IDs.
            subject_ids (Optional[str]): Comma-separated list of subject IDs.
            event_trigger_ids (Optional[str]): Comma-separated list of event trigger IDs.
            event_levels (Optional[str]): Comma-separated list of event levels.
            sort (Optional[str]): The sort order. Default is "startDate,desc".

        Returns:
            List[Dict[str, Any]]: A list of events matching the criteria.
        """
        params = {
            "active": active,
            "suppressed": suppressed,
            "fromDate": from_date,
            "toDate": to_date,
            "onlyNew": only_new,
            "propertyValueIds": property_value_ids,
            "subjectIds": subject_ids,
            "eventTriggerIds": event_trigger_ids,
            "eventLevels": event_levels,
            "sort": sort,
        }
        return self.search(endpoint=self.events_endpoint, params=params)
