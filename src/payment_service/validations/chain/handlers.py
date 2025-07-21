from .base import ChainHandler
from src.payment_service.models import Request
from src.payment_service.validations import CustomerValidator, PaymentDataValidator


class CustomerHandler(ChainHandler):
    def handle(self, request: Request) -> None:
        validator = CustomerValidator()
        validator.validate(request.customer_data)
        if self.next_handler:
            self.next_handler.handle(request)


class PaymentHandler(ChainHandler):
    def handle(self, request: Request) -> None:
        validator = PaymentDataValidator()
        validator.validate(request.payment_data)
        if self.next_handler:
            self.next_handler.handle(request)
