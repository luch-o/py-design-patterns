from src.payment_service.processors import StripePaymentProcessor, OfflinePaymentProcessor, PaymentProcessorProtocol

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