from typing import Optional, Sequence

from buz.event import Event, Subscriber


class SubscribersNotFoundException(Exception):
    def __init__(
        self, event: Event, allowed_subscriber_fqns: set[str], event_subscribers: Optional[Sequence[Subscriber]] = None
    ) -> None:
        self.event = event
        self.allowed_subscriber_fqns = allowed_subscriber_fqns
        self.event_subscribers = event_subscribers

        message = f"Subscribers not found for event {event}. Allowed subscriber FQNs: {allowed_subscriber_fqns}."
        if event_subscribers is not None:
            message += f" All event subscribers found: {event_subscribers}"

        super().__init__(message)
