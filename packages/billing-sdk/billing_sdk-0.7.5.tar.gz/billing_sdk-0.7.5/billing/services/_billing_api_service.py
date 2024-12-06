from __future__ import annotations

from typing import Any, Literal, Mapping, TypeVar, overload

from httpx import Response

from billing._http_client import HTTPClient
from billing.types import BillingObject, HTTPMethod

_APIObject = TypeVar("_APIObject", bound=BillingObject)


class BillingAPIService:
    def __init__(self, http_client: HTTPClient) -> None:
        self._http_client = http_client

    @overload
    def _request(
        self,
        method: HTTPMethod,
        url: str,
        *,
        json: Any | None = None,
        params: Mapping[str, Any] | None = None,
        data_model: None = None,
        batch_mode: Literal[False] = False,
    ) -> None: ...

    @overload
    def _request(
        self,
        method: HTTPMethod,
        url: str,
        *,
        json: Any | None = None,
        params: Mapping[str, Any] | None = None,
        data_model: type[_APIObject],
        batch_mode: Literal[False] = False,
    ) -> _APIObject: ...

    @overload
    def _request(
        self,
        method: HTTPMethod,
        url: str,
        *,
        json: Any | None = None,
        params: Mapping[str, Any] | None = None,
        data_model: type[_APIObject],
        batch_mode: Literal[True],
    ) -> list[_APIObject]: ...

    def _request(
        self,
        method: HTTPMethod,
        url: str,
        *,
        json: Any | None = None,
        params: Mapping[str, Any] | None = None,
        data_model: type[_APIObject] | None = None,
        batch_mode: bool = False,
    ) -> _APIObject | list[_APIObject] | None:
        response = self._http_client.request_with_retries(
            method,
            url,
            json=json,
            params=params,
        )

        if data_model is None:
            return None

        return self._convert_response_to_entity(
            data_model=data_model,
            batch_mode=batch_mode,
            response=response,
        )

    @overload
    async def _request_async(
        self,
        method: HTTPMethod,
        url: str,
        *,
        json: Any | None = None,
        params: Mapping[str, Any] | None = None,
        data_model: None = None,
        batch_mode: Literal[False] = False,
    ) -> None: ...

    @overload
    async def _request_async(
        self,
        method: HTTPMethod,
        url: str,
        *,
        json: Any | None = None,
        params: Mapping[str, Any] | None = None,
        data_model: type[_APIObject],
        batch_mode: Literal[False] = False,
    ) -> _APIObject: ...

    @overload
    async def _request_async(
        self,
        method: HTTPMethod,
        url: str,
        *,
        json: Any | None = None,
        params: Mapping[str, Any] | None = None,
        data_model: type[_APIObject],
        batch_mode: Literal[True],
    ) -> list[_APIObject]: ...

    async def _request_async(
        self,
        method: HTTPMethod,
        url: str,
        *,
        json: Any | None = None,
        params: Mapping[str, Any] | None = None,
        data_model: type[_APIObject] | None = None,
        batch_mode: bool = False,
    ) -> _APIObject | list[_APIObject] | None:
        response = await self._http_client.request_async_with_retries(
            method,
            url,
            json=json,
            params=params,
        )

        if data_model is None:
            return None

        return self._convert_response_to_entity(
            data_model=data_model,
            batch_mode=batch_mode,
            response=response,
        )

    @staticmethod
    def _convert_response_to_entity(
        *,
        data_model: type[_APIObject],
        batch_mode: bool = False,
        response: Response,
    ) -> _APIObject | list[_APIObject]:
        response_json = response.json()

        if not batch_mode:
            return data_model.parse(response_json)

        if isinstance(response_json, list):
            objects_from_response = response_json
        elif "items" in response_json:
            objects_from_response = response_json["items"]
        else:
            raise ValueError(f"Unexpected response format: {response_json!r}")

        return [data_model.parse(obj) for obj in objects_from_response]
