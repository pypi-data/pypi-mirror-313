import itertools
from collections import UserDict
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from functools import singledispatch
from typing import TYPE_CHECKING, Any, Optional, TypeVar, Union

from classiq.interface.exceptions import (
    ClassiqExpansionError,
    ClassiqInternalExpansionError,
)
from classiq.interface.generator.expressions.evaluated_expression import (
    EvaluatedExpression,
)
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.expressions.qmod_qarray_proxy import (
    ILLEGAL_SLICE_BOUNDS_MSG,
)
from classiq.interface.generator.expressions.qmod_struct_instance import (
    QmodStructInstance,
)
from classiq.interface.generator.functions.type_name import TypeName
from classiq.interface.model.handle_binding import (
    FieldHandleBinding,
    HandleBinding,
    SlicedHandleBinding,
    SubscriptHandleBinding,
)
from classiq.interface.model.quantum_function_call import ArgValue
from classiq.interface.model.quantum_type import (
    QuantumBitvector,
    QuantumType,
)

if TYPE_CHECKING:
    from classiq.model_expansions.closure import FunctionClosure

T = TypeVar("T")


@dataclass(frozen=True)
class QuantumSymbol:
    handle: HandleBinding
    quantum_type: QuantumType

    @property
    def is_subscript(self) -> bool:
        return isinstance(self.handle, (SubscriptHandleBinding, SlicedHandleBinding))

    def emit(self) -> HandleBinding:
        return self.handle

    def __getitem__(self, item: Union[slice, int]) -> "QuantumSymbol":
        if isinstance(item, int):
            return self._subscript(item)

        return self._slice(item.start, item.stop)

    def _slice(self, start: int, end: int) -> "QuantumSymbol":
        if not isinstance(self.quantum_type, QuantumBitvector):
            raise ClassiqExpansionError(
                f"{self.quantum_type.type_name} is not subscriptable."
            )
        if start >= end:
            raise ClassiqExpansionError(ILLEGAL_SLICE_BOUNDS_MSG.format(start, end))
        if (
            self.quantum_type.has_length
            and end - start > self.quantum_type.length_value
        ):
            raise ClassiqExpansionError(
                f"Slice [{start}:{end}] is out of bounds for {self.handle}."
            )
        return QuantumSymbol(
            handle=SlicedHandleBinding(
                base_handle=self.handle,
                start=Expression(expr=str(start)),
                end=Expression(expr=str(end)),
            ),
            quantum_type=QuantumBitvector(
                element_type=self.quantum_type.element_type,
                length=Expression(expr=str(end - start)),
            ),
        )

    def _subscript(self, index: int) -> "QuantumSymbol":
        if not isinstance(self.quantum_type, QuantumBitvector):
            raise ClassiqExpansionError(
                f"{self.quantum_type.type_name} is not subscriptable."
            )
        if (
            index < 0
            or self.quantum_type.has_length
            and index > self.quantum_type.length_value
        ):
            raise ClassiqExpansionError(
                f"Subscript [{index}] is out of bounds for {self.handle}."
            )
        return QuantumSymbol(
            handle=SubscriptHandleBinding(
                base_handle=self.handle,
                index=Expression(expr=str(index)),
            ),
            quantum_type=self.quantum_type.element_type,
        )

    @property
    def fields(self) -> dict[str, "QuantumSymbol"]:
        quantum_type = self.quantum_type
        if not isinstance(quantum_type, TypeName):
            raise ClassiqExpansionError(
                f"{self.quantum_type.type_name} is not a struct"
            )
        return {
            field_name: QuantumSymbol(
                handle=FieldHandleBinding(base_handle=self.handle, field=field_name),
                quantum_type=field_type,
            )
            for field_name, field_type in quantum_type.fields.items()
        }


@singledispatch
def evaluated_to_str(value: Any) -> str:
    return str(value)


@evaluated_to_str.register
def _evaluated_to_str_list(value: list) -> str:
    return f"[{', '.join(evaluated_to_str(x) for x in value)}]"


@evaluated_to_str.register
def _evaluated_to_str_struct_literal(value: QmodStructInstance) -> str:
    return f"struct_literal({value.struct_declaration.name}, {', '.join(f'{k}={evaluated_to_str(v)}' for k, v in value.fields.items())})"


@dataclass(frozen=True)
class Evaluated:  # FIXME: Merge with EvaluatedExpression if possible
    value: Any
    defining_function: Optional["FunctionClosure"] = None

    def as_type(self, t: type[T]) -> T:
        if t is int:
            return self._as_int()  # type: ignore[return-value]

        if not isinstance(self.value, t):
            raise ClassiqExpansionError(
                f"Invalid access to expression {self.value!r} as {t}"
            )

        return self.value

    def _as_int(self) -> int:
        if not isinstance(self.value, (int, float)):
            raise ClassiqExpansionError(
                f"Invalid access to expression {self.value!r} as {int}"
            )

        return int(self.value)

    def emit(self) -> ArgValue:
        if isinstance(self.value, QuantumSymbol):
            return self.value.emit()

        ret = Expression(expr=evaluated_to_str(self.value))
        ret._evaluated_expr = EvaluatedExpression(value=self.value)
        return ret


if TYPE_CHECKING:
    EvaluatedUserDict = UserDict[str, Evaluated]
else:
    EvaluatedUserDict = UserDict


class Scope(EvaluatedUserDict):
    def __init__(
        self,
        data: Optional[dict[str, Evaluated]] = None,
        /,
        *,
        parent: Optional["Scope"] = None,
    ) -> None:
        super().__init__(data or {})
        self._parent: Optional["Scope"] = parent

    @property
    def parent(self) -> Optional["Scope"]:
        return self._parent

    def __getitem__(self, name: str) -> Evaluated:
        if name in self.data:
            return self.data[name]
        if self._parent is not None:
            return self._parent[name]
        raise ClassiqExpansionError(f"Variable {name!r} is undefined")

    def __contains__(self, item: Any) -> bool:
        return item in self.data or (self._parent is not None and item in self._parent)

    def __iter__(self) -> Iterator[str]:
        if self._parent is None:
            return iter(self.data)
        return iter(itertools.chain(self.data, self._parent))

    def iter_without_top_level(self) -> Iterator[str]:
        if self.parent is None:
            return iter(tuple())
        return iter(itertools.chain(self.data, self.parent.iter_without_top_level()))

    def __or__(self, other: Any) -> "Scope":  # type: ignore[override]
        if not (isinstance(other, Scope) and isinstance(self, Scope)):
            raise ClassiqInternalExpansionError

        if self.parent is None:
            parent = other.parent
        elif other.parent is None:
            parent = self.parent
        else:
            parent = self.parent | other.parent

        return Scope(
            (self.data or {}) | (other.data or {}),
            parent=parent,
        )

    def _copy(self) -> "Scope":
        return Scope(
            self.data, parent=None if self._parent is None else self._parent.copy()
        )

    @contextmanager
    def freeze(self) -> Iterator[None]:
        previous = self._copy()
        yield
        self.data = previous.data
        self._parent = previous._parent
