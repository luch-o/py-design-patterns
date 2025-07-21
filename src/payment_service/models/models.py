from typing import Optional

from enum import Enum
from pydantic import BaseModel


class ContactInfo(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None


class CustomerData(BaseModel):
    name: str
    contact_info: ContactInfo
    customer_id: Optional[str] = None


class PaymentType(Enum):
    ONLINE = "online"
    OFFLINE = "offline"


class PaymentData(BaseModel):
    amount: int
    source: str
    currency: str = "USD"
    payment_type: PaymentType = PaymentType.ONLINE


class Request(BaseModel):
    customer_data: CustomerData
    payment_data: PaymentData


class PaymentResponse(BaseModel):
    status: str
    amount: int
    transaction_id: Optional[str] = None
    message: Optional[str] = None
