import os
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from pydantic import BaseModel

from dotenv import load_dotenv
import stripe
from stripe import Charge
from stripe.error import StripeError

_ = load_dotenv()


class ContactInfo(BaseModel):
    email: str | None = None
    phone: str | None = None


class Customer(BaseModel):
    name: str
    contact_info: ContactInfo


class Payment(BaseModel):
    amount: int
    source: str
    cvv: int


class CustomerValidator:
    def validate(self, customer_data: Customer):
        if not customer_data.get("name"):
            print("Invalid customer data: missing name")
            raise ValueError("Invalid customer data: missing name")

        if not customer_data.get("contact_info"):
            print("Invalid customer data: missing contact info")
            raise ValueError("Invalid customer data: missing contact info")


class PaymentValidator:
    def validate(self, payment_data: Payment):
        if not payment_data.get("source"):
            print("Invalid payment data")
            raise ValueError("Invalid payment data")

class INotificationSender(ABC):
    """Notification sender interface"""

    @abstractmethod
    def send_confirmation(self, customer_data: Customer):
        """Send a confirmation notification to the customer"""

class EmailNotificationSender(INotificationSender):
    """Email notification sender"""

    def send_confirmation(self, customer_data: Customer):
        from email.mime.text import MIMEText

        msg = MIMEText("Thank you for your payment.")
        msg["Subject"] = "Payment Confirmation"
        msg["From"] = "no-reply@example.com"
        msg["To"] = customer_data.contact_info.email or ""

        print("Email sent to", customer_data.contact_info.email)

class SMSNotificationSender(INotificationSender):
    """SMS notification sender"""

    def send_confirmation(self, customer_data: Customer):        
        phone_number = customer_data.contact_info.phone
        sms_gateway = "the custom SMS Gateway"
        print(
            f"send the sms using {sms_gateway}: SMS sent to {phone_number}: Thank you for your payment."
        )


class TransactionLogger:
    def log(self, customer_data: Customer, payment_data: Payment, charge: Charge):
        with open("transactions.log", "a") as log_file:
            log_file.write(f"{customer_data['name']} paid {payment_data['amount']}\n")
            log_file.write(f"Payment status: {charge['status']}\n")


class IPaymentProcessor(ABC):
    """Payment processor interface"""

    @abstractmethod
    def process_transaction(self, customer_data: Customer, payment_data: Payment) -> Charge:
        """Process a transaction"""


class StripePaymentProcessor(IPaymentProcessor):
    """Stripe payment processor"""

    def process_transaction(self, customer_data: Customer, payment_data: Payment) -> Charge:
        stripe.api_key = os.getenv("STRIPE_API_KEY")

        try:
            charge = stripe.Charge.create(
                amount=payment_data["amount"],
                currency="usd",
                source=payment_data["source"],
                description="Charge for " + customer_data["name"],
            )
            print("Payment successful")
        except StripeError as e:
            print("Payment failed:", e)
            raise

        return charge

@dataclass
class PaymentProcessingSerivice:
    """Payment processing service"""

    customer_validator = CustomerValidator()
    payment_validator = PaymentValidator()
    payment_processor: IPaymentProcessor = field(default_factory=StripePaymentProcessor)
    notification_sender: INotificationSender = field(default_factory=EmailNotificationSender)
    transaction_logger = TransactionLogger()

    def process_transaction(self, customer_data: Customer, payment_data: Payment):
        self.customer_validator.validate(customer_data)
        self.payment_validator.validate(payment_data)
        charge = self.payment_processor.process_transaction(customer_data, payment_data)
        self.notification_sender.notify(customer_data)
        self.transaction_logger.log(customer_data, payment_data, charge)


if __name__ == "__main__":
    payment_processor = PaymentProcessingSerivice()

    customer_data_with_email = {
        "name": "John Doe",
        "contact_info": {"email": "e@mail.com"},
    }
    customer_data_with_phone = {
        "name": "Platzi Python",
        "contact_info": {"phone": "1234567890"},
    }

    payment_data = {"amount": 500, "source": "tok_mastercard", "cvv": 123}

    payment_processor.process_transaction(customer_data_with_email, payment_data)
    payment_processor.process_transaction(customer_data_with_phone, payment_data)
