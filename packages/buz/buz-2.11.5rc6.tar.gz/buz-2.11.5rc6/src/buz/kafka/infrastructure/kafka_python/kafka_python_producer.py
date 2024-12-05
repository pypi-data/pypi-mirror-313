from __future__ import annotations

from typing import Generic, Optional, TypeVar

from kafka import KafkaProducer as KafkaPythonLibraryProducer

from buz.kafka.domain.models.kafka_connection_config import KafkaConnectionConfig
from buz.kafka.domain.services.kafka_producer import KafkaProducer
from buz.kafka.infrastructure.serializers.byte_serializer import ByteSerializer
from buz.kafka.infrastructure.serializers.kafka_header_serializer import KafkaHeaderSerializer

T = TypeVar("T")


class KafkaPythonProducer(KafkaProducer, Generic[T]):
    def __init__(
        self,
        *,
        config: KafkaConnectionConfig,
        byte_serializer: ByteSerializer[T],
        retries: int = 0,
        retry_backoff_ms: int = 100,
    ) -> None:
        self.__config = config
        self.__byte_serializer = byte_serializer
        self.__header_serializer = KafkaHeaderSerializer()

        self.__kafka_producer = KafkaPythonLibraryProducer(
            client_id=self.__config.client_id,
            bootstrap_servers=self.__config.bootstrap_servers,
            security_protocol=self.__config.credentials.security_protocol.value,
            sasl_mechanism=self.__config.credentials.sasl_mechanism,
            sasl_plain_username=self.__config.credentials.user,
            sasl_plain_password=self.__config.credentials.password,
            retries=retries,
            retry_backoff_ms=retry_backoff_ms,
        )

    def produce(
        self,
        *,
        topic: str,
        message: T,
        partition_key: Optional[str] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> None:
        serialized_headers = self.__header_serializer.serialize(headers) if headers is not None else None

        self.__kafka_producer.send(
            topic=topic,
            value=self.__byte_serializer.serialize(message),
            headers=serialized_headers,
            key=partition_key,
        )
        # We are forcing a flush because the task related with the send is asynchronous, and we want that the event to be sent after call produce
        self.__kafka_producer.flush()
