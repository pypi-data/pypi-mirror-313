import uuid
from typing import Optional, TypedDict

from typing_extensions import NotRequired

from billing.types._billing_entity import BillingEntity, BillingObject


class CustomerAddress(BillingObject):
    country: str
    state: Optional[str] = None
    city: Optional[str] = None
    line1: Optional[str] = None
    line2: Optional[str] = None
    postal_code: Optional[str] = None


class Customer(BillingEntity):
    user_id: uuid.UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[CustomerAddress]


class CustomerAddressCreatePayload(TypedDict):
    country: str
    state: NotRequired[str]
    city: NotRequired[str]
    line1: NotRequired[str]
    line2: NotRequired[str]
    postal_code: NotRequired[str]


class CustomerCreatePayload(TypedDict):
    user_id: uuid.UUID
    first_name: NotRequired[str]
    last_name: NotRequired[str]
    email: NotRequired[str]
    phone: NotRequired[str]
    address: NotRequired[CustomerAddressCreatePayload]


class CustomerListParams(TypedDict):
    user_id: NotRequired[uuid.UUID]
