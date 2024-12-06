import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional, TypedDict, Union

from billing.types._billing_entity import BillingEntity, BillingObject


class FeatureUsageSummary(BillingObject):
    feature_id: str
    feature_codename: str
    period_start: Optional[datetime]
    max_usage_limit: Optional[Decimal]
    used_amount: Optional[Decimal]


class FeatureUsageEvent(BillingEntity):
    feature_id: str
    user_id: uuid.UUID
    amount: Decimal
    refunded_at: Optional[datetime]


class FeatureRecordPayload(TypedDict):
    user_id: uuid.UUID
    amount: Union[Decimal, int]
