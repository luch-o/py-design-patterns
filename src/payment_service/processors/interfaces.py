from typing import Protocol
from src.payment_service.models import CustomerData, PaymentData, PaymentResponse


class PaymentProcessorProtocol(Protocol):
    """
    Protocol for processing payments, refunds, and recurring payments.

    This protocol defines the interface for payment processors. Implementations
    should provide methods for processing payments, refunds, and setting up recurring payments.
    """

    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse: ...


class RefundPaymentProtocol(Protocol):
    def refund_payment(self, transaction_id: str) -> PaymentResponse: ...


class RecurringPaymentProtocol(Protocol):
    def setup_recurring_payment(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse: ...
