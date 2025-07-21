from typing import Protocol, TypeVar

T = TypeVar("T")


class Listener(Protocol[T]):
    def notify(self, event: T) -> None: ...
