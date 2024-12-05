from __future__ import annotations

from abc import abstractmethod, ABC
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class KafkaProducer(ABC, Generic[T]):
    @abstractmethod
    def produce(
        self,
        *,
        topic: str,
        message: T,
        partition_key: Optional[str] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> None:
        pass
