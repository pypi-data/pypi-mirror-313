from abc import ABC, abstractmethod
from typing import Collection

from buz.event import Event


class EventBus(ABC):
    @abstractmethod
    def publish(self, event: Event) -> None:
        pass

    @abstractmethod
    def bulk_publish(self, events: Collection[Event]) -> None:
        pass
