from decimal import Decimal
from typing import Optional

from billing.types._billing_entity import BillingEntityWithTimestamps
from billing.types._common import PeriodType, ProductPlanType
from billing.types._product import Product


class ProductPlan(BillingEntityWithTimestamps):
    product_id: str
    amount: Decimal
    currency: str
    period_type: Optional[PeriodType]
    period_count: int
    trial_period_days: Optional[int]
    product_plan_type: ProductPlanType


class ProductPlanWithProduct(ProductPlan):
    product: Product
