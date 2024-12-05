from billing.types._billing_entity import BillingEntity
from billing.types._product_plan import ProductPlanWithProduct


class OfferProductPlan(BillingEntity):
    offer_id: str
    product_plan_id: str


class OfferProductPlanWithProduct(OfferProductPlan):
    product_plan: ProductPlanWithProduct
