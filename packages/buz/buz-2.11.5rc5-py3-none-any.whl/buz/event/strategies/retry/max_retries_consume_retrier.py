from buz.event import Event, Subscriber

from buz.event.strategies.retry.consume_retrier import ConsumeRetrier
from buz.event.strategies.retry.consumed_event_retry_repository import ConsumedEventRetryRepository
from buz.event.strategies.retry.max_retries_negative_exception import InvalidMaxRetriesParamException


class MaxRetriesConsumeRetrier(ConsumeRetrier):
    def __init__(
        self,
        consumed_event_retry_repository: ConsumedEventRetryRepository,
        max_retries: int = 1,
    ):
        self.__consumed_event_retry_repository = consumed_event_retry_repository
        self.__max_retries = max_retries
        self.__check_max_retries_positive()

    def __check_max_retries_positive(self) -> None:
        if self.__max_retries < 0:
            raise InvalidMaxRetriesParamException(self.__max_retries)

    def should_retry(self, event: Event, subscribers: list[Subscriber]) -> bool:
        consumed_event_retry = self.__consumed_event_retry_repository.find_one_by_event_and_subscriber(
            event, subscribers
        )
        return consumed_event_retry.retries < self.__max_retries

    def register_retry(self, event: Event, subscribers: list[Subscriber]) -> None:
        consumed_event_retry = self.__consumed_event_retry_repository.find_one_by_event_and_subscriber(
            event, subscribers
        )
        consumed_event_retry.register_retry()
        self.__consumed_event_retry_repository.save(consumed_event_retry)
