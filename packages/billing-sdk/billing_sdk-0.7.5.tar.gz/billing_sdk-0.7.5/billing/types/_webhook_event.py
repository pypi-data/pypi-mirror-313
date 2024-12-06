from datetime import datetime
from typing import Any, Dict

from billing.types._billing_entity import BillingObject


class WebhookEvent(BillingObject):
    id: str
    event_type: str
    attempt_number: int
    published_at: datetime
    object: Dict[str, Any]
