from __future__ import annotations

from dataclasses import asdict

from buz.event import Event
from buz.kafka.infrastructure.cdc.cdc_message import CDCMessage, CDCPayload
from buz.kafka.infrastructure.serializers.byte_serializer import ByteSerializer
from buz.kafka.infrastructure.serializers.implementations.json_byte_serializer import JSONByteSerializer


class CDCRecordBytesToEventSerializer(ByteSerializer):
    def __init__(self) -> None:
        self.__json_serializer = JSONByteSerializer()

    def serialize(self, data: Event) -> bytes:
        cdc_message: CDCMessage = CDCMessage(
            payload=CDCPayload(
                event_id=data.id,
                created_at=data.created_at,
                event_fqn=data.fqn(),
                payload=self.__serialize_payload(data),
            )
        )
        return self.__json_serializer.serialize(asdict(cdc_message))

    def __serialize_payload(self, event: Event) -> str:
        # Remove id and created at, because Transactional outbox is not adding them
        payload = asdict(event)
        del payload["id"]
        del payload["created_at"]
        return self.__json_serializer.serialize_as_json(payload)
