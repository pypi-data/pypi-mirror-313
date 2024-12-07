from abc import abstractmethod
from typing import TypeVar, Any, Generic

from . import BasicClient
from .dto import RequestWithHeaders, Headers

R = TypeVar("R", bound=RequestWithHeaders)
H = TypeVar("H", bound=Headers)
type DictValue = str | int | str


class HeaderClient(BasicClient, Generic[R, H]):
    """
    Базовый класс, который одним из параметров запроса принимает Headers.
    Ниже представлен пример наследования класса

    from dataclasses import dataclass
    from typing import Any

    from agi_med_protos.dto import Headers, RequestWithHeaders
    from agi_med_protos.header_client import HeaderClient, DictValue



    class FooHeaders(Headers):
        some_value: str


    @dataclass
    class FooRequest(RequestWithHeaders[FooHeaders]):
        text: str


    class FooClient(HeaderClient[FooRequest, FooHeaders]):
        def __call__(self, request: FooRequest) -> float:
            metadata: list[tuple[str, DictValue]] = self._generate_metadata(request.headers, request.text)
            print(metadata)
            return 0.91

        def _generate_metadata(
                self, headers: FooHeaders, text: str | None = None, **_: Any
        ) -> list[tuple[str, DictValue]]:
            if text is None:
                text = "really_need_information"
            headers["additional_headers"] = {
                "text": text
            }
            return super()._generate_metadata(headers)

    """

    @abstractmethod
    def __call__(self, request: R) -> Any:
        pass

    def _generate_metadata(self, headers: H, **_: Any) -> list[tuple[str, DictValue]]:
        items: list[tuple[str, DictValue]] = []
        stack: list[dict[str, DictValue | dict] | H] = [headers]
        while stack:
            current_dict: dict[str, DictValue | dict] | H = stack.pop()
            for key, value in current_dict.items():

                if isinstance(value, dict):
                    stack.append(value)
                elif isinstance(value, (int, str, bool)):
                    items.append((key, value))
                else:
                    raise AttributeError(f"Incorrect value type! key={key} value={value}, type={type(value)}")
        return items
