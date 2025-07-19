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

def get_sample_payment_data() -> PaymentData:
    return PaymentData(
        amount=100,
        source="stripe",
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
    payment_data = get_sample_payment_data()

    
    sms_notifier = SMSNotifier(gateway="CustomGateway")
    customer_validator = CustomerValidator()
    payment_validator = PaymentDataValidator()
    logger = TransactionLogger()

    payment_service = PaymentService.create_with_processor(
        payment_data,
        notifier=notifier,
        customer_validator=customer_validator,
        payment_validator=payment_validator,
        logger=logger,
    )

    payment_service.process_transaction(customer, PaymentData(amount=100, source="stripe"))

    payment_service.set_notification_strategy(notifier)

    payment_service.process_transaction(customer, PaymentData(amount=100, source="stripe"))

