from dataclasses import dataclass


@dataclass(frozen=True)
class CDCPayload:
    payload: str  # json encoded
    event_id: str  # uuid
    created_at: str  # date and hour ISO 8601
    event_fqn: str

    def validate(self) -> None:
        if not isinstance(self.payload, str):
            raise ValueError("The payload value is not a valid value")
        if not isinstance(self.event_id, str):
            raise ValueError("The event_id value is not a valid value")
        if not isinstance(self.created_at, str):
            raise ValueError("The created_at value is not a value")
        if not isinstance(self.event_fqn, str):
            raise ValueError("The event_fqn value is not a valid value")

    def __post_init__(self) -> None:
        self.validate()


@dataclass(frozen=True)
class CDCMessage:
    payload: CDCPayload

    def validate(self) -> None:
        if not isinstance(self.payload, CDCPayload):
            raise ValueError("The payload value is not a valid value")

    def __post_init__(self) -> None:
        self.validate()
