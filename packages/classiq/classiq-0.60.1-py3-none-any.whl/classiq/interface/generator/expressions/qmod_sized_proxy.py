from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from classiq.interface.model.handle_binding import HandleBinding


class QmodSizedProxy:
    def __init__(self, handle: "HandleBinding", size: int) -> None:
        self._handle = handle
        self._size = size

    @property
    def size(self) -> int:
        return self._size

    def __str__(self) -> str:
        return str(self.handle)

    @property
    def type_name(self) -> str:
        raise NotImplementedError

    @property
    def handle(self) -> "HandleBinding":
        return self._handle

    @property
    def len(self) -> int:
        return self._size

    @property
    def fields(self) -> Mapping[str, Any]:
        return {"size": self._size}
