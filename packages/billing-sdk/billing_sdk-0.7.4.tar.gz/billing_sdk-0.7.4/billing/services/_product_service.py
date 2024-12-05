from typing import List

from typing_extensions import Unpack

from billing.services._billing_api_service import BillingAPIService
from billing.types import ProductDetailParams, ProductListParams, ProductWithPlansAndImagesBundle


class ProductAPIService(BillingAPIService):
    def retrieve(
        self,
        object_id: str,
        **params: Unpack[ProductDetailParams],
    ) -> ProductWithPlansAndImagesBundle:
        return self._request(
            "GET",
            f"v1/products/{object_id}/",
            params=params,
            data_model=ProductWithPlansAndImagesBundle,
        )

    async def retrieve_async(
        self,
        object_id: str,
        **params: Unpack[ProductDetailParams],
    ) -> ProductWithPlansAndImagesBundle:
        return await self._request_async(
            "GET",
            f"v1/products/{object_id}/",
            params=params,
            data_model=ProductWithPlansAndImagesBundle,
        )

    def list(
        self,
        page_number: int = 1,
        page_size: int = 50,
        **params: Unpack[ProductListParams],
    ) -> List[ProductWithPlansAndImagesBundle]:
        return self._request(
            "GET",
            "v1/products/",
            params={
                "page": page_number,
                "page_size": page_size,
                **params,
            },
            data_model=ProductWithPlansAndImagesBundle,
            batch_mode=True,
        )

    async def list_async(
        self,
        page_number: int = 1,
        page_size: int = 50,
        **params: Unpack[ProductListParams],
    ) -> List[ProductWithPlansAndImagesBundle]:
        return await self._request_async(
            "GET",
            "v1/products/",
            params={
                "page": page_number,
                "page_size": page_size,
                **params,
            },
            data_model=ProductWithPlansAndImagesBundle,
            batch_mode=True,
        )
