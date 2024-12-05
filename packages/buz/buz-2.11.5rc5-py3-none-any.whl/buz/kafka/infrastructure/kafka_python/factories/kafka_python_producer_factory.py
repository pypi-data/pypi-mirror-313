from buz.kafka.domain.models.kafka_connection_config import KafkaConnectionConfig
from buz.kafka.infrastructure.kafka_python.kafka_python_producer import KafkaPythonProducer
from buz.kafka.infrastructure.serializers.byte_serializer import ByteSerializer
from buz.kafka.infrastructure.serializers.implementations.json_byte_serializer import JSONByteSerializer


class KafkaPythonProducerFactory:
    def __init__(
        self,
        kafka_connection_config: KafkaConnectionConfig,
        byte_serializer: ByteSerializer = JSONByteSerializer(),
    ):
        self._kafka_connection_config = kafka_connection_config
        self._byte_serializer = byte_serializer

    def build(self) -> KafkaPythonProducer:
        return KafkaPythonProducer(
            config=self._kafka_connection_config,
            byte_serializer=self._byte_serializer,
        )
