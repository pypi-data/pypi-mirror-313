from __future__ import annotations

from abc import abstractmethod, ABC

from buz.kafka.domain.models.kafka_topic import KafkaTopic

DEFAULT_NUMBER_OF_MESSAGES_TO_POLLING = 999


class KafkaAdminClient(ABC):
    @abstractmethod
    def create_topics(
        self,
        *,
        topics: set[KafkaTopic],
    ) -> None:
        pass

    @abstractmethod
    def delete_topics(
        self,
        *,
        topics: set[str],
    ) -> None:
        pass

    @abstractmethod
    def get_topics(
        self,
    ) -> set[str]:
        pass
