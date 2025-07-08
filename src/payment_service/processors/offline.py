from src.payment_service.processors.interfaces import PaymentProcessorProtocol
from src.payment_service.models import CustomerData, PaymentData, PaymentResponse
import uuid


class OfflinePaymentProcessor(PaymentProcessorProtocol):
    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse:
        print("Processing offline payment for", customer_data.name)
        return PaymentResponse(
            status="success",
            amount=payment_data.amount,
            transaction_id=str(uuid.uuid4()),
            message="Offline payment success",
        )
