from typing import List

from typing_extensions import Unpack

from billing.services._billing_api_service import BillingAPIService
from billing.types import Offer, OfferCancelPayload, OfferCustomerProductsBundle, OfferListParams


class OfferAPIService(BillingAPIService):
    def retrieve(self, object_id: str) -> OfferCustomerProductsBundle:
        return self._request(
            "GET",
            f"v1/offers/{object_id}/",
            data_model=OfferCustomerProductsBundle,
        )

    async def retrieve_async(self, object_id: str) -> OfferCustomerProductsBundle:
        return await self._request_async(
            "GET",
            f"v1/offers/{object_id}/",
            data_model=OfferCustomerProductsBundle,
        )

    def list(
        self,
        page_number: int = 1,
        page_size: int = 50,
        **params: Unpack[OfferListParams],
    ) -> List[Offer]:
        return self._request(
            "GET",
            "v1/offers/",
            params={
                "page": page_number,
                "page_size": page_size,
                **params,
            },
            data_model=Offer,
            batch_mode=True,
        )

    async def list_async(
        self,
        page_number: int = 1,
        page_size: int = 50,
        **params: Unpack[OfferListParams],
    ) -> List[Offer]:
        return await self._request_async(
            "GET",
            "v1/offers/",
            params={
                "page": page_number,
                "page_size": page_size,
                **params,
            },
            data_model=Offer,
            batch_mode=True,
        )

    def cancel(
        self,
        object_id: str,
        **payload: Unpack[OfferCancelPayload],
    ) -> None:
        return self._request(
            "POST",
            f"v1/offers/{object_id}/cancel/",
            json=payload,
        )

    async def cancel_async(
        self,
        object_id: str,
        **payload: Unpack[OfferCancelPayload],
    ) -> None:
        return await self._request_async(
            "POST",
            f"v1/offers/{object_id}/cancel/",
            json=payload,
        )
