from collections.abc import Mapping
from typing import Any

from sympy import Symbol

from classiq.interface.exceptions import ClassiqValueError
from classiq.interface.generator.expressions.qmod_sized_proxy import QmodSizedProxy
from classiq.interface.model.handle_binding import HandleBinding


class QmodQScalarProxy(Symbol, QmodSizedProxy):
    def __new__(cls, handle: HandleBinding, **assumptions: bool) -> "QmodQScalarProxy":
        return super().__new__(cls, str(handle), **assumptions)

    def __init__(self, handle: HandleBinding, size: int) -> None:
        super().__init__(handle, size)


class QmodQBitProxy(QmodQScalarProxy):
    def __init__(self, handle: HandleBinding) -> None:
        super().__init__(handle, 1)

    @property
    def type_name(self) -> str:
        return "Quantum bit"


class QmodQNumProxy(QmodQScalarProxy):
    def __init__(
        self, handle: HandleBinding, size: int, fraction_digits: int, is_signed: bool
    ) -> None:
        super().__init__(handle, size)
        if fraction_digits > size:
            raise ClassiqValueError(
                f"Quantum numeric of size {size} cannot have {fraction_digits} "
                f"fraction digits"
            )
        self._fraction_digits = fraction_digits
        self._is_signed = is_signed

    @property
    def type_name(self) -> str:
        return "Quantum numeric"

    @property
    def fraction_digits(self) -> int:
        return self._fraction_digits

    @property
    def is_signed(self) -> bool:
        return self._is_signed

    @property
    def fields(self) -> Mapping[str, Any]:
        return {
            **super().fields,
            "is_signed": self.is_signed,
            "fraction_digits": self.fraction_digits,
        }
