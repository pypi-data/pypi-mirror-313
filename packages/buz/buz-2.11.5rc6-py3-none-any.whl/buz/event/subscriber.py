from abc import abstractmethod
from typing import Type

from buz import Handler
from buz.event import Event


class Subscriber(Handler):
    @classmethod
    @abstractmethod
    def handles(cls) -> Type[Event]:
        pass

    @abstractmethod
    def consume(self, event: Event) -> None:
        pass
