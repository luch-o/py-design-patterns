from dataclasses import dataclass
from typing import Optional, Self


from src.payment_service.services import (
    PaymentService,
    PaymentServiceLoggerDecorator,
    PaymentServiceProtocol,
)
from src.payment_service.processors import (
    PaymentProcessorProtocol,
    RecurringPaymentProtocol,
    RefundPaymentProtocol,
)
from src.payment_service.notifications import Notifier
from src.payment_service.validations import ChainHandler, CustomerHandler, PaymentHandler
from src.payment_service.notifications import NotifierFactory
from src.payment_service.processors import PaymentProcessorFactory
from src.payment_service.logging import TransactionLogger
from src.payment_service.models import ContactInfo, PaymentData
from src.payment_service.listeners import EventManager, AccountabilityListener


@dataclass
class PaymentServiceBuilder:
    payment_processor: Optional[PaymentProcessorProtocol] = None
    notifier: Optional[Notifier] = None
    validator: Optional[ChainHandler] = None
    logger: Optional[TransactionLogger] = None
    event_manager: Optional[EventManager] = None
    recurring_processor: Optional[RecurringPaymentProtocol] = None
    refund_processor: Optional[RefundPaymentProtocol] = None

    def set_validator(self) -> Self:
        customer_validator = CustomerHandler()
        payment_validator = PaymentHandler()
        customer_validator.set_next(payment_validator)
        self.validator = customer_validator
        return self

    def set_logger(self) -> Self:
        self.logger = TransactionLogger()
        return self

    def set_notifier(self, contact_info: ContactInfo) -> Self:
        self.notifier = NotifierFactory.create_notifier(contact_info)
        return self
    
    def set_event_manager(self) -> Self:
        self.event_manager = EventManager()
        self.event_manager.subscribe(AccountabilityListener())
        return self

    def set_payment_processor(self, payment_data: PaymentData) -> Self:
        self.payment_processor = PaymentProcessorFactory.create_processor(payment_data)
        return self

    def set_recurring_processor(self, payment_data: PaymentData) -> Self:
        try:
            self.recurring_processor = (
                PaymentProcessorFactory.create_recurring_processor(payment_data)
            )
        except ValueError:
            pass  # log something
        finally:
            return self

    def set_refund_processor(self, payment_data: PaymentData) -> Self:
        try:
            self.refund_processor = PaymentProcessorFactory.create_refund_processor(
                payment_data
            )
        except ValueError:
            pass  # log something
        finally:
            return self

    def set_processor_logging(self) -> Self:
        if self.payment_processor:
            self.payment_processor = PaymentServiceLoggerDecorator(
                self.payment_processor
            )
        else:
            raise ValueError("Missing payment processor dependency")
        if self.recurring_processor:
            self.recurring_processor = PaymentServiceLoggerDecorator(
                self.recurring_processor
            )
        if self.refund_processor:
            self.refund_processor = PaymentServiceLoggerDecorator(self.refund_processor)
        return self

    def build(self) -> PaymentServiceProtocol:
        missing = [
            name
            for name, value in [
                ("payment_processor", self.payment_processor),
                ("notifier", self.notifier),
                ("validator", self.validator),
                ("logger", self.logger),
                ("event_manager", self.event_manager),
            ]
            if value is None
        ]
        if missing:
            raise ValueError(f"Missing dependencies: {missing}")

        return PaymentService(
            payment_processor=self.payment_processor,
            notifier=self.notifier,
            validator=self.validator,
            logger=self.logger,
            event_manager=self.event_manager,
            recurring_processor=self.recurring_processor,
            refund_processor=self.refund_processor,
        )
