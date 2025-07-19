from dataclasses import dataclass
import logging
from src.payment_service.models import CustomerData, PaymentData, PaymentResponse
from src.payment_service.notifications import Notifier
from src.payment_service.services.decorators.interfaces import (
    PaymentServiceDecoratorProtocol,
)
from src.payment_service.services.interfaces import PaymentServiceProtocol

logger = logging.getLogger(__name__)


@dataclass
class PaymentServiceLoggerDecorator(PaymentServiceDecoratorProtocol):
    wrapee: PaymentServiceProtocol

    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse:
        logger.info(
            "Processing transaction for customer %s with payment data %s",
            customer_data.name,
            payment_data,
        )
        response = self.wrapee.process_transaction(customer_data, payment_data)
        logger.info(
            "Transaction processed for customer %s with payment data %s",
            customer_data.name,
            payment_data,
        )
        return response

    def process_refund(self, transaction_id: str) -> PaymentResponse:
        logger.info("Processing refund for transaction %s", transaction_id)
        response = self.wrapee.process_refund(transaction_id)
        logger.info("Refund processed for transaction %s", transaction_id)
        return response

    def setup_recurring(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse:
        logger.info(
            "Setting up recurring payment for customer %s with payment data %s",
            customer_data.name,
            payment_data,
        )
        response = self.wrapee.setup_recurring(customer_data, payment_data)
        logger.info(
            "Recurring payment setup for customer %s with payment data %s",
            customer_data.name,
            payment_data,
        )
        return response

    def set_notification_strategy(self, notifier: Notifier):
        logger.info("Setting notification strategy to %s", notifier)
        self.wrapee.set_notification_strategy(notifier)