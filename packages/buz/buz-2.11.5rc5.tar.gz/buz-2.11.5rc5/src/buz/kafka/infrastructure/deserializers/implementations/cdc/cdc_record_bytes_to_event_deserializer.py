from __future__ import annotations

from typing import TypeVar, Type, Generic

import orjson
from dacite import from_dict

from buz.kafka.infrastructure.deserializers.implementations.cdc.not_valid_cdc_message_exception import (
    NotValidCDCMessageException,
)
from buz.event import Event
from buz.kafka.infrastructure.cdc.cdc_message import CDCMessage, CDCPayload
from buz.kafka.infrastructure.deserializers.bytes_to_message_deserializer import BytesToMessageDeserializer

T = TypeVar("T", bound=Event)


class CDCRecordBytesToEventDeserializer(BytesToMessageDeserializer[Event], Generic[T]):
    __STRING_ENCODING = "utf-8"

    def __init__(self, event_class: Type[T]) -> None:
        self.__event_class = event_class

    def deserialize(self, data: bytes) -> T:
        decoded_string = data.decode(self.__STRING_ENCODING)
        try:
            cdc_message = self.__get_outbox_record_as_dict(decoded_string)
            return self.__event_class.restore(
                id=cdc_message.payload.event_id,
                created_at=cdc_message.payload.created_at,
                **orjson.loads(cdc_message.payload.payload),
            )
        except Exception as exception:
            raise NotValidCDCMessageException(decoded_string, exception) from exception

    def __get_outbox_record_as_dict(self, decoded_string: str) -> CDCMessage:
        decoded_record: dict = orjson.loads(decoded_string)

        payload = decoded_record.get("payload")
        if not isinstance(payload, dict):
            raise ValueError("The provided payload value is not valid")

        cdc_message = CDCMessage(payload=from_dict(CDCPayload, payload))
        return cdc_message
