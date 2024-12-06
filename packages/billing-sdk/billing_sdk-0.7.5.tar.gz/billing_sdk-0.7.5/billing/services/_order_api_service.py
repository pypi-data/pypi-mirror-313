from typing import List

from typing_extensions import Unpack

from billing.services._billing_api_service import BillingAPIService
from billing.types import OrderCreatePayload, OrderListParams, OrderOffersBundle, OrderWithOffersAndInvoicesBundle


class OrderAPIService(BillingAPIService):
    def retrieve(self, object_id: str) -> OrderOffersBundle:
        return self._request(
            "GET",
            f"v1/orders/{object_id}/",
            data_model=OrderOffersBundle,
        )

    async def retrieve_async(self, object_id: str) -> OrderOffersBundle:
        return await self._request_async(
            "GET",
            f"v1/orders/{object_id}/",
            data_model=OrderOffersBundle,
        )

    def list(
        self,
        page_number: int = 1,
        page_size: int = 50,
        **params: Unpack[OrderListParams],
    ) -> List[OrderOffersBundle]:
        return self._request(
            "GET",
            "v1/orders/",
            params={
                "page": page_number,
                "page_size": page_size,
                **params,
            },
            data_model=OrderOffersBundle,
            batch_mode=True,
        )

    async def list_async(
        self,
        page_number: int = 1,
        page_size: int = 50,
        **params: Unpack[OrderListParams],
    ) -> List[OrderOffersBundle]:
        return await self._request_async(
            "GET",
            "v1/orders/",
            params={
                "page": page_number,
                "page_size": page_size,
                **params,
            },
            data_model=OrderOffersBundle,
            batch_mode=True,
        )

    def create(self, **payload: Unpack[OrderCreatePayload]) -> OrderWithOffersAndInvoicesBundle:
        return self._request(
            "POST",
            "v1/orders/",
            json=payload,
            data_model=OrderWithOffersAndInvoicesBundle,
        )

    async def create_async(self, **payload: Unpack[OrderCreatePayload]) -> OrderWithOffersAndInvoicesBundle:
        return await self._request_async(
            "POST",
            "v1/orders/",
            json=payload,
            data_model=OrderWithOffersAndInvoicesBundle,
        )
