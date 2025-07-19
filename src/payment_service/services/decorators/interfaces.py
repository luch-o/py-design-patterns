from src.payment_service.models import CustomerData, PaymentData, PaymentResponse
from src.payment_service.notifications import Notifier
from src.payment_service.services.interfaces import PaymentServiceProtocol


class PaymentServiceDecoratorProtocol(PaymentServiceProtocol):
    wrapee: PaymentServiceProtocol

    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse: ...

    def process_refund(self, transaction_id: str) -> PaymentResponse: ...

    def setup_recurring(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse: ...

    def set_notification_strategy(self, notifier: Notifier): ...