from abc import ABC, abstractmethod

from buz.event import Event, Subscriber


class RejectCallback(ABC):
    @abstractmethod
    def on_reject(self, event: Event, subscribers: list[Subscriber]) -> None:
        pass
