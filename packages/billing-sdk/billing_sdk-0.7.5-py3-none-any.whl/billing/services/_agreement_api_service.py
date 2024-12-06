from typing import List

from typing_extensions import Unpack

from billing.services._billing_api_service import BillingAPIService
from billing.types import Agreement, AgreementListParams, AgreementWithTerms


class AgreementAPIService(BillingAPIService):
    def retrieve(self, object_id: str) -> AgreementWithTerms:
        return self._request(
            "GET",
            f"v1/agreements/{object_id}/",
            data_model=AgreementWithTerms,
        )

    async def retrieve_async(self, object_id: str) -> AgreementWithTerms:
        return await self._request_async(
            "GET",
            f"v1/agreements/{object_id}/",
            data_model=AgreementWithTerms,
        )

    def list(
        self,
        page_number: int = 1,
        page_size: int = 50,
        **params: Unpack[AgreementListParams],
    ) -> List[Agreement]:
        return self._request(
            "GET",
            "v1/agreements/",
            params={
                "page": page_number,
                "page_size": page_size,
                **params,
            },
            data_model=Agreement,
            batch_mode=True,
        )

    async def list_async(
        self,
        page_number: int = 1,
        page_size: int = 50,
        **params: Unpack[AgreementListParams],
    ) -> List[Agreement]:
        return await self._request_async(
            "GET",
            "v1/agreements/",
            params={
                "page": page_number,
                "page_size": page_size,
                **params,
            },
            data_model=Agreement,
            batch_mode=True,
        )
