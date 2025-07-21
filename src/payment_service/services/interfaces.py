from typing import Optional, Protocol
from src.payment_service.models import CustomerData, PaymentData, PaymentResponse
from src.payment_service.processors import (
    PaymentProcessorProtocol,
    RecurringPaymentProtocol,
    RefundPaymentProtocol,
)
from src.payment_service.notifications import Notifier
from src.payment_service.validations import CustomerValidator, PaymentDataValidator
from src.payment_service.logging import TransactionLogger
from src.payment_service.listeners import EventManager


class PaymentServiceProtocol(Protocol):
    payment_processor: PaymentProcessorProtocol
    notifier: Notifier
    customer_validator: CustomerValidator
    payment_validator: PaymentDataValidator
    logger: TransactionLogger
    event_manager: EventManager
    recurring_processor: Optional[RecurringPaymentProtocol] = None
    refund_processor: Optional[RefundPaymentProtocol] = None

    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse: ...

    def process_refund(self, transaction_id: str) -> PaymentResponse: ...

    def setup_recurring(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse: ...

    def set_notification_strategy(self, notifier: Notifier): ...


