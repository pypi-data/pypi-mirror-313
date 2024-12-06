from classiq.interface.generator.functions.classical_type import (
    ClassicalArray,
    ClassicalList,
)
from classiq.interface.generator.functions.concrete_types import ConcreteClassicalType
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.quantum_function_declaration import PositionalArg

from classiq import ClassicalParameterDeclaration
from classiq.qmod.semantics.error_manager import append_error


def validate_main_function(func: NativeFunctionDefinition) -> None:
    for param in func.positional_arg_declarations:
        _validate_main_param(param)


def _validate_main_param(param: PositionalArg) -> None:
    if isinstance(param, ClassicalParameterDeclaration):
        _validate_main_classical_param_type(param.classical_type, param.name)


def _validate_main_classical_param_type(
    param: ConcreteClassicalType, param_name: str
) -> None:
    if isinstance(param, ClassicalList):
        append_error(
            param,
            f"Classical array parameter {param_name!r} of function 'main' must must "
            f"specify array length",
        )
    if isinstance(param, ClassicalArray):
        _validate_main_classical_param_type(param.element_type, param_name)
