from typing import Optional
from buz.event.infrastructure.buz_kafka.consume_strategy.consume_strategy import KafkaConsumeStrategy
from buz.event.subscriber import Subscriber


class TopicAndSubscriptionGroupPerSubscriberKafkaConsumerStrategy(KafkaConsumeStrategy):
    def __init__(self, prefix: Optional[str]):
        self._prefix = f"{prefix}." or ""

    def get_topics(self, subscriber: Subscriber) -> list[str]:
        event_class = subscriber.handles()
        return [f"{self._prefix}{event_class.fqn()}"]

    def get_subscription_group(self, subscriber: Subscriber) -> str:
        return subscriber.fqn()
