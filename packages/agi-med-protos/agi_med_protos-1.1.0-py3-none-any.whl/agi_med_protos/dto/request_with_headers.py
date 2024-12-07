from dataclasses import dataclass
from typing import TypeVar, Generic

from . import Headers, BaseRequest

H = TypeVar("H", bound=Headers)


@dataclass
class RequestWithHeaders(BaseRequest, Generic[H]):
    headers: H
