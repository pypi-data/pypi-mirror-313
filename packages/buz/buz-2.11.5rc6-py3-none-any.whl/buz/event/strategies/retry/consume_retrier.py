from abc import ABC, abstractmethod
from buz.event import Event, Subscriber


class ConsumeRetrier(ABC):
    @abstractmethod
    def should_retry(self, event: Event, subscribers: list[Subscriber]) -> bool:
        pass

    @abstractmethod
    def register_retry(self, event: Event, subscribers: list[Subscriber]) -> None:
        pass
