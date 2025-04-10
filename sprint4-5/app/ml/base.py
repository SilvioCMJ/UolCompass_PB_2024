from abc import ABC, abstractmethod
from typing import Generic, TypeVar


T = TypeVar("T")


class MLModelHandlerInterface(ABC, Generic[T]):
    @abstractmethod
    def load_model(self) -> T:
        """Carrega um modelo de ML serializado."""
        ...
