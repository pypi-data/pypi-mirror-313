from __future__ import annotations

from functools import wraps
from logging import Logger
from typing import Callable, Optional, Type, cast

from kafka import TopicPartition, OffsetAndMetadata, KafkaConsumer as KafkaPythonLibraryConsumer
from kafka.coordinator.assignors.abstract import AbstractPartitionAssignor

from buz.kafka.domain.exceptions.not_valid_kafka_message_exception import NotValidKafkaMessageException
from buz.kafka.domain.models.consumer_initial_offset_position import ConsumerInitialOffsetPosition
from buz.kafka.domain.models.kafka_connection_config import KafkaConnectionConfig
from buz.kafka.domain.models.kafka_consumer_record import KafkaConsumerRecord
from buz.kafka.domain.services.kafka_consumer import (
    KafkaConsumer,
    DEFAULT_NUMBER_OF_MESSAGES_TO_POLL,
)
from buz.kafka.infrastructure.deserializers.byte_deserializer import ByteDeserializer
from buz.kafka.infrastructure.kafka_python.exception.consumer_interrupted_exception import (
    ConsumerInterruptedException,
)
from buz.kafka.infrastructure.kafka_python.kafka_poll_record import KafkaPollRecord
from buz.kafka.infrastructure.kafka_python.translators.consumer_initial_offset_position_translator import (
    ConsumerInitialOffsetPositionTranslator,
)
from buz.kafka.infrastructure.serializers.kafka_header_serializer import KafkaHeaderSerializer


class KafkaPythonConsumer(KafkaConsumer):
    __CONSUMER_POLL_TIMEOUT_MS = 1000
    # https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html#kafka.KafkaConsumer.poll
    __SESSION_TIMEOUT_MS = 10000
    # https://docs.confluent.io/platform/current/installation/configuration/consumer-configs.html#session-timeout-ms

    def __init__(
        self,
        *,
        consumer_group: str,
        topics: list[str],
        connection_config: KafkaConnectionConfig,
        initial_offset_position: ConsumerInitialOffsetPosition,
        byte_deserializer: ByteDeserializer,
        header_serializer: KafkaHeaderSerializer,
        partition_assignors: tuple[Type[AbstractPartitionAssignor], ...],
        logger: Logger,
    ) -> None:
        self.__consumer_group = consumer_group
        self.__topics = topics
        self.__initial_offset_position = initial_offset_position
        self.__connection_config = connection_config
        self.__byte_deserializer = byte_deserializer
        self.__header_serializer = header_serializer
        self.__partition_assignors = partition_assignors
        self.__logger = logger

        self.__consumer = self.__generate_consumer()
        self.__offsets_metadata: dict[TopicPartition, OffsetAndMetadata] = {}
        self.__gracefully_stop = False

    def __generate_consumer(self) -> KafkaPythonLibraryConsumer:
        sasl_mechanism: Optional[str] = None

        if self.__connection_config.credentials.sasl_mechanism is not None:
            sasl_mechanism = self.__connection_config.credentials.sasl_mechanism.value

        consumer = KafkaPythonLibraryConsumer(
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
            session_timeout_ms=self.__SESSION_TIMEOUT_MS,
            partition_assignment_strategy=list(self.__partition_assignors),
        )

        consumer.subscribe(self.__topics)
        return consumer

    def __gracefully_handle_consumer_interruption(func: Callable) -> Callable:  # type: ignore[misc]
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.__gracefully_stop is True:
                self.__close_consumer()
                return

            try:
                return func(self, *args, **kwargs)
            except ConsumerInterruptedException:
                self.__close_consumer()
                return
            except Exception:
                self.__close_consumer()
                raise

        return wrapper

    @__gracefully_handle_consumer_interruption  # noqa
    def consume(
        self,
        *,
        consumption_callback: Callable[[KafkaConsumerRecord], None],
        number_of_messages_to_poll: int = DEFAULT_NUMBER_OF_MESSAGES_TO_POLL,
    ) -> None:
        self.__offsets_metadata.clear()
        poll_results = self.__consumer.poll(
            timeout_ms=self.__CONSUMER_POLL_TIMEOUT_MS,
            max_records=number_of_messages_to_poll,
        )

        for topic_partition, consumer_records in poll_results.items():
            for consumer_record in consumer_records:
                kafka_poll_record = cast(KafkaPollRecord, consumer_record)

                try:
                    if kafka_poll_record.value is None:
                        raise NotValidKafkaMessageException("The kafka poll record value is None")

                    consumption_callback(
                        KafkaConsumerRecord(
                            value=self.__byte_deserializer.deserialize(kafka_poll_record.value),
                            headers=self.__header_serializer.deserialize(kafka_poll_record.headers),
                        )
                    )
                except NotValidKafkaMessageException:
                    self.__logger.error(
                        f'The message "{str(kafka_poll_record.value)}" is not valid, it will be consumed but not processed'
                    )

                self.__mark_record_as_consumed(kafka_poll_record)

                if self.__gracefully_stop is True:
                    raise ConsumerInterruptedException()

        self.__consumer.commit()

    def __mark_record_as_consumed(self, consumer_record: KafkaPollRecord) -> None:
        """
        the committed offset should be
        the next message your application should consume, i.e.: last_offset + 1.
        """
        next_offset_to_be_consumed = consumer_record.offset + 1
        self.__offsets_metadata[
            TopicPartition(topic=consumer_record.topic, partition=consumer_record.partition)
        ] = OffsetAndMetadata(next_offset_to_be_consumed, "")

    def __close_consumer(self) -> None:
        self.__consumer.commit(offsets=self.__offsets_metadata)

        self.__logger.info(f"Closing connection of consumer with group_id={self.__consumer_group}")
        self.__consumer.close(autocommit=False)

    def request_stop(self) -> None:
        self.__gracefully_stop = True

    def is_ready_for_rebalancing(self) -> bool:
        return True
