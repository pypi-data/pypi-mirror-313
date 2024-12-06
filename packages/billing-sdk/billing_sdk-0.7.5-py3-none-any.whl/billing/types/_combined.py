from typing import List

from billing.types._invoice import Invoice
from billing.types._invoice_item import InvoiceItemWithProduct
from billing.types._offer import Offer, OfferWithCustomer
from billing.types._offer_product_plan import OfferProductPlan, OfferProductPlanWithProduct
from billing.types._order import Order
from billing.types._product import Product
from billing.types._product_plan import ProductPlan


class InvoiceWithItemsBundle(Invoice):
    items: List[InvoiceItemWithProduct]


class OfferPlansBundle(Offer):
    offer_product_plans: List[OfferProductPlan]


class OfferInvoicesBundle(Offer):
    invoices: List[InvoiceWithItemsBundle]


class OrderOffersBundle(Order):
    offers: List[OfferPlansBundle]


class OfferCustomerProductsBundle(OfferWithCustomer):
    last_invoice: InvoiceWithItemsBundle
    offer_product_plans: List[OfferProductPlanWithProduct]


class OrderWithOffersAndInvoicesBundle(Order):
    offers: List[OfferInvoicesBundle]


class ProductWithPlansAndImagesBundle(Product):
    product_plans: List[ProductPlan]
