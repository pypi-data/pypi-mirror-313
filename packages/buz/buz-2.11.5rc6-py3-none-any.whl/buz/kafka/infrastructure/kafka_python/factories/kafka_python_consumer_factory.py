from __future__ import annotations

from logging import Logger, getLogger
from typing import Type

from kafka.coordinator.assignors.abstract import AbstractPartitionAssignor
from kafka.coordinator.assignors.roundrobin import RoundRobinPartitionAssignor

from buz.kafka.domain.models.consumer_initial_offset_position import ConsumerInitialOffsetPosition
from buz.kafka.domain.models.kafka_connection_config import KafkaConnectionConfig
from buz.kafka.domain.services.kafka_consumer import KafkaConsumer
from buz.kafka.infrastructure.deserializers.byte_deserializer import ByteDeserializer
from buz.kafka.infrastructure.deserializers.implementations.json_byte_deserializer import JSONByteDeserializer
from buz.kafka.infrastructure.kafka_python.kafka_python_consumer import KafkaPythonConsumer
from buz.kafka.infrastructure.serializers.kafka_header_serializer import KafkaHeaderSerializer


class KafkaPythonConsumerFactory:
    __FALLBACK_PARTITION_ASSIGNORS = (RoundRobinPartitionAssignor,)

    def __init__(
        self,
        consumer_group: str,
        topics: list[str],
        kafka_connection_config: KafkaConnectionConfig,
        initial_offset_position: ConsumerInitialOffsetPosition = ConsumerInitialOffsetPosition.BEGINNING,
        byte_deserializer: ByteDeserializer = JSONByteDeserializer(),
        header_serializer: KafkaHeaderSerializer = KafkaHeaderSerializer(),
        kafka_partition_assignors: tuple[Type[AbstractPartitionAssignor], ...] = (),
        logger: Logger = getLogger(),
    ) -> None:
        self.__consumer_group = consumer_group
        self.__topics = topics
        self.__kafka_connection_config = kafka_connection_config
        self.__initial_offset_position = initial_offset_position
        self.__byte_deserializer = byte_deserializer
        self.__header_serializer = header_serializer
        self.__kafka_partition_assignors = self.__get_partition_assignors_ordered_by_priority(kafka_partition_assignors)
        self.__logger = logger

    def __get_partition_assignors_ordered_by_priority(
        self, kafka_partition_assignors: tuple[Type[AbstractPartitionAssignor], ...]
    ) -> tuple[Type[AbstractPartitionAssignor], ...]:
        # A tuple is used to support rolling-updates.
        return tuple(kafka_partition_assignors + self.__FALLBACK_PARTITION_ASSIGNORS)

    def build(self) -> KafkaConsumer:
        return KafkaPythonConsumer(
            consumer_group=self.__consumer_group,
            topics=self.__topics,
            connection_config=self.__kafka_connection_config,
            initial_offset_position=self.__initial_offset_position,
            byte_deserializer=self.__byte_deserializer,
            header_serializer=self.__header_serializer,
            partition_assignors=self.__kafka_partition_assignors,
            logger=self.__logger,
        )
