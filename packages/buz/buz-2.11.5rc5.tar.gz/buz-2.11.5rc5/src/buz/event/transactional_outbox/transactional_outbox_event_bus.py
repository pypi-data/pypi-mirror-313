from typing import Collection, Optional

from buz.event import Event, EventBus
from buz.event.transactional_outbox.event_to_outbox_record_translator import EventToOutboxRecordTranslator
from buz.event.transactional_outbox.outbox_record_validation.outbox_record_validator import OutboxRecordValidator
from buz.event.transactional_outbox.outbox_repository import OutboxRepository


class TransactionalOutboxEventBus(EventBus):
    def __init__(
        self,
        outbox_repository: OutboxRepository,
        event_to_outbox_record_translator: EventToOutboxRecordTranslator,
        outbox_record_validator: Optional[OutboxRecordValidator] = None,
    ):
        self.__outbox_repository = outbox_repository
        self.__event_to_outbox_record_translator = event_to_outbox_record_translator
        self.__outbox_record_validator = outbox_record_validator

    def publish(self, event: Event) -> None:
        """
        Raises:
            OutboxRecordValidationException: If any validation inside outbox_record_validator fails.
        """
        outbox_record = self.__event_to_outbox_record_translator.translate(event)
        if self.__outbox_record_validator is not None:
            self.__outbox_record_validator.validate(record=outbox_record)

        self.__outbox_repository.save(outbox_record)

    def bulk_publish(self, events: Collection[Event]) -> None:
        for event in events:
            self.publish(event)
