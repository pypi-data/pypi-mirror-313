from decimal import Decimal

from billing.types._billing_entity import BillingEntityWithTimestamps
from billing.types._offer_product_plan import OfferProductPlanWithProduct


class InvoiceItem(BillingEntityWithTimestamps):
    amount: Decimal


class InvoiceItemWithProduct(InvoiceItem):
    offer_product_plan: OfferProductPlanWithProduct
