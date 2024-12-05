import contextlib
import uuid
from typing import AsyncGenerator, Generator, List

from typing_extensions import Unpack

from billing.services._billing_api_service import BillingAPIService
from billing.types import FeatureRecordPayload, FeatureUsageEvent, FeatureUsageSummary


class FeatureAPIService(BillingAPIService):
    def retrieve_usage_summary(
        self,
        codename: str,
        user_id: uuid.UUID,
    ) -> FeatureUsageSummary:
        return self._request(
            "GET",
            f"v1/features/{codename}/usage/summary/",
            params={"user_id": user_id},
            data_model=FeatureUsageSummary,
        )

    async def retrieve_usage_summary_async(
        self,
        codename: str,
        user_id: uuid.UUID,
    ) -> FeatureUsageSummary:
        return await self._request_async(
            "GET",
            f"v1/features/{codename}/usage/summary/",
            params={"user_id": user_id},
            data_model=FeatureUsageSummary,
        )

    def list_usage_summary(
        self,
        user_id: uuid.UUID,
        page_number: int = 1,
        page_size: int = 50,
    ) -> List[FeatureUsageSummary]:
        return self._request(
            "GET",
            "v1/features/usage/summary/",
            params={
                "page": page_number,
                "page_size": page_size,
                "user_id": user_id,
            },
            data_model=FeatureUsageSummary,
            batch_mode=True,
        )

    async def list_usage_summary_async(
        self,
        user_id: uuid.UUID,
        page_number: int = 1,
        page_size: int = 50,
    ) -> List[FeatureUsageSummary]:
        return await self._request_async(
            "GET",
            "v1/features/usage/summary/",
            params={
                "page": page_number,
                "page_size": page_size,
                "user_id": user_id,
            },
            data_model=FeatureUsageSummary,
            batch_mode=True,
        )

    def record_usage(
        self,
        codename: str,
        **payload: Unpack[FeatureRecordPayload],
    ) -> FeatureUsageEvent:
        return self._request(
            "POST",
            f"v1/features/{codename}/usage/record/",
            json=payload,
            data_model=FeatureUsageEvent,
        )

    async def record_usage_async(
        self,
        codename: str,
        **payload: Unpack[FeatureRecordPayload],
    ) -> FeatureUsageEvent:
        return await self._request_async(
            "POST",
            f"v1/features/{codename}/usage/record/",
            json=payload,
            data_model=FeatureUsageEvent,
        )

    def refund_usage(self, feature_usage_event_id: str) -> FeatureUsageEvent:
        return self._request(
            "POST",
            f"v1/features/usage/{feature_usage_event_id}/refund/",
            data_model=FeatureUsageEvent,
        )

    async def refund_usage_async(self, feature_usage_event_id: str) -> FeatureUsageEvent:
        return await self._request_async(
            "POST",
            f"v1/features/usage/{feature_usage_event_id}/refund/",
            data_model=FeatureUsageEvent,
        )

    @contextlib.contextmanager
    def safely_record_usage(
        self,
        codename: str,
        **payload: Unpack[FeatureRecordPayload],
    ) -> Generator[FeatureUsageEvent, None, None]:
        """
        Safely record usage of a feature.

        If an exception is raised inside the context manager, the usage will be
        refunded.

        It is generally recommended to use `safely_record_usage` over `record_usage`
        to avoid inconsistent results.
        """
        event = self.record_usage(codename, **payload)
        try:
            yield event
        except BaseException:
            self.refund_usage(event.id)
            raise

    @contextlib.asynccontextmanager
    async def safely_record_usage_async(
        self,
        codename: str,
        **payload: Unpack[FeatureRecordPayload],
    ) -> AsyncGenerator[FeatureUsageEvent, None]:
        """
        Safely record usage of a feature asynchronously.

        If an exception is raised inside the context manager, the usage will be
        refunded.

        It is generally recommended to use `safely_record_usage_async` over `record_usage_async`
        to avoid inconsistent results.
        """
        event = await self.record_usage_async(codename, **payload)
        try:
            yield event
        except BaseException:
            await self.refund_usage_async(event.id)
            raise
