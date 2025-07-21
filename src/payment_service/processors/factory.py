from src.payment_service.processors import (
    StripePaymentProcessor,
    OfflinePaymentProcessor,
    PaymentProcessorProtocol,
    RecurringPaymentProtocol,
    RefundPaymentProtocol,
)

from src.payment_service.models.models import PaymentData, PaymentType


class PaymentProcessorFactory:
    @staticmethod
    def create_processor(payment_data: PaymentData) -> PaymentProcessorProtocol:
        match payment_data.payment_type:
            case PaymentType.ONLINE:
                return StripePaymentProcessor()
            case PaymentType.OFFLINE:
                return OfflinePaymentProcessor()
            case _:
                raise ValueError(f"Invalid payment type: {payment_data.payment_type}")

    @staticmethod
    def create_recurring_processor(
        payment_data: PaymentData,
    ) -> RecurringPaymentProtocol:
        match payment_data.payment_type:
            case PaymentType.ONLINE:
                return StripePaymentProcessor()
            case _:
                raise ValueError("Can't create recurring processor for offline payments")

    @staticmethod
    def create_refund_processor(payment_data: PaymentData) -> RefundPaymentProtocol:
        match payment_data.payment_type:
            case PaymentType.ONLINE:
                return StripePaymentProcessor()
            case _:
                raise ValueError("Can't create refund processor for offline payments")
