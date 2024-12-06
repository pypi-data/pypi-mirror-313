import asyncio
import random
import time
from typing import Any, Dict, Optional, Union
from urllib.parse import urljoin

from httpx import USE_CLIENT_DEFAULT, AsyncClient, Client, Response
from httpx._client import UseClientDefault
from httpx._types import (
    AuthTypes,
    CookieTypes,
    QueryParamTypes,
    RequestContent,
    RequestData,
    RequestFiles,
    TimeoutTypes,
)
from typing_extensions import Unpack

from billing._constants import FEATURE_USAGE_LIMIT_EXCEEDED_ERROR_CODE
from billing._exceptions import AuthenticationError, BillingAPIError, FeatureUsageLimitExceededError, RateLimitError
from billing.types import HTTPXPayload
from billing.types._billing_entity import DynamicDictModel


class HTTPClient:
    MAX_DELAY_WITHOUT_JITTER = 2
    INITIAL_DELAY = 0.5

    def __init__(
        self,
        terminal_secret_key: str,
        terminal_id: str,
        base_url: str,
        max_network_retries: int = 0,
        setup_sync_client: bool = False,
        setup_async_client: bool = True,
        sync_client: Optional[Client] = None,
        async_client: Optional[AsyncClient] = None,
        **httpx_client_kwargs: Unpack[HTTPXPayload],
    ) -> None:
        if not setup_sync_client and sync_client:
            raise ValueError("Cannot set both `setup_sync_client=False` and `sync_client`.")
        if not setup_async_client and async_client:
            raise ValueError("Cannot set both `setup_async_client=False` and `async_client`.")
        if not setup_sync_client and not setup_async_client:
            raise ValueError("Either `setup_sync_client=True` or `setup_async_client=True` must be set.")

        self._base_url = base_url

        self._max_network_retries = max_network_retries

        self._auth_headers = {
            "Authorization": f"Bearer {terminal_secret_key}",
            "X-Terminal-Id": terminal_id,
        }

        if setup_sync_client:
            self._sync_client = sync_client or Client(**httpx_client_kwargs)
        if setup_async_client:
            self._async_client = async_client or AsyncClient(**httpx_client_kwargs)

    def request_with_retries(
        self,
        method: str,
        url: str,
        *,
        content: Optional[RequestContent] = None,
        data: Optional[RequestData] = None,
        files: Optional[RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[QueryParamTypes] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[CookieTypes] = None,
        auth: Union[AuthTypes, UseClientDefault, None] = USE_CLIENT_DEFAULT,
        follow_redirects: Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
        timeout: Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
    ) -> Response:
        attempt_number = 1
        while True:
            try:
                return self._request(
                    method,
                    url,
                    content=content,
                    data=data,
                    files=files,
                    json=json,
                    params=params,
                    headers=headers,
                    cookies=cookies,
                    auth=auth,
                    follow_redirects=follow_redirects,
                    timeout=timeout,
                )
            except BillingAPIError as e:
                if self._is_should_retry(e, attempt_number=attempt_number):
                    time.sleep(self._compute_sleep_seconds(attempt_number))
                else:
                    raise

            attempt_number += 1

    def _request(
        self,
        method: str,
        url: str,
        *,
        content: Optional[RequestContent] = None,
        data: Optional[RequestData] = None,
        files: Optional[RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[QueryParamTypes] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[CookieTypes] = None,
        auth: Union[AuthTypes, UseClientDefault, None] = USE_CLIENT_DEFAULT,
        follow_redirects: Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
        timeout: Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
    ) -> Response:
        if not self._sync_client:
            raise RuntimeError("Sync client is not set.")

        if isinstance(data, dict):
            data = DynamicDictModel.init(data).dump(mode="json")
        if isinstance(json, dict):
            json = DynamicDictModel.init(json).dump(mode="json")
        if isinstance(params, dict):
            params = DynamicDictModel.init(params).dump(mode="json")

        if headers is None:
            headers = {}
        headers.update(self._auth_headers)

        response = self._sync_client.request(
            method,
            self._construct_url(url),
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
        )

        self._handle_api_error_if_any(response)
        return response

    async def request_async_with_retries(
        self,
        method: str,
        url: str,
        *,
        content: Optional[RequestContent] = None,
        data: Optional[RequestData] = None,
        files: Optional[RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[QueryParamTypes] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[CookieTypes] = None,
        auth: Union[AuthTypes, UseClientDefault, None] = USE_CLIENT_DEFAULT,
        follow_redirects: Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
        timeout: Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
    ) -> Response:

        attempt_number = 1
        while True:
            try:
                return await self._request_async(
                    method,
                    url,
                    content=content,
                    data=data,
                    files=files,
                    json=json,
                    params=params,
                    headers=headers,
                    cookies=cookies,
                    auth=auth,
                    follow_redirects=follow_redirects,
                    timeout=timeout,
                )
            except BillingAPIError as e:
                if self._is_should_retry(e, attempt_number=attempt_number):
                    await asyncio.sleep(self._compute_sleep_seconds(attempt_number))
                else:
                    raise

            attempt_number += 1

    async def _request_async(
        self,
        method: str,
        url: str,
        *,
        content: Optional[RequestContent] = None,
        data: Optional[RequestData] = None,
        files: Optional[RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[QueryParamTypes] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[CookieTypes] = None,
        auth: Union[AuthTypes, UseClientDefault, None] = USE_CLIENT_DEFAULT,
        follow_redirects: Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
        timeout: Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
    ) -> Response:
        if not self._async_client:
            raise RuntimeError("Async client is not set.")

        if isinstance(data, dict):
            data = DynamicDictModel.init(data).dump(mode="json")
        if isinstance(json, dict):
            json = DynamicDictModel.init(json).dump(mode="json")
        if isinstance(params, dict):
            params = DynamicDictModel.init(params).dump(mode="json")

        if headers is None:
            headers = {}
        headers.update(self._auth_headers)

        response = await self._async_client.request(
            method,
            self._construct_url(url),
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
        )

        self._handle_api_error_if_any(response)
        return response

    def _construct_url(self, path: str) -> str:
        return urljoin(self._base_url, path)

    @staticmethod
    def _handle_api_error_if_any(response: Response) -> None:
        if 200 <= response.status_code < 300:
            return

        if response.status_code in (401, 403):
            raise AuthenticationError(
                status_code=response.status_code,
                response_text=response.text,
            )
        elif response.status_code == 429:
            if FEATURE_USAGE_LIMIT_EXCEEDED_ERROR_CODE in response.text:
                raise FeatureUsageLimitExceededError(
                    status_code=response.status_code,
                    response_text=response.text,
                )

            raise RateLimitError(
                status_code=response.status_code,
                response_text=response.text,
            )

        else:
            raise BillingAPIError(
                status_code=response.status_code,
                response_text=response.text,
            )

    def _is_should_retry(
        self,
        api_error: BillingAPIError,
        attempt_number: int,
    ) -> bool:
        """
        Should retry on conflict, rate limit or server error.
        """

        if attempt_number >= self._max_network_retries + 1:
            return False

        # Should not retry on feature usage limit exceeded error
        if isinstance(api_error, FeatureUsageLimitExceededError):
            return False

        return api_error.status_code in (409, 429) or api_error.status_code >= 500

    @classmethod
    def _compute_sleep_seconds(cls, attempt_number: int) -> float:
        sleep_seconds = min(
            cls.INITIAL_DELAY * (2 ** (attempt_number - 1)),
            cls.MAX_DELAY_WITHOUT_JITTER,
        )

        # Add jitter to the sleep seconds.
        sleep_seconds += random.uniform(0, 1)

        return sleep_seconds  # type: ignore[no-any-return]

    def close_sync_client(self) -> None:
        if self._sync_client:
            self._sync_client.close()

    async def close_async_client(self) -> None:
        if self._async_client:
            await self._async_client.aclose()
