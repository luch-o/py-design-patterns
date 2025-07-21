from dataclasses import dataclass, field
from typing import TypeVar

from src.payment_service.listeners.interfaces import Listener


T = TypeVar("T")

@dataclass
class EventManager:
    listeners: list[Listener[T]] = field(default_factory=list)

    def subscribe(self, listener: Listener) -> None:
        self.listeners.append(listener)
    
    def unsubscribe(self, listener: Listener) -> None:
        self.listeners.remove(listener)

    def notify(self, event: T) -> None:
        for listener in self.listeners:
            listener.notify(event)