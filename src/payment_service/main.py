from src.payment_service.processors import (
    StripePaymentProcessor,
    OfflinePaymentProcessor,
)
from src.payment_service.notifications import EmailNotifier, SMSNotifier
from src.payment_service.validations import CustomerValidator, PaymentDataValidator
from src.payment_service.logging import TransactionLogger
from src.payment_service.services import PaymentService


if __name__ == "__main__":
    stripe_processor = StripePaymentProcessor()
    offline_processor = OfflinePaymentProcessor()
    email_notifier = EmailNotifier()
    sms_notifier = SMSNotifier(gateway="CustomGateway")
    customer_validator = CustomerValidator()
    payment_validator = PaymentDataValidator()
    logger = TransactionLogger()

    payment_service = PaymentService(
        payment_processor=stripe_processor,
        notifier=email_notifier,
        customer_validator=customer_validator,
        payment_validator=payment_validator,
        logger=logger,
        recurring_processor=stripe_processor,
        refund_processor=stripe_processor,
    )

    second_service = PaymentService(
        payment_processor=offline_processor,
        notifier=sms_notifier,
        customer_validator=customer_validator,
        payment_validator=payment_validator,
        logger=logger,
    )
