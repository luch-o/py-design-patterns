from src.payment_service.processors import (
    StripePaymentProcessor,
    OfflinePaymentProcessor,
)
from src.payment_service.notifications import EmailNotifier, SMSNotifier
from src.payment_service.validations import CustomerValidator, PaymentDataValidator
from src.payment_service.logging import TransactionLogger
from src.payment_service.services import PaymentService
from src.payment_service.models import CustomerData, ContactInfo, PaymentData
from src.payment_service.notifications import Notifier


def get_sample_customer_data() -> CustomerData:
    return CustomerData(
        name="John Doe",
        contact_info=ContactInfo(email="john.doe@example.com", phone="1234567890"),
    )

def get_notification_strategy(customer_data: CustomerData) -> Notifier:
    if customer_data.contact_info.email:
        return EmailNotifier()
    elif customer_data.contact_info.phone:
        return SMSNotifier(gateway="CustomGateway")
    else:
        raise ValueError("No contact info provided")


if __name__ == "__main__":
    customer = get_sample_customer_data()
    notifier = get_notification_strategy(customer)
    
    stripe_processor = StripePaymentProcessor()
    offline_processor = OfflinePaymentProcessor()
    
    sms_notifier = SMSNotifier(gateway="CustomGateway")
    customer_validator = CustomerValidator()
    payment_validator = PaymentDataValidator()
    logger = TransactionLogger()

    payment_service = PaymentService(
        payment_processor=stripe_processor,
        notifier=notifier,
        customer_validator=customer_validator,
        payment_validator=payment_validator,
        logger=logger,
        recurring_processor=stripe_processor,
        refund_processor=stripe_processor,
    )

    payment_service.process_transaction(customer, PaymentData(amount=100, source="stripe"))

    payment_service.set_notification_strategy(notifier)

    payment_service.process_transaction(customer, PaymentData(amount=100, source="stripe"))

