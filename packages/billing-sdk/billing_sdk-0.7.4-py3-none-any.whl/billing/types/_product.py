from typing import TypedDict

from typing_extensions import NotRequired

from billing.types._billing_entity import BillingEntityWithTimestamps


class Product(BillingEntityWithTimestamps):
    name: str
    description: str


class ProductDetailParams(TypedDict):
    product_plan_currency: NotRequired[str]


class ProductListParams(TypedDict):
    product_plan_currency: NotRequired[str]
