from __future__ import annotations

from logging import Logger
from typing import Callable, Optional, cast
from asgiref.sync import sync_to_async

from aiokafka import AIOKafkaConsumer, TopicPartition, OffsetAndMetadata
from buz.kafka.domain.exceptions.not_valid_kafka_message_exception import NotValidKafkaMessageException
from buz.kafka.domain.models.consumer_initial_offset_position import ConsumerInitialOffsetPosition
from buz.kafka.domain.models.kafka_connection_config import KafkaConnectionConfig
from buz.kafka.domain.models.kafka_consumer_record import KafkaConsumerRecord
from buz.kafka.infrastructure.deserializers.byte_deserializer import ByteDeserializer
from buz.kafka.infrastructure.kafka_python.kafka_poll_record import KafkaPollRecord
from buz.kafka.infrastructure.kafka_python.rebalance_ready import RebalanceReady
from buz.kafka.infrastructure.kafka_python.simple_kafka_lock_rebalancer import SimpleKafkaLockRebalancer
from buz.kafka.infrastructure.kafka_python.translators.consumer_initial_offset_position_translator import (
    ConsumerInitialOffsetPositionTranslator,
)
from buz.kafka.infrastructure.serializers.kafka_header_serializer import KafkaHeaderSerializer


class KafkaPythonMultiThreadedConsumer(RebalanceReady):
    __DEFAULT_POLL_TIMEOUT_MS = 0
    __DEFAULT_SESSION_TIMEOUT_MS = 1000 * 60
    __DEFAULT_HEARTBEAT_INTERVAL_MS = 1000 * 15
    __DEFAULT_MAX_POLL_INTERVAL = 2147483647

    def __init__(
        self,
        *,
        consumer_group: str,
        topics: list[str],
        connection_config: KafkaConnectionConfig,
        initial_offset_position: ConsumerInitialOffsetPosition,
        byte_deserializer: ByteDeserializer,
        header_serializer: KafkaHeaderSerializer,
        partition_assignors: tuple,
        logger: Logger,
        session_timeout_ms: int = __DEFAULT_SESSION_TIMEOUT_MS,
    ) -> None:
        self.__consumer_group = consumer_group
        self.__topics = topics
        self.__initial_offset_position = initial_offset_position
        self.__connection_config = connection_config
        self.__byte_deserializer = byte_deserializer
        self.__header_serializer = header_serializer
        self.__partition_assignors = partition_assignors
        self.__logger = logger
        self.__session_timeout_ms = session_timeout_ms
        self.__pending_messages: int = 0
        self.__consumer = self.__generate_consumer()

    def __generate_consumer(self) -> AIOKafkaConsumer:
        sasl_mechanism: Optional[str] = None

        if self.__connection_config.credentials.sasl_mechanism is not None:
            sasl_mechanism = self.__connection_config.credentials.sasl_mechanism.value

        consumer = AIOKafkaConsumer(
            None,
            bootstrap_servers=self.__connection_config.bootstrap_servers,
            security_protocol=self.__connection_config.credentials.security_protocol.value,
            sasl_mechanism=sasl_mechanism,
            sasl_plain_username=self.__connection_config.credentials.user,
            sasl_plain_password=self.__connection_config.credentials.password,
            client_id=self.__connection_config.client_id,
            group_id=self.__consumer_group,
            enable_auto_commit=False,
            auto_offset_reset=ConsumerInitialOffsetPositionTranslator.to_kafka_supported_format(
                self.__initial_offset_position
            ),
            session_timeout_ms=self.__session_timeout_ms,
            heartbeat_interval_ms=self.__DEFAULT_HEARTBEAT_INTERVAL_MS,
            partition_assignment_strategy=list(self.__partition_assignors),
            max_poll_interval_ms=self.__DEFAULT_MAX_POLL_INTERVAL,
            rebalance_timeout_ms=self.__DEFAULT_MAX_POLL_INTERVAL,
        )

        consumer.subscribe(topics=self.__topics, listener=SimpleKafkaLockRebalancer(self))
        return consumer

    async def init(self) -> None:
        await self.__consumer.start()

    async def poll(
        self,
        *,
        timeout_ms: int = __DEFAULT_POLL_TIMEOUT_MS,
        number_of_messages_to_poll: Optional[int] = None,
    ) -> list[KafkaPollRecord]:
        poll_results = await self.__consumer.getmany(
            timeout_ms=timeout_ms,
            max_records=number_of_messages_to_poll,
        )

        results = [
            cast(KafkaPollRecord, consumer_record)
            for consumer_records in poll_results.values()
            for consumer_record in consumer_records
        ]

        self.__pending_messages += len(results)

        return results

    async def consume(
        self,
        *,
        kafka_poll_record: KafkaPollRecord,
        consumption_callback: Callable[[KafkaConsumerRecord], None],
    ) -> None:
        try:
            if kafka_poll_record.value is None:
                raise NotValidKafkaMessageException("Message is None")

            await sync_to_async(
                lambda: consumption_callback(
                    KafkaConsumerRecord(
                        value=self.__byte_deserializer.deserialize(kafka_poll_record.value),
                        headers=self.__header_serializer.deserialize(kafka_poll_record.headers),
                    )
                ),
                thread_sensitive=True,
            )()

        except NotValidKafkaMessageException:
            self.__logger.error(
                f'The message "{str(kafka_poll_record.value)}" is not valid, it will be consumed but not processed'
            )

    async def commit_poll_record(self, poll_record: KafkaPollRecord) -> None:
        offset = {
            TopicPartition(topic=poll_record.topic, partition=poll_record.partition): OffsetAndMetadata(
                poll_record.offset + 1, ""
            )
        }
        await self.__consumer.commit(offset)
        self.__pending_messages -= 1

    def reject_poll_record(self, poll_record: KafkaPollRecord) -> None:
        self.__logger.warning(f"Message {str(poll_record.value)} will be rejected")
        self.__pending_messages -= 1

    async def stop(self) -> None:
        self.__logger.info(f"Closing connection of consumer with group_id={self.__consumer_group}")
        self.__pending_messages = 0
        await self.__consumer.stop()

    def is_ready_for_rebalancing(self) -> bool:
        return self.__pending_messages == 0
