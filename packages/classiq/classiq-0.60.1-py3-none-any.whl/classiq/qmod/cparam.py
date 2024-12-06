import sys
from typing import (  # type: ignore[attr-defined]
    TYPE_CHECKING,
    Any,
    Generic,
    Union,
    _GenericAlias,
)

from typing_extensions import ParamSpec

from classiq.qmod.symbolic_expr import Symbolic, SymbolicExpr

if TYPE_CHECKING:
    from classiq.qmod.qmod_variable import QNum

    SymbolicSuperclass = SymbolicExpr
else:
    SymbolicSuperclass = Symbolic


class CParam(SymbolicSuperclass):
    def __init__(self, expr: str) -> None:
        super().__init__(expr, False)


class CInt(CParam):
    pass


class CReal(CParam):
    pass


class CBool(CParam):
    pass


_P = ParamSpec("_P")


class ArrayBase(Generic[_P]):
    # Support comma-separated generic args in older Python versions
    if sys.version_info[0:2] < (3, 10):

        def __class_getitem__(cls, args) -> _GenericAlias:
            return _GenericAlias(cls, args)


class CArray(CParam, ArrayBase[_P]):
    if TYPE_CHECKING:

        @property
        def len(self) -> int: ...

        def __getitem__(self, idx: Union[int, CInt, slice, "QNum"]) -> Any: ...


Array = CArray


class CParamScalar(CParam, SymbolicExpr):
    def __hash__(self) -> int:
        return hash(str(self))
