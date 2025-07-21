from src.payment_service.notifications import EmailNotifier, SMSNotifier
from src.payment_service.services import PaymentServiceBuilder
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

    builder = PaymentServiceBuilder()
    service = (
        builder.set_customer_validator()
        .set_payment_validator()
        .set_logger()
        .set_notifier(customer.contact_info)
        .set_payment_processor(payment_data)
        .set_recurring_processor(payment_data)
        .set_refund_processor(payment_data)
        .set_processor_logging()
        .build()
    )

    service.process_transaction(customer, PaymentData(amount=100, source="stripe"))
