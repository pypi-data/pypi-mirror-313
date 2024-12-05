from dataclasses import dataclass


@dataclass(frozen=True)
class KafkaTopic:
    name: str
    partitions: int = 1
    replication_factor: int = 1
