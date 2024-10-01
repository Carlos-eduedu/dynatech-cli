from abc import ABC, abstractmethod
from typing import Any


class Exporter(ABC):
    @abstractmethod
    def export(self, data: Any) -> None:
        pass
