
from abc import ABC, abstractmethod


class Registrable(ABC):
    @abstractmethod
    def to_register_json(self) -> dict:
        """Returns a JSON representation for registration."""
        pass