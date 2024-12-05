from typing import List

from typing_extensions import Unpack

from billing.services._billing_api_service import BillingAPIService
from billing.types import Customer, CustomerCreatePayload, CustomerListParams


class CustomerAPIService(BillingAPIService):
    def retrieve(self, object_id: str) -> Customer:
        return self._request(
            "GET",
            f"v1/customers/{object_id}/",
            data_model=Customer,
        )

    async def retrieve_async(self, object_id: str) -> Customer:
        return await self._request_async(
            "GET",
            f"v1/customers/{object_id}/",
            data_model=Customer,
        )

    def list(
        self,
        page_number: int = 1,
        page_size: int = 50,
        **params: Unpack[CustomerListParams],
    ) -> List[Customer]:
        return self._request(
            "GET",
            "v1/customers/",
            params={
                "page": page_number,
                "page_size": page_size,
                **params,
            },
            data_model=Customer,
            batch_mode=True,
        )

    async def list_async(
        self,
        page_number: int = 1,
        page_size: int = 50,
        **params: Unpack[CustomerListParams],
    ) -> List[Customer]:
        return await self._request_async(
            "GET",
            "v1/customers/",
            params={
                "page": page_number,
                "page_size": page_size,
                **params,
            },
            data_model=Customer,
            batch_mode=True,
        )

    def create(self, **payload: Unpack[CustomerCreatePayload]) -> Customer:
        return self._request(
            "POST",
            "v1/customers/",
            json=payload,
            data_model=Customer,
        )

    async def create_async(self, **payload: Unpack[CustomerCreatePayload]) -> Customer:
        return await self._request_async(
            "POST",
            "v1/customers/",
            json=payload,
            data_model=Customer,
        )
