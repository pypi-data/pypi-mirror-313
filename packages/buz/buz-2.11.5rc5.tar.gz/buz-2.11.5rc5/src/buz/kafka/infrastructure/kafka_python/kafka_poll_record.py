from __future__ import annotations

from typing import Optional, Union


class KafkaPollRecord:
    key: Optional[Union[str, bytes]]
    headers: list[tuple[str, bytes]]
    value: Optional[bytes]
    partition: int
    topic: str
    offset: int
