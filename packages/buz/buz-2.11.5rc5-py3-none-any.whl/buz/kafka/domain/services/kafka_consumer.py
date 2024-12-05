from abc import abstractmethod, ABC
from typing import Callable

from buz.kafka.domain.models.kafka_consumer_record import KafkaConsumerRecord

DEFAULT_NUMBER_OF_MESSAGES_TO_POLL = 500


class KafkaConsumer(ABC):
    @abstractmethod
    def consume(
        self,
        *,
        consumption_callback: Callable[[KafkaConsumerRecord], None],
        number_of_messages_to_poll: int = DEFAULT_NUMBER_OF_MESSAGES_TO_POLL,
    ) -> None:
        pass

    @abstractmethod
    def request_stop(self) -> None:
        """Request a graceful stop.
        This method does not stop the consumer in an instantaneous way,
        it will eventually finalize when the current task is completed
        """
        pass
