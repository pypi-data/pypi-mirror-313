from abc import ABC, abstractmethod


class RebalanceReady(ABC):
    @abstractmethod
    def is_ready_for_rebalancing(self) -> bool:
        pass
