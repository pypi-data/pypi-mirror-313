from abc import ABC, abstractmethod


class AsyncExecutionStrategy(ABC):
    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass
