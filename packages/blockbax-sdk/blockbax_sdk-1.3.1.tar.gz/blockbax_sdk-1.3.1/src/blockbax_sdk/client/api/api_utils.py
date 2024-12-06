from typing import Any, Dict, List, Optional

import datetime
import logging
import enum
import json
import decimal

import httpx
from tenacity import TryAgain, nap

from ...errors import (
    RateLimitError,
    BlockbaxHTTPError,
    BlockbaxClientError,
    BlockbaxServerError,
    BlockbaxUnauthorizedError,
)

logger = logging.getLogger(__name__)


class RateLimitOption(str, enum.Enum):
    SLEEP = enum.auto()
    THROW = enum.auto()


def handle_rate_limiter(
    response: httpx.Response, rate_limit_option: RateLimitOption, sleep_buffer: int = 1
):
    rate_limit_header_keys = [
        "x-ratelimit-limit",
        "x-ratelimit-remaining",
        "x-ratelimit-reset",
    ]
    header_keys = response.headers.keys()
    if not all(
        rate_limit_key in header_keys for rate_limit_key in rate_limit_header_keys
    ):
        return

    limit: int = int(response.headers.get("x-ratelimit-limit"))
    remaining: int = int(response.headers.get("x-ratelimit-remaining"))
    reset: int = response.headers.get("x-ratelimit-reset")
    if reset is None:
        reset = 60
    else:
        reset = int(reset)
    if response.status_code == httpx.codes.TOO_MANY_REQUESTS:
        if rate_limit_option == RateLimitOption.THROW:
            raise RateLimitError(
                limit=limit,
                remaining=remaining,
                reset_time_remaining=datetime.timedelta(seconds=int(reset)),
            )
        elif rate_limit_option == RateLimitOption.SLEEP:
            waiting_time = reset + sleep_buffer
            print(
                f"Request throttled, waiting for '{waiting_time}' seconds, (hit the rate limit of '{limit}' requests per minute)"
            )
            nap.sleep(waiting_time)

            if response.is_error:
                raise TryAgain(f"{response.text}")


def parse_response(response: httpx.Response) -> Optional[Dict[str, Any]]:
    response.read()
    if response.status_code == httpx.codes.NOT_FOUND or not response.text:
        return None
    try:
        return json.loads(response.text)
    except Exception as exc:
        raise BlockbaxHTTPError(
            f"Could not parse response: {exc}, received status code: {response.status_code}",
            response=response,
        ) from exc


def notify_partial_accepted(r: httpx.Response):
    # when sending measurements ingestion ID('s) could be rejected.
    # API returns a 207 with a message telling the user which ingestion ID('s) are not accepted.
    if (
        r.status_code == httpx.codes.MULTI_STATUS
        or r.status_code == httpx.codes.PARTIAL_CONTENT
    ):
        r.read()
        logger.warning("%s", json.loads(r.text)["message"])


def notify_not_found(r: httpx.Response):
    if r.status_code == httpx.codes.NOT_FOUND:
        r.read()
        response_message = f", response message: {r.text}" if r.text else ""
        logger.warning(
            "Request with Url: %s, was not found! %s", r.request.url, response_message
        )


def raise_client_error(r: httpx.Response, response_codes: List[int]):
    try:
        r.raise_for_status()
    except httpx.HTTPError as http_error:
        if r.status_code in response_codes:
            r.read()
            response_message = f", response: {r.text}" if r.text else ""
            error_message_4xx = f"HTTP Error: {http_error}{response_message}"
            logger.error(error_message_4xx)
            raise BlockbaxClientError(error_message_4xx, response=r) from http_error


def raise_server_error(r: httpx.Response, response_codes: List[int]):
    try:
        r.raise_for_status()
    except httpx.HTTPError as http_error:
        if r.status_code in response_codes:
            # with a 5xx there is no pint in trying to access the response content
            error_message_5xx = f"HTTP Error: {http_error}"
            logger.error(error_message_5xx)
            raise BlockbaxServerError(error_message_5xx, response=r) from http_error


def raise_for_unauthorized_error(r: httpx.Response):
    """checks authorization for access token and project ID raises if status code is 401"""
    try:
        r.raise_for_status()
    except httpx.HTTPError as http_error:
        if r.status_code == httpx.codes.UNAUTHORIZED:
            if "Authorization" not in r.request.headers:
                suffix_error_message = (
                    ", 'Authorization' header is missing. "  # not likely
                )
            else:
                suffix_error_message = (
                    ", the access token is unauthorized. "  # unauthorized access token
                )
            error_message = f"HTTP error: {http_error}" + (
                suffix_error_message
                if suffix_error_message
                else ", Unknown unauthorized error."
            )
            raise BlockbaxUnauthorizedError(error_message, response=r) from http_error


class JSONEncoderWithDecimal(json.JSONEncoder):
    def default(self, o: object):
        if isinstance(o, decimal.Decimal):
            return "{:f}".format(o)
        return json.JSONEncoder.default(self, o)
