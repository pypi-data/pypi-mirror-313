from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Union

from sympy import Integer

from classiq.interface.exceptions import ClassiqValueError
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.expressions.non_symbolic_expr import NonSymbolicExpr
from classiq.interface.generator.expressions.qmod_sized_proxy import QmodSizedProxy
from classiq.interface.model.handle_binding import (
    HandleBinding,
    SlicedHandleBinding,
    SubscriptHandleBinding,
)

if TYPE_CHECKING:
    from classiq.interface.model.quantum_type import QuantumType


ILLEGAL_SLICING_STEP_MSG = "Slicing with a step of a quantum variable is not supported"
SLICE_OUT_OF_BOUNDS_MSG = "Slice indices out of bounds"
SUBSCRIPT_OUT_OF_BOUNDS_MSG = "Subscript index out of bounds"
ILLEGAL_SLICE_MSG = "Quantum array slice must be of the form [<int-value>:<int-value>]."
ILLEGAL_SLICE_BOUNDS_MSG = (
    "The quantum array slice start value ({}) must be lower than its stop value ({})."
)


class QmodQArrayProxy(NonSymbolicExpr, QmodSizedProxy):
    def __init__(
        self,
        handle: HandleBinding,
        element_type: "QuantumType",
        element_size: int,
        length: int,
    ) -> None:
        super().__init__(handle, element_size * length)
        self._length = length
        self._element_type = element_type
        self._element_size = element_size

    def __getitem__(self, key: Union[slice, int, Integer]) -> "QmodSizedProxy":
        return (
            self._get_slice(key) if isinstance(key, slice) else self._get_subscript(key)
        )

    def _get_subscript(self, index: Union[int, Integer]) -> "QmodSizedProxy":
        if isinstance(index, Integer):
            index = int(index)
        if index < 0 or index >= self._length:
            raise ClassiqValueError(SUBSCRIPT_OUT_OF_BOUNDS_MSG)

        return self._element_type.get_proxy(
            SubscriptHandleBinding(
                base_handle=self.handle,
                index=Expression(expr=str(index)),
            )
        )

    def _get_slice(self, slice_: slice) -> "QmodSizedProxy":
        if slice_.step is not None:
            raise ClassiqValueError(ILLEGAL_SLICING_STEP_MSG)
        if isinstance(slice_.start, Integer):
            slice_ = slice(int(slice_.start), slice_.stop)
        if isinstance(slice_.stop, Integer):
            slice_ = slice(slice_.start, int(slice_.stop))
        if not isinstance(slice_.start, int) or not isinstance(slice_.stop, int):
            raise ClassiqValueError(ILLEGAL_SLICE_MSG)
        if slice_.start >= slice_.stop:
            raise ClassiqValueError(
                ILLEGAL_SLICE_BOUNDS_MSG.format(slice_.start, slice_.stop)
            )
        if slice_.start < 0 or slice_.stop > self._length:
            raise ClassiqValueError(SLICE_OUT_OF_BOUNDS_MSG)

        return QmodQArrayProxy(
            SlicedHandleBinding(
                base_handle=self.handle,
                start=Expression(expr=str(slice_.start)),
                end=Expression(expr=str(slice_.stop)),
            ),
            self._element_type,
            self._element_size,
            slice_.stop - slice_.start,
        )

    @property
    def type_name(self) -> str:
        return "Quantum array"

    @property
    def len(self) -> int:
        return self._length

    @property
    def fields(self) -> Mapping[str, Any]:
        return {**super().fields, "len": self.len}

    @property
    def size(self) -> int:
        return self.len * self._element_size
