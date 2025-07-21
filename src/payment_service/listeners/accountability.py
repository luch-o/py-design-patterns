from typing import TypeVar
from src.payment_service.listeners.interfaces import Listener

T = TypeVar("T")

class AccountabilityListener(Listener[T]):

    def notify(self, event: T) -> None:
        print(f"Notifying accountability the event: {event}")