from abc import ABC
from typing import Self

from grpc import insecure_channel


class AbstractClient(ABC):
    def __init__(self, address: str) -> None:
        self._channel = insecure_channel(address)

    # https://stackoverflow.com/a/65131927
    def close(self) -> None:
        self._channel.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self) -> None:
        self.close()
