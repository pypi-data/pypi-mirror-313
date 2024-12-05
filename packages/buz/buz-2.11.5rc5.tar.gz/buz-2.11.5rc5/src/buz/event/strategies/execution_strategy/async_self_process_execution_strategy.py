from buz.event.async_consumer import AsyncConsumer
from buz.event.strategies.execution_strategy.async_execution_strategy import AsyncExecutionStrategy


class AsyncSelfProcessExecutionStrategy(AsyncExecutionStrategy):
    def __init__(self, consumer: AsyncConsumer):
        self.__consumer = consumer

    async def start(self) -> None:
        await self.__consumer.run()

    async def stop(self) -> None:
        await self.__consumer.stop()
