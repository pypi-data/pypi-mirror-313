import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional, TypedDict

from typing_extensions import NotRequired

from billing.types._billing_entity import BillingEntityWithTimestamps
from billing.types._common import PaymentMethod


class Invoice(BillingEntityWithTimestamps):
    total: Decimal
    currency: str
    issued_at: Optional[datetime]
    expired_at: datetime
    paid_at: Optional[datetime]
    refunded_at: Optional[datetime]
    payment_method: PaymentMethod
    receipt_url: str
    failed_reason: str
    checkout_session_url: Optional[str]


class InvoiceListParams(TypedDict):
    order_id: NotRequired[str]
    user_id: NotRequired[uuid.UUID]
