from typing import TYPE_CHECKING, Optional, Union

from classiq.interface.generator.functions.type_name import TypeName
from classiq.interface.model.handle_binding import (
    ConcreteHandleBinding,
    FieldHandleBinding,
    HandleBinding,
    NestedHandleBinding,
    SlicedHandleBinding,
    SubscriptHandleBinding,
)
from classiq.interface.model.quantum_type import QuantumBitvector, QuantumType

import classiq.qmod.semantics.error_manager as error_manager
from classiq.qmod.model_state_container import QMODULE

if TYPE_CHECKING:
    from classiq.qmod.semantics.static_semantics_visitor import StaticScope


def resolve_handle(scope: "StaticScope", handle: HandleBinding) -> None:
    if handle.name not in scope.variables_to_types:
        error_manager.append_error(handle, f"Variable {handle.name!r} is undefined.")
        return
    _resolve_handle_recursively(scope.variables_to_types[handle.name], handle)


def _resolve_handle_recursively(
    qtype: QuantumType, handle: ConcreteHandleBinding
) -> Optional[QuantumType]:
    if isinstance(handle, NestedHandleBinding):
        return _resolve_nested_handle(qtype, handle)
    return qtype


def _resolve_nested_handle(
    qtype: QuantumType, handle: NestedHandleBinding
) -> Optional[QuantumType]:
    nested_qtype = _resolve_handle_recursively(qtype, handle.base_handle)
    if nested_qtype is None:
        return None
    if isinstance(handle, (SubscriptHandleBinding, SlicedHandleBinding)):
        return _resolve_subscript_sliced_handle(nested_qtype, handle)
    if TYPE_CHECKING:
        assert isinstance(handle, FieldHandleBinding)
    return _resolve_field_handle(nested_qtype, handle)


def _resolve_subscript_sliced_handle(
    qtype: QuantumType, handle: Union[SubscriptHandleBinding, SlicedHandleBinding]
) -> Optional[QuantumType]:
    if not isinstance(qtype, QuantumBitvector):
        error_manager.append_error(handle, f"{qtype.type_name} is not subscriptable.")
        return None
    return qtype.element_type if isinstance(handle, SubscriptHandleBinding) else qtype


def _validate_field_access(qtype: QuantumType, handle: FieldHandleBinding) -> bool:
    if not isinstance(qtype, TypeName):
        error_manager.append_error(handle, f"{qtype.type_name} has no fields.")
        return False
    if qtype.name not in QMODULE.qstruct_decls:
        error_manager.append_error(
            handle, f"{qtype.type_name} is not a quantum struct."
        )
        return False
    if handle.field not in qtype.fields:
        error_manager.append_error(
            handle,
            f"Struct {qtype.type_name} has no field {handle.field!r}. "
            f"Available fields: {', '.join(qtype.fields.keys())}",
        )
        return False

    return True


def _resolve_field_handle(
    qtype: QuantumType, handle: FieldHandleBinding
) -> Optional[QuantumType]:
    if _validate_field_access(qtype, handle):
        if TYPE_CHECKING:
            assert isinstance(qtype, TypeName)
        return qtype.fields[handle.field]
    return None
