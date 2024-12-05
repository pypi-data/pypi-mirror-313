from signal import signal, SIGTERM, SIGINT
from types import FrameType
from typing import Optional

from buz.event.strategies.execution_strategy.execution_strategy import ExecutionStrategy


class Worker:
    def __init__(
        self,
        execution_strategy: ExecutionStrategy,
    ) -> None:
        self.__execution_strategy = execution_strategy

    def start(self) -> None:
        signal(SIGINT, self.__sigterm_handler)
        signal(SIGTERM, self.__sigterm_handler)
        print("Starting buz worker...")
        self.__execution_strategy.start()
        print("Buz worker stopped gracefully")

    def __sigterm_handler(self, signum: int, frame: Optional[FrameType]) -> None:
        self.stop()

    def stop(self) -> None:
        print("Stopping buz worker...")
        self.__execution_strategy.stop()
