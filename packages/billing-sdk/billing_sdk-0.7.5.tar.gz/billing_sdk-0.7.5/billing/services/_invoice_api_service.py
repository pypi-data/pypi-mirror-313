from typing import List

from typing_extensions import Unpack

from billing.services._billing_api_service import BillingAPIService
from billing.types import InvoiceListParams, InvoiceWithItemsBundle


class InvoiceAPIService(BillingAPIService):
    def retrieve(self, object_id: str) -> InvoiceWithItemsBundle:
        return self._request(
            "GET",
            f"v1/invoices/{object_id}/",
            data_model=InvoiceWithItemsBundle,
        )

    async def retrieve_async(self, object_id: str) -> InvoiceWithItemsBundle:
        return await self._request_async(
            "GET",
            f"v1/invoices/{object_id}/",
            data_model=InvoiceWithItemsBundle,
        )

    def list(
        self,
        page_number: int = 1,
        page_size: int = 50,
        **params: Unpack[InvoiceListParams],
    ) -> List[InvoiceWithItemsBundle]:
        return self._request(
            "GET",
            "v1/invoices/",
            params={
                "page": page_number,
                "page_size": page_size,
                **params,
            },
            data_model=InvoiceWithItemsBundle,
            batch_mode=True,
        )

    async def list_async(
        self,
        page_number: int = 1,
        page_size: int = 50,
        **params: Unpack[InvoiceListParams],
    ) -> List[InvoiceWithItemsBundle]:
        return await self._request_async(
            "GET",
            "v1/invoices/",
            params={
                "page": page_number,
                "page_size": page_size,
                **params,
            },
            data_model=InvoiceWithItemsBundle,
            batch_mode=True,
        )
