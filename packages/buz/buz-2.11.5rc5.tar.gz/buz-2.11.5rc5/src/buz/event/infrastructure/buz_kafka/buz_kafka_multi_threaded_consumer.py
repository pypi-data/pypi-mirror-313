import time
import asyncio
from asyncio import Future, create_task, gather, Semaphore, Event as AsyncIOEvent, sleep
from datetime import timedelta, datetime
from logging import Logger
from threading import Thread
import traceback
from typing import Optional, Type, TypeVar
from queue import Queue

from kafka.coordinator.assignors.abstract import AbstractPartitionAssignor

from buz.event import Event, Subscriber
from buz.event.async_consumer import AsyncConsumer
from buz.event.domain.queue.queue_repository import QueueRepository
from buz.event.infrastructure.buz_kafka.consume_strategy.consume_strategy import KafkaConsumeStrategy
from buz.event.infrastructure.buz_kafka.consume_strategy.kafka_on_fail_strategy import KafkaOnFailStrategy
from buz.event.infrastructure.buz_kafka.in_memory_queue_repository import InMemoryQueueRepository
from buz.event.middleware.consume_middleware import ConsumeMiddleware
from buz.event.middleware.consume_middleware_chain_resolver import ConsumeMiddlewareChainResolver
from buz.event.strategies.retry.consume_retrier import ConsumeRetrier
from buz.event.strategies.retry.reject_callback import RejectCallback
from buz.kafka import (
    KafkaConnectionConfig,
    KafkaConsumerRecord,
    ConsumerInitialOffsetPosition,
)
from buz.kafka.infrastructure.deserializers.bytes_to_message_deserializer import BytesToMessageDeserializer
from buz.kafka.infrastructure.deserializers.implementations.json_bytes_to_message_deserializer import (
    JSONBytesToMessageDeserializer,
)
from buz.kafka.infrastructure.kafka_python.factories.kafka_python_multi_threaded_consumer_factory import (
    KafkaPythonMultiThreadedConsumerFactory,
)
from buz.kafka.infrastructure.kafka_python.kafka_poll_record import KafkaPollRecord
from buz.kafka.infrastructure.kafka_python.kafka_python_multi_threaded_consumer import KafkaPythonMultiThreadedConsumer

T = TypeVar("T", bound=Event)
KafkaConsumer = KafkaPythonMultiThreadedConsumer  # TODO: remove this alias once we comply with the interface

ConsumingTask = tuple[KafkaPollRecord, KafkaConsumer]


