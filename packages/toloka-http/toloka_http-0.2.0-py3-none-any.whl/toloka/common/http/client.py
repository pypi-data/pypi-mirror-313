import asyncio
import logging
from functools import cache, partial
from typing import Any, Callable, Iterable, Literal, Mapping, Sequence, overload

from httpx import AsyncClient, AsyncHTTPTransport, HTTPStatusError, Response, TransportError
from tenacity import AsyncRetrying
from tenacity.before_sleep import before_sleep_log
from tenacity.retry import retry_if_exception, retry_if_exception_type
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_exponential_jitter
from typing_extensions import Self, Unpack

from toloka.common.http.args import BaseHttpClientNotRequiredArgs, apply_defaults
from toloka.common.http.auth import ApiKeyHeaders, AuthHeaders

logger = logging.getLogger(__name__)


def _is_specific_code_status_error(exc: Exception, code_predicate: Callable[[int], bool]) -> bool:
    if isinstance(exc, HTTPStatusError):
        return code_predicate(exc.response.status_code)
    return False


class BaseHttpClient:
    def __init__(
        self,
        base_url: str,
        auth_headers: AuthHeaders,
        **kwargs: Unpack[BaseHttpClientNotRequiredArgs],
    ) -> None:
        resolved_kwargs = apply_defaults(kwargs)
        self.base_url = base_url.rstrip('/')
        self.auth_headers = auth_headers
        self.connection_timeout = resolved_kwargs['timeout']
        self.transport_retries = resolved_kwargs['transport_retries']
        self.retry_count = resolved_kwargs['retry_count']
        self.retry_timeout_max = resolved_kwargs['retry_time_max']
        self.retry_timeout_jitter = resolved_kwargs['retry_time_jitter']
        self.is_status_retriable = resolved_kwargs['is_status_retriable']
        self.logging_level = resolved_kwargs['logging_level']
        self.use_http2 = resolved_kwargs['use_http2']

    @classmethod
    def from_api_key(
        cls,
        base_url: str,
        api_key: str,
        key_prefix: str = 'ApiKey',
        **kwargs: Unpack[BaseHttpClientNotRequiredArgs],
    ) -> Self:
        return cls(
            base_url=base_url,
            auth_headers=ApiKeyHeaders(api_key=api_key, key_prefix=key_prefix),
            **kwargs,
        )


HttpMethodWithBody = Literal['POST', 'PUT', 'PATCH', 'SEARCH']
HttpMethodWithoutBody = Literal['GET', 'DELETE']
HttpMethod = Literal[HttpMethodWithBody, HttpMethodWithoutBody]

QueryParam = Mapping[str, bool | int | str | float | None | Sequence[bool | int | str | float | None]]


class AsyncHttpClient(BaseHttpClient):
    def __init__(
        self,
        base_url: str,
        auth_headers: AuthHeaders,
        **kwargs: Unpack[BaseHttpClientNotRequiredArgs],
    ) -> None:
        super().__init__(base_url=base_url, auth_headers=auth_headers, **kwargs)
        self.get_client = cache(self._get_client)

    def _get_client(self, event_loop_id: int) -> AsyncClient:
        return AsyncClient(
            base_url=self.base_url,
            timeout=self.connection_timeout,
            transport=AsyncHTTPTransport(retries=self.transport_retries, http2=self.use_http2),
        )

    @property
    def client(self) -> AsyncClient:
        try:
            event_loop = asyncio.get_event_loop()
        except RuntimeError:
            event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(event_loop)

        return self.get_client(event_loop_id=id(event_loop))

    @overload
    async def make_request(
        self,
        method: HttpMethodWithBody,
        url: str,
        body: Mapping[str, Any] | Iterable[Mapping[str, Any]] | None,
        params: QueryParam | None = None,
    ) -> Response: ...

    @overload
    async def make_request(
        self,
        method: HttpMethodWithoutBody,
        url: str,
        body: None = None,
        params: QueryParam | None = None,
    ) -> Response: ...

    async def make_request(
        self,
        method: HttpMethod,
        url: str,
        body: Mapping[str, Any] | Iterable[Mapping[str, Any]] | None = None,
        params: QueryParam | None = None,
    ) -> Response:
        response = await self.client.request(
            method=method,
            url=url,
            json=body,
            headers=self.auth_headers.get_headers(),
            params=params,
        )
        response.raise_for_status()
        return response

    @overload
    async def make_retriable_request(
        self,
        method: HttpMethodWithBody,
        url: str,
        body: Mapping[str, Any] | Iterable[Mapping[str, Any]] | None,
        params: QueryParam | None = None,
        is_status_retriable: Callable[[int], bool] | None = None,
    ) -> Response: ...

    @overload
    async def make_retriable_request(
        self,
        method: HttpMethodWithoutBody,
        url: str,
        body: None = None,
        params: QueryParam | None = None,
        is_status_retriable: Callable[[int], bool] | None = None,
    ) -> Response: ...

    async def make_retriable_request(
        self,
        method: HttpMethod,
        url: str,
        body: Mapping[str, Any] | Iterable[Mapping[str, Any]] | None = None,
        params: QueryParam | None = None,
        is_status_retriable: Callable[[int], bool] | None = None,
    ) -> Response:
        is_response_retriable = retry_if_exception(
            partial(
                _is_specific_code_status_error,
                code_predicate=is_status_retriable or self.is_status_retriable,
            )
        )

        async for attempt in AsyncRetrying(
            wait=wait_exponential_jitter(
                max=self.retry_timeout_max,
                jitter=self.retry_timeout_jitter,
            ),
            stop=stop_after_attempt(max_attempt_number=self.retry_count),
            retry=is_response_retriable | retry_if_exception_type(TransportError),
            reraise=True,
            before_sleep=before_sleep_log(
                logger=logger,
                log_level=self.logging_level,
                exc_info=True,
            ),
        ):
            with attempt:
                if method == 'GET' or method == 'DELETE':
                    response = await self.make_request(
                        method=method,
                        url=url,
                        params=params,
                    )
                else:
                    response = await self.make_request(
                        method=method,
                        url=url,
                        body=body,
                        params=params,
                    )
            if attempt.retry_state.outcome is not None and not attempt.retry_state.outcome.failed:
                attempt.retry_state.set_result(response)
        return response
