import datetime
import httpx


class BlockbaxError(Exception):
    pass


class ValidationError(BlockbaxError):
    pass


# API Errors


class BlockbaxHTTPError(BlockbaxError):
    response: httpx.Response

    def __init__(self, *args: object, response: httpx.Response) -> None:
        super().__init__(
            *args,
        )
        self.response = response


class BlockbaxUnauthorizedError(BlockbaxHTTPError):
    pass


class BlockbaxClientError(BlockbaxHTTPError):
    pass


class BlockbaxServerError(BlockbaxHTTPError):
    pass


class RateLimitError(BlockbaxHTTPError):
    limit: float
    remaining: float
    reset_time_remaining: datetime.timedelta

    def __init__(
        self,
        limit: float,
        remaining: float,
        reset_time_remaining: datetime.timedelta,
    ) -> None:
        self.limit = limit
        self.remaining = remaining
        self.reset_time_remaining = reset_time_remaining

    def __str__(self) -> str:
        return f"Rate limit reached, remaining request: {self.remaining}, time left for reset: {self.reset_time_remaining}"
