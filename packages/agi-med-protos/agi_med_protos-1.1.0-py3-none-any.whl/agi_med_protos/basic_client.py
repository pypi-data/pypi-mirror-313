from abc import abstractmethod
from typing import Generic, TypeVar, Any

from . import AbstractClient
from .dto import BaseRequest

T = TypeVar("T", bound=BaseRequest)


class BasicClient(AbstractClient, Generic[T]):
    @abstractmethod
    def __call__(self, request: T) -> Any:
        pass
