import uuid
from datetime import datetime
from typing import Optional, TypedDict

from typing_extensions import NotRequired

from billing.types._billing_entity import BillingEntityWithTimestamps
from billing.types._common import CancellationFeedback
from billing.types._order import OrderWithCustomer


class Offer(BillingEntityWithTimestamps):
    order_id: str
    activated_at: Optional[datetime]
    cancel_at: Optional[datetime]
    cancellation_requested_at: Optional[datetime]
    cancellation_feedback: Optional[CancellationFeedback]
    cancellation_comment: Optional[str]


class OfferWithCustomer(Offer):
    order: OrderWithCustomer


class OfferCancelPayload(TypedDict):
    cancel_at: NotRequired[datetime]
    cancellation_feedback: NotRequired[CancellationFeedback]
    cancellation_comment: NotRequired[str]


class OfferListParams(TypedDict):
    user_id: NotRequired[uuid.UUID]
    order_id: NotRequired[str]
    offer_product_plan_id: NotRequired[str]
