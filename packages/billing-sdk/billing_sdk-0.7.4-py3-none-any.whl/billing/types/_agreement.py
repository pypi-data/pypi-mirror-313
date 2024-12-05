from datetime import datetime
from typing import Literal, Optional, TypedDict

from typing_extensions import NotRequired

from billing.types._billing_entity import BillingEntityWithTimestamps


class Agreement(BillingEntityWithTimestamps):
    name: str
    type: Literal["generic", "named", "additional"]
    offer_id: str
    signed_at: Optional[datetime]


class AgreementWithTerms(Agreement):
    terms: str


class AgreementListParams(TypedDict):
    customer_id: NotRequired[str]
    order_id: NotRequired[str]
    offer_id: NotRequired[str]
    is_signed: NotRequired[bool]
