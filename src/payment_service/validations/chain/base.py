from abc import ABC, abstractmethod
from typing import Optional

from src.payment_service.models import Request


class ChainHandler(ABC):
    next_handler: Optional["ChainHandler"] = None

    @abstractmethod
    def handle(self, request: Request) -> None: ...

    def set_next(self, handler: "ChainHandler") -> "ChainHandler":
        self.next_handler = handler
        return handler