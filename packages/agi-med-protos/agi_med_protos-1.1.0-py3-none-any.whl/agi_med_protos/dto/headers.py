from typing import NotRequired, TypedDict


class Headers(TypedDict):
    extra_uuid: str
    additional_headers: NotRequired[dict[str, int | str | bool]]
