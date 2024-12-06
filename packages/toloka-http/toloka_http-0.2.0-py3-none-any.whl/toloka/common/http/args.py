from typing import Callable, TypedDict

from typing_extensions import NotRequired

from toloka.common.http.defaults import (
    DEFAULT_LOGGING_LEVEL,
    DEFAULT_RETRY_COUNT,
    DEFAULT_RETRY_TIME_JITTER,
    DEFAULT_RETRY_TIME_MAX,
    DEFAULT_TIMEOUT,
    DEFAULT_TRANSPORT_RETRIES,
    DEFAULT_USE_HTTP2,
    _is_5xx,
)


class BaseHttpClientNotRequiredArgs(TypedDict):
    timeout: NotRequired[float]
    transport_retries: NotRequired[int]
    retry_count: NotRequired[int]
    retry_time_max: NotRequired[float]
    retry_time_jitter: NotRequired[float]
    is_status_retriable: NotRequired[Callable[[int], bool]]
    logging_level: NotRequired[int]
    use_http2: NotRequired[bool]


class BaseHttpClientDefaults(TypedDict):
    timeout: float
    transport_retries: int
    retry_count: int
    retry_time_max: float
    retry_time_jitter: float
    is_status_retriable: Callable[[int], bool]
    logging_level: int
    use_http2: bool


def apply_defaults(kwargs: BaseHttpClientNotRequiredArgs) -> BaseHttpClientDefaults:
    return {
        'timeout': DEFAULT_TIMEOUT,
        'transport_retries': DEFAULT_TRANSPORT_RETRIES,
        'retry_count': DEFAULT_RETRY_COUNT,
        'retry_time_max': DEFAULT_RETRY_TIME_MAX,
        'retry_time_jitter': DEFAULT_RETRY_TIME_JITTER,
        'is_status_retriable': _is_5xx,
        'logging_level': DEFAULT_LOGGING_LEVEL,
        'use_http2': DEFAULT_USE_HTTP2,
        **kwargs,
    }
