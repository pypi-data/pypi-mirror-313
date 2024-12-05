from abc import ABC, abstractmethod


class AsyncConsumer(ABC):
    @abstractmethod
    async def run(self) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass
