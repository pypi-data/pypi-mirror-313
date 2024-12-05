from typing import Collection, Optional

from buz.kafka import (
    KafkaPythonProducer,
)
from buz.event import Event, EventBus
from buz.event.infrastructure.buz_kafka.publish_strategy.publish_strategy import KafkaPublishStrategy
from buz.event.middleware import (
    PublishMiddleware,
)
from buz.event.exceptions.event_not_published_exception import EventNotPublishedException
from buz.event.middleware.publish_middleware_chain_resolver import PublishMiddlewareChainResolver


class BuzKafkaEventBus(EventBus):
    def __init__(
        self,
        *,
        publish_strategy: KafkaPublishStrategy,
        publish_middlewares: Optional[list[PublishMiddleware]] = None,
        producer: KafkaPythonProducer,
    ):
        self.__publish_middleware_chain_resolver = PublishMiddlewareChainResolver(publish_middlewares or [])
        self.__publish_strategy = publish_strategy
        self.__producer = producer

    def publish(self, event: Event) -> None:
        self.__publish_middleware_chain_resolver.resolve(event, self.__perform_publish)

    def __perform_publish(self, event: Event) -> None:
        try:
            topic = self.__publish_strategy.get_topic(event)
            headers = self.__get_event_headers(event)
            self.__producer.produce(
                message=event,
                headers=headers,
                topic=topic,
            )
        except Exception as exc:
            raise EventNotPublishedException(event) from exc

    def bulk_publish(self, events: Collection[Event]) -> None:
        for event in events:
            self.publish(event)

    def __get_event_headers(self, event: Event) -> dict:
        return {"id": event.id}
