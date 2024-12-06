from typing import TypedDict

from typing_extensions import NotRequired

from billing.types._billing_entity import BillingEntityWithTimestamps
from billing.types._common import ProductPlanType


class Product(BillingEntityWithTimestamps):
    name: str
    description: str


class ProductDetailParams(TypedDict):
    product_plan_currency: NotRequired[str]
    product_plan_type: NotRequired[ProductPlanType]


class ProductListParams(TypedDict):
    product_plan_currency: NotRequired[str]
    product_plan_type: NotRequired[ProductPlanType]
