from logging import Logger
from typing import Optional, Callable, cast

from kombu import Connection, Queue, Consumer as MessageConsumer, Message
from kombu.mixins import ConsumerMixin
from kombu.transport.pyamqp import Channel

from buz.event import Event, Subscriber
from buz.event.infrastructure.kombu.allowed_kombu_serializer import AllowedKombuSerializer
from buz.event.exceptions.term_signal_interruption_exception import TermSignalInterruptionException
from buz.event.middleware import ConsumeMiddleware, ConsumeMiddlewareChainResolver
from buz.event.middleware.exceptions.event_already_in_progress_exception import EventAlreadyInProgressException
from buz.locator import Locator
from buz.event.consumer import Consumer
from buz.event.exceptions.event_restore_exception import EventRestoreException
from buz.event.exceptions.subscribers_not_found_exception import SubscribersNotFoundException
from buz.event.strategies.retry.consume_retrier import ConsumeRetrier
from buz.event.strategies.retry.reject_callback import RejectCallback

QueueToSubscriberFqnMapping = dict[Queue, set[str]]


class KombuConsumer(ConsumerMixin, Consumer):
    def __init__(
        self,
        connection: Connection,
        queues_mapping: QueueToSubscriberFqnMapping,
        serializer: AllowedKombuSerializer,
        prefetch_count: int,
        locator: Locator[Event, Subscriber],
        logger: Logger,
        consume_retrier: Optional[ConsumeRetrier] = None,
        reject_callback: Optional[RejectCallback] = None,
        consume_middlewares: Optional[list[ConsumeMiddleware]] = None,
    ):
        self.connection = connection
        self.__queues_mapping = queues_mapping
        self.__serializer = serializer
        self.__prefetch_count = prefetch_count
        self.__locator = locator
        self.__logger = logger
        self.__consume_retrier = consume_retrier
        self.__reject_callback = reject_callback
        self.__consume_middleware_chain_resolver = ConsumeMiddlewareChainResolver(consume_middlewares or [])

    def stop(self) -> None:
        self.should_stop = True

    def get_consumers(self, consumer_factory: Callable, channel: Channel) -> list[MessageConsumer]:
        return [
            consumer_factory(
                queues=[queue],
                callbacks=self.__get_consumer_callbacks(allowed_subscriber_fqns),
                prefetch_count=self.__prefetch_count,
                accept=[self.__serializer],
            )
            for queue, allowed_subscriber_fqns in self.__queues_mapping.items()
        ]

    def __get_consumer_callbacks(self, allowed_subscriber_fqns: set[str]) -> list[Callable[[dict, Message], None]]:
        return [lambda body, message: self.__on_message_received(body, message, allowed_subscriber_fqns)]

    def __on_message_received(self, body: dict, message: Message, allowed_subscriber_fqns: set[str]) -> None:
        try:
            event = self.__restore_event(body, message)
            subscribers = self.__subscribers(event, allowed_subscriber_fqns)
        except (EventRestoreException, SubscribersNotFoundException) as exc:
            self.__logger.exception(f"Message cannot be processed: {exc}")
            message.ack()
            return
        except Exception as exc:
            self.__logger.exception(f"Unknown error while processing message: {exc}")
            message.ack()
            return

        self.__consume_event(message, event, subscribers)

    def __restore_event(self, body: dict, message: Message) -> Event:
        try:
            event_fqn = message.headers["fqn"]
            event_klass = self.__locator.get_message_klass_by_fqn(event_fqn)
            return cast(Event, event_klass.restore(**body))
        except Exception as exc:
            raise EventRestoreException(body, str(message)) from exc

    def __subscribers(self, event: Event, allowed_subscriber_fqns: set[str]) -> list[Subscriber]:
        event_subscribers = None
        try:
            event_subscribers = self.__locator.get(event)
            allowed_event_subscribers = [
                subscriber for subscriber in event_subscribers if subscriber.fqn() in allowed_subscriber_fqns
            ]
            if len(allowed_event_subscribers) == 0:
                raise SubscribersNotFoundException(event, allowed_subscriber_fqns, event_subscribers)

            return allowed_event_subscribers
        except Exception as exc:
            raise SubscribersNotFoundException(event, allowed_subscriber_fqns, event_subscribers) from exc

    def __consume_event(self, message: Message, event: Event, subscribers: list[Subscriber]) -> None:
        try:
            if self.should_stop is True:
                raise TermSignalInterruptionException()

            for subscriber in subscribers:
                self.__consume_middleware_chain_resolver.resolve(event, subscriber, self.__perform_consume)
            message.ack()
        except Exception as exc:
            self.__on_consume_exception(message, event, subscribers, exc)

    def __perform_consume(self, event: Event, subscriber: Subscriber) -> None:
        subscriber.consume(event)

    def __on_consume_exception(
        self, message: Message, event: Event, subscribers: list[Subscriber], exception: Exception
    ) -> None:
        if isinstance(exception, EventAlreadyInProgressException) or isinstance(
            exception, TermSignalInterruptionException
        ):
            message.requeue()
            return

        self.__logger.warning(
            f"Event {event.id} could not be consumed by subscribers {[subscriber.fqn() for subscriber in subscribers]}:"
            f"{exception}."
        )

        if self.__consume_retrier is None:
            self.__reject_message(message, event, subscribers)
            return

        should_retry = self.__consume_retrier.should_retry(event, subscribers)
        if should_retry is True:
            self.__consume_retrier.register_retry(event, subscribers)
            message.requeue()
            return

        self.__reject_message(message, event, subscribers)

    def __reject_message(self, message: Message, event: Event, subscribers: list[Subscriber]) -> None:
        message.reject()
        if self.__reject_callback is not None:
            self.__reject_callback.on_reject(event, subscribers)
