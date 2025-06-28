import os
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


class NotificationSender:
    def notify(self, customer_data: Customer):
        if "email" in customer_data["contact_info"]:
            # import smtplib
            from email.mime.text import MIMEText

            msg = MIMEText("Thank you for your payment.")
            msg["Subject"] = "Payment Confirmation"
            msg["From"] = "no-reply@example.com"
            msg["To"] = customer_data["contact_info"]["email"]

            # server = smtplib.SMTP("localhost")
            # server.send_message(msg)
            # server.quit()
            print("Email sent to", customer_data["contact_info"]["email"])

        elif "phone" in customer_data["contact_info"]:
            phone_number = customer_data["contact_info"]["phone"]
            sms_gateway = "the custom SMS Gateway"
            print(
                f"send the sms using {sms_gateway}: SMS sent to {phone_number}: Thank you for your payment."
            )

        else:
            print("No valid contact information for notification")
            return


class TransactionLogger:
    def log(self, customer_data: Customer, payment_data: Payment, charge: Charge):
        with open("transactions.log", "a") as log_file:
            log_file.write(f"{customer_data['name']} paid {payment_data['amount']}\n")
            log_file.write(f"Payment status: {charge['status']}\n")


class StripePaymentProcessor:
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


class PaymentProcessingSerivice:
    customer_validator = CustomerValidator()
    payment_validator = PaymentValidator()
    payment_processor = StripePaymentProcessor()
    notification_sender = NotificationSender()
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
