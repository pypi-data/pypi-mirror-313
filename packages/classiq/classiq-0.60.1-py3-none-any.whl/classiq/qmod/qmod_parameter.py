from typing import TYPE_CHECKING, Any, Union

from classiq.interface.exceptions import ClassiqValueError
from classiq.interface.generator.functions.classical_type import (
    Bool,
    ClassicalArray,
    ClassicalList,
    ClassicalType,
    Integer,
    Real,
)
from classiq.interface.generator.functions.type_name import Struct, TypeName

from classiq.qmod.builtins.structs import BUILTIN_STRUCT_DECLARATIONS
from classiq.qmod.cparam import (  # noqa: F401
    Array,
    ArrayBase,
    CArray,
    CBool,
    CInt,
    CParam,
    CParamScalar,
    CReal,
)
from classiq.qmod.model_state_container import ModelStateContainer
from classiq.qmod.symbolic_expr import Symbolic, SymbolicExpr

if TYPE_CHECKING:

    SymbolicSuperclass = SymbolicExpr
else:
    SymbolicSuperclass = Symbolic


class CParamList(CParam):
    def __init__(
        self,
        expr: str,
        list_type: Union[ClassicalList, ClassicalArray],
        qmodule: ModelStateContainer,
    ) -> None:
        super().__init__(expr)
        self._qmodule = qmodule
        self._list_type = list_type

    def __getitem__(self, key: Any) -> CParam:
        param_type = self._list_type.element_type
        if isinstance(key, slice):
            param_type = self._list_type
            start = key.start if key.start is not None else ""
            stop = key.stop if key.stop is not None else ""
            if key.step is not None:
                key = f"{start}:{key.step}:{stop}"
            else:
                key = f"{start}:{stop}"
        return create_param(
            f"({self})[{key}]",
            param_type,
            qmodule=self._qmodule,
        )

    def __len__(self) -> int:
        raise ClassiqValueError(
            "len(<expr>) is not supported for QMod lists - use <expr>.len instead"
        )

    @property
    def len(self) -> CParamScalar:
        return CParamScalar(f"get_field({self}, 'len')")


class CParamStruct(CParam):
    def __init__(
        self, expr: str, struct_type: Struct, *, qmodule: ModelStateContainer
    ) -> None:
        super().__init__(expr)
        self._qmodule = qmodule
        self._struct_type = struct_type

    def __getattr__(self, field_name: str) -> CParam:
        return CParamStruct.get_field(
            self._qmodule, str(self), self._struct_type.name, field_name
        )

    @staticmethod
    def get_field(
        qmodule: ModelStateContainer,
        variable_name: str,
        struct_name: str,
        field_name: str,
    ) -> CParam:
        struct_decl = BUILTIN_STRUCT_DECLARATIONS.get(
            struct_name, qmodule.type_decls.get(struct_name)
        )
        assert struct_decl is not None
        field_type = struct_decl.variables.get(field_name)
        if field_type is None:
            raise ClassiqValueError(
                f"{struct_name} {variable_name!r} has no field {field_name!r}. "
                f"Available fields: {', '.join(struct_decl.variables.keys())}"
            )

        return create_param(
            f"get_field({variable_name},{field_name!r})",
            field_type,
            qmodule=qmodule,
        )


def create_param(
    expr_str: str, ctype: ClassicalType, qmodule: ModelStateContainer
) -> CParam:
    if isinstance(ctype, (ClassicalList, ClassicalArray)):
        return CParamList(expr_str, ctype, qmodule=qmodule)
    elif isinstance(ctype, Struct):
        return CParamStruct(expr_str, ctype, qmodule=qmodule)
    else:
        return CParamScalar(expr_str)


def get_qmod_type(ctype: ClassicalType) -> type:
    if isinstance(ctype, Integer):
        return CInt
    elif isinstance(ctype, Real):
        return CReal
    elif isinstance(ctype, Bool):
        return CBool
    elif isinstance(ctype, ClassicalList):
        return CArray[get_qmod_type(ctype.element_type)]  # type: ignore[misc]
    elif isinstance(ctype, ClassicalArray):
        return CArray[get_qmod_type(ctype.element_type), ctype.size]  # type: ignore[misc]
    elif isinstance(ctype, TypeName):
        type_ = type(ctype.name, (TypeName,), dict())
        if isinstance(ctype, Struct):
            type_.__dataclass_fields__ = []  # type:ignore[attr-defined]
        return type_
    raise NotImplementedError(
        f"{ctype.__class__.__name__!r} has no QMOD SDK equivalent"
    )