class BuzKafkaMultiThreadedConsumer(AsyncConsumer):
    __MAX_NUMBER_OF_POLLING_TASKS = 20
    __TIME_BETWEEN_POLLS_IF_THERE_ARE_TASKS_IN_THE_QUEUE = 0.5
    __TIME_BETWEEN_COMMITS_POLLING = 0.1
    __TIME_BETWEEN_RETRIES = 5

    __commit_task_future: Optional[Future]

    def __init__(
        self,
        *,
        connection_config: KafkaConnectionConfig,
        consume_strategy: KafkaConsumeStrategy,
        on_fail_strategy: KafkaOnFailStrategy,
        queue_repository: QueueRepository[ConsumingTask],
        kafka_partition_assignors: tuple[Type[AbstractPartitionAssignor], ...] = (),
        subscribers: list[Subscriber],
        logger: Logger,
        consumer_initial_offset_position: ConsumerInitialOffsetPosition,
        deserializers_per_subscriber: dict[Subscriber, BytesToMessageDeserializer[T]],
        consume_middlewares: Optional[list[ConsumeMiddleware]] = None,
        consume_retrier: Optional[ConsumeRetrier] = None,
        reject_callback: Optional[RejectCallback] = None,
        max_queue_size: int,
        max_records_retrieved_per_poll: int,
        min_time_between_polls_in_ms: int,
    ):
        self.__connection_config = connection_config
        self.__consume_strategy = consume_strategy
        self.__on_fail_strategy = on_fail_strategy
        self.__queue_repository = queue_repository
        self.__commit_repository: QueueRepository[ConsumingTask] = InMemoryQueueRepository(queue=Queue())
        self.__kafka_partition_assignors = kafka_partition_assignors
        self.__subscribers = subscribers
        self.__logger = logger
        self.__consumer_initial_offset_position = consumer_initial_offset_position
        self.__deserializers_per_subscriber = deserializers_per_subscriber
        self.__consume_middleware_chain_resolver = ConsumeMiddlewareChainResolver(consume_middlewares or [])
        self.__consume_retrier = consume_retrier
        self.__reject_callback = reject_callback
        self.__max_records_retrieved_per_poll = 1
        self.__subscriber_per_consumer_mapper: dict[KafkaConsumer, Subscriber] = {}
        self.__should_stop = AsyncIOEvent()
        self.__stop_commit_task = AsyncIOEvent()
        self.__stop_consumption_thread = AsyncIOEvent()
        self.__start_kafka_consumers_elapsed_time: Optional[timedelta] = None
        self.__initial_coroutines_created_elapsed_time: Optional[timedelta] = None
        self.__events_processed: int = 0
        self.__events_processed_elapsed_time: timedelta = timedelta()
        self.__polling_tasks_semaphore = Semaphore(self.__MAX_NUMBER_OF_POLLING_TASKS)
        self.__consumption_thread = Thread(target=lambda: asyncio.run(self.__consume_events_thread()))

    async def run(self) -> None:
        await self.__generate_kafka_consumers()

        start_time = datetime.now()

        self.__consumption_thread.start()
        self.__commit_task_future = create_task(self.__commit_task())
        await self.__polling_task()

        self.__events_processed_elapsed_time = datetime.now() - start_time

        await self.__perform_graceful_stop()

    async def __generate_kafka_consumers(self):
        start_time = datetime.now()
        tasks = [self.__create_kafka_consumer_for_subscriber(subscriber) for subscriber in self.__subscribers]
        await gather(*tasks)
        self.__start_kafka_consumers_elapsed_time = datetime.now() - start_time

    async def __create_kafka_consumer_for_subscriber(self, subscriber: Subscriber) -> None:
        byte_deserializer = self.__deserializers_per_subscriber.get(subscriber)
        kafka_python_consumer_factory = KafkaPythonMultiThreadedConsumerFactory(
            consumer_group=self.__consume_strategy.get_subscription_group(subscriber),
            topics=self.__consume_strategy.get_topics(subscriber),
            kafka_connection_config=self.__connection_config,
            initial_offset_position=self.__consumer_initial_offset_position,
            byte_deserializer=byte_deserializer or JSONBytesToMessageDeserializer(event_class=subscriber.handles()),  # type: ignore[arg-type]
            kafka_partition_assignors=self.__kafka_partition_assignors,
            logger=self.__logger,
        )
        kafka_consumer = kafka_python_consumer_factory.build()
        self.__subscriber_per_consumer_mapper[kafka_consumer] = subscriber
        await kafka_consumer.init()

    async def __polling_task(self) -> None:
        try:
            while not self.__should_stop.is_set():
                if not self.__queue_repository.is_empty():
                    await sleep(self.__TIME_BETWEEN_POLLS_IF_THERE_ARE_TASKS_IN_THE_QUEUE)
                    continue
                raw_consuming_tasks = await gather(
                    *[
                        self.__polling_consuming_tasks(kafka_consumer=consumer)
                        for consumer, subscriber in self.__subscriber_per_consumer_mapper.items()
                    ]
                )
                poll_results = [
                    consuming_task for consuming_tasks in raw_consuming_tasks for consuming_task in consuming_tasks
                ]

                if len(poll_results) == 0:
                    await sleep(self.__TIME_BETWEEN_POLLS_IF_THERE_ARE_TASKS_IN_THE_QUEUE)

                for poll_result in poll_results:
                    self.__queue_repository.push(poll_result)

        except Exception:
            self.__logger.error(f"Polling task failed with exception: {traceback.format_exc()}")
            self.__should_stop.set()

        return

    async def __commit_task(self) -> None:
        while not self.__stop_commit_task.is_set():
            await sleep(self.__TIME_BETWEEN_COMMITS_POLLING)
            await self.__commit_pending_tasks()

    async def __commit_pending_tasks(self) -> None:
        while self.__commit_repository.is_empty() is False:
            commit_record, consumer = self.__commit_repository.pop()
            await consumer.commit_poll_record(commit_record)

    async def __polling_consuming_tasks(self, kafka_consumer: KafkaConsumer) -> list[ConsumingTask]:
        async with self.__polling_tasks_semaphore:
            results = await kafka_consumer.poll(
                number_of_messages_to_poll=self.__max_records_retrieved_per_poll,
            )
        return [(result, kafka_consumer) for result in results]

    async def __consume_events_thread(self) -> None:
        while not self.__stop_consumption_thread.is_set():
            if self.__queue_repository.is_empty():
                await sleep(self.__TIME_BETWEEN_POLLS_IF_THERE_ARE_TASKS_IN_THE_QUEUE)
                continue

            kafka_poll_record, consumer = self.__queue_repository.pop()
            subscriber = self.__subscriber_per_consumer_mapper[consumer]

            try:
                await consumer.consume(
                    kafka_poll_record=kafka_poll_record,
                    consumption_callback=lambda kafka_record: self.__consumption_callback(subscriber, kafka_record),
                )
                self.__commit_repository.push((kafka_poll_record, consumer))
            except Exception as ex:
                self.__should_stop.set()
                consumer.reject_poll_record(kafka_poll_record)
                raise ex

    def __consumption_callback(self, subscriber: Subscriber, message: KafkaConsumerRecord[T]) -> None:
        self.__consume_middleware_chain_resolver.resolve(
            event=message.value, subscriber=subscriber, consume=self.__perform_consume
        )

    def __perform_consume(self, event: T, subscriber: Subscriber) -> None:
        should_retry = True
        while should_retry is True:
            try:
                self.__events_processed += 1
                return subscriber.consume(event)
            except Exception as exc:
                self.__events_processed -= 1
                self.__logger.warning(f"Event {event.id} could not be consumed by the subscriber {subscriber.fqn}")

                if self.__should_retry(event, subscriber) is True:
                    self.__register_retry(event, subscriber)
                    time.sleep(self.__TIME_BETWEEN_RETRIES)
                    continue

                if self.__on_fail_strategy == KafkaOnFailStrategy.STOP_ON_FAIL:
                    raise exc

                if self.__reject_callback:
                    self.__reject_callback.on_reject(event=event, subscribers=[subscriber])

                return

    def __should_retry(self, event: Event, subscriber: Subscriber) -> bool:
        if self.__consume_retrier is None:
            return False

        return self.__consume_retrier.should_retry(event, [subscriber])

    def __register_retry(self, event: Event, subscriber: Subscriber) -> None:
        if self.__consume_retrier is None:
            return None

        return self.__consume_retrier.register_retry(event, [subscriber])

    async def stop(self) -> None:
        self.__should_stop.set()
        self.__logger.info("Worker stop requested. Waiting for finalize the current task")

    async def __perform_graceful_stop(self) -> None:
        self.__logger.info("Stopping consuming thread....")
        await self.__manage_comsuption_thread_stopping()

        self.__logger.info("Commiting pending tasks")
        await self.__manage_commiting_task_stopping()

        self.__logger.info("Stopping kafka consumers...")
        await self.__manage_kafka_consumers_stopping()

        self.__logger.info("All kafka consumers stopped")
        self.__print_statistics()

    async def __manage_comsuption_thread_stopping(self) -> None:
        self.__stop_consumption_thread.set()
        await asyncio.to_thread(self.__consumption_thread.join)

    async def __manage_commiting_task_stopping(self) -> None:
        if self.__commit_task_future:
            self.__stop_commit_task.set()
            await self.__commit_task_future
        await self.__commit_pending_tasks()

    async def __manage_kafka_consumers_stopping(self) -> None:
        for kafka_consumer in self.__subscriber_per_consumer_mapper.keys():
            await kafka_consumer.stop()

    def __print_statistics(self) -> None:
        self.__logger.info("Number of subscribers: %d", len(self.__subscribers))
        self.__logger.info(f"Start kafka consumers elapsed time: {self.__start_kafka_consumers_elapsed_time}")
        self.__logger.info(f"Initial coroutines created elapsed time: {self.__initial_coroutines_created_elapsed_time}")
        self.__logger.info(f"Events processed: {self.__events_processed}")
        self.__logger.info(f"Events processed elapsed time: {self.__events_processed_elapsed_time}")
