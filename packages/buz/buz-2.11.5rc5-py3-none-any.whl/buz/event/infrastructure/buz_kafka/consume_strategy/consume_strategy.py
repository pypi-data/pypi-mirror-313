from abc import abstractmethod, ABC
from buz.event.subscriber import Subscriber


class KafkaConsumeStrategy(ABC):
    @abstractmethod
    def get_topics(self, subscriber: Subscriber) -> list[str]:
        pass

    @abstractmethod
    def get_subscription_group(self, subscriber: Subscriber) -> str:
        pass
