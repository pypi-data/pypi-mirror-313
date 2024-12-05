from logging import Logger
from typing import Optional, Type, TypeVar, cast

from kafka.coordinator.assignors.abstract import AbstractPartitionAssignor

from buz.event import Event, Subscriber
from buz.event.consumer import Consumer
from buz.event.infrastructure.buz_kafka.consume_strategy.consume_strategy import KafkaConsumeStrategy
from buz.event.infrastructure.buz_kafka.consume_strategy.kafka_on_fail_strategy import KafkaOnFailStrategy
from buz.event.middleware.consume_middleware import ConsumeMiddleware
from buz.event.middleware.consume_middleware_chain_resolver import ConsumeMiddlewareChainResolver
from buz.event.strategies.retry.consume_retrier import ConsumeRetrier
from buz.event.strategies.retry.reject_callback import RejectCallback
from buz.kafka import (
    KafkaPythonConsumerFactory,
    KafkaConnectionConfig,
    KafkaConsumerRecord,
    ConsumerInitialOffsetPosition,
)
from buz.kafka.infrastructure.deserializers.bytes_to_message_deserializer import BytesToMessageDeserializer
from buz.kafka.infrastructure.deserializers.implementations.json_bytes_to_message_deserializer import (
    JSONBytesToMessageDeserializer,
)

T = TypeVar("T", bound=Event)


class BuzKafkaConsumer(Consumer):
    def __init__(
        self,
        *,
        connection_config: KafkaConnectionConfig,
        consume_strategy: KafkaConsumeStrategy,
        on_fail_strategy: KafkaOnFailStrategy,
        kafka_partition_assignors: tuple[Type[AbstractPartitionAssignor], ...] = (),
        subscriber: Subscriber,
        logger: Logger,
        consumer_initial_offset_position: ConsumerInitialOffsetPosition,
        deserializer: Optional[BytesToMessageDeserializer[T]] = None,
        consume_middlewares: Optional[list[ConsumeMiddleware]] = None,
        consume_retrier: Optional[ConsumeRetrier] = None,
        reject_callback: Optional[RejectCallback] = None,
    ):
        self.__deserializer: BytesToMessageDeserializer[T] = deserializer or JSONBytesToMessageDeserializer(
            event_class=cast(Type[T], subscriber.handles())
        )

        self.__consume_strategy = consume_strategy
        self.__on_fail_strategy = on_fail_strategy
        self.__subscriber = subscriber
        self.__logger = logger
        self.__consumer_initial_offset_position = consumer_initial_offset_position
        self.__consume_middleware_chain_resolver = ConsumeMiddlewareChainResolver(consume_middlewares or [])
        self.__consume_retrier = consume_retrier
        self.__reject_callback = reject_callback

        kafka_python_consumer_factory = KafkaPythonConsumerFactory(
            consumer_group=self.__consume_strategy.get_subscription_group(self.__subscriber),
            topics=self.__consume_strategy.get_topics(self.__subscriber),
            kafka_connection_config=connection_config,
            initial_offset_position=self.__consumer_initial_offset_position,
            byte_deserializer=self.__deserializer,
            kafka_partition_assignors=kafka_partition_assignors,
            logger=self.__logger,
        )
        self.__consumer = kafka_python_consumer_factory.build()

    def run(self) -> None:
        self.__consumer.consume(consumption_callback=self.consumption_callback)

    def consumption_callback(self, message: KafkaConsumerRecord[T]) -> None:
        self.__consume_middleware_chain_resolver.resolve(message.value, self.__subscriber, self.__perform_consume)

    def stop(self) -> None:
        self.__consumer.request_stop()

    def __perform_consume(self, event: T, subscriber: Subscriber) -> None:
        should_retry = True
        while should_retry is True:
            try:
                return subscriber.consume(event)
            except Exception as exc:
                self.__logger.warning(f"Event {event.id} could not be consumed by the subscriber {subscriber.fqn}")

                should_retry = self.__should_retry(event, subscriber)

                if should_retry is True:
                    self.__register_retry(event, subscriber)
                    continue

                if should_retry is False:
                    if self.__reject_callback:
                        self.__reject_callback.on_reject(event=event, subscribers=[subscriber])

                    if self.__on_fail_strategy == KafkaOnFailStrategy.STOP_ON_FAIL:
                        raise exc

    def __should_retry(self, event: Event, subscriber: Subscriber) -> bool:
        if self.__consume_retrier is None:
            return False

        return self.__consume_retrier.should_retry(event, [subscriber])

    def __register_retry(self, event: Event, subscriber: Subscriber) -> None:
        if self.__consume_retrier is None:
            return None

        return self.__consume_retrier.register_retry(event, [subscriber])
