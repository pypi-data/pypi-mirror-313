from typing import Union

from classiq.interface.exceptions import (
    ClassiqExpansionError,
    ClassiqInternalExpansionError,
)
from classiq.interface.generator.functions.concrete_types import ConcreteQuantumType
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.generator.functions.type_name import (
    TypeName,
)
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_declaration import (
    PositionalArg,
    QuantumOperandDeclaration,
)
from classiq.interface.model.quantum_type import (
    QuantumBit,
    QuantumBitvector,
    QuantumNumeric,
    QuantumType,
)

from classiq.model_expansions.closure import FunctionClosure
from classiq.model_expansions.evaluators.arg_type_match import check_type_match
from classiq.model_expansions.evaluators.classical_expression import (
    evaluate_classical_expression,
)
from classiq.model_expansions.evaluators.quantum_type_utils import (
    copy_type_information,
    set_element_type,
    set_fraction_digits,
    set_is_signed,
    set_length,
    set_size,
)
from classiq.model_expansions.scope import Evaluated, QuantumSymbol, Scope


def evaluate_parameter_types_from_args(
    closure: FunctionClosure, signature_scope: Scope, arguments: list[Evaluated]
) -> list[PositionalArg]:
    parameters = closure.positional_arg_declarations
    function_name = closure.name
    check_type_match(parameters, arguments, function_name)

    for parameter, argument in zip(parameters, arguments):
        _update_scope(parameter, argument, closure)

    parameter_names = {parameter.name for parameter in parameters}
    for parameter in parameters:
        if isinstance(parameter, QuantumOperandDeclaration):
            parameter_value = closure.scope[parameter.name].value
            _update_operand_signature_environment(
                parameter_value, parameter_names, closure
            )

    return [
        _evaluate_type_from_arg(
            parameter, argument, Scope(parent=closure.scope | signature_scope)
        )
        for parameter, argument in zip(parameters, arguments)
    ]


def _update_scope(
    parameter: PositionalArg, argument: Evaluated, closure: FunctionClosure
) -> None:
    if not isinstance(parameter, PortDeclaration):
        closure.scope[parameter.name] = argument
        return
    if parameter.direction is PortDeclarationDirection.Output:
        return
    quantum_symbol = argument.as_type(QuantumSymbol)
    if not quantum_symbol.quantum_type.has_size_in_bits:
        raise ClassiqExpansionError(
            f"Argument {str(quantum_symbol.emit())!r} to function {closure.name!r} "
            f"is not initialized"
        )
    casted_argument = _cast(
        parameter.quantum_type,
        quantum_symbol,
        parameter.name,
    )
    closure.scope[parameter.name] = Evaluated(
        value=casted_argument, defining_function=closure
    )


NestedFunctionClosureT = Union[FunctionClosure, list["NestedFunctionClosureT"]]


def _update_operand_signature_environment(
    operand_val: NestedFunctionClosureT,
    parameter_names: set[str],
    closure: FunctionClosure,
) -> None:
    # We update the environment (parent) of the operand by adding closure.scope.data,
    # which includes the parameters that appear in the function's signature only.
    if isinstance(operand_val, list):
        for operand in operand_val:
            _update_operand_signature_environment(operand, parameter_names, closure)
        return
    if not isinstance(operand_val, FunctionClosure):
        raise ClassiqInternalExpansionError
    operand_val.signature_scope.update(
        {
            identifier: value
            for identifier, value in closure.scope.data.items()
            if identifier in parameter_names
        }
    )


def _cast(
    quantum_type: QuantumType, quantum_symbol: QuantumSymbol, param_name: str
) -> QuantumSymbol:
    updated_quantum_type = quantum_type.model_copy()
    _inject_quantum_arg_info_to_type(updated_quantum_type, quantum_symbol, param_name)
    return QuantumSymbol(
        handle=quantum_symbol.handle, quantum_type=updated_quantum_type
    )


def _evaluate_type_from_arg(
    parameter: PositionalArg, argument: Evaluated, inner_scope: Scope
) -> PositionalArg:
    if not isinstance(parameter, PortDeclaration):
        return parameter

    updated_quantum_type: QuantumType = evaluate_type_in_quantum_symbol(
        parameter.quantum_type.model_copy(), inner_scope, parameter.name
    )
    if parameter.direction != PortDeclarationDirection.Output:
        updated_quantum_type = _inject_quantum_arg_info_to_type(
            updated_quantum_type, argument.as_type(QuantumSymbol), parameter.name
        )
    return parameter.model_copy(update={"quantum_type": updated_quantum_type})


def evaluate_type_in_quantum_symbol(
    type_to_update: QuantumType, scope: Scope, param_name: str
) -> ConcreteQuantumType:
    if isinstance(type_to_update, QuantumBitvector):
        return _evaluate_qarray_in_quantum_symbol(type_to_update, scope, param_name)
    elif isinstance(type_to_update, QuantumNumeric):
        return _evaluate_qnum_in_quantum_symbol(type_to_update, scope, param_name)
    elif isinstance(type_to_update, TypeName):
        return _evaluate_qstruct_in_quantum_symbol(type_to_update, scope, param_name)
    else:
        assert isinstance(type_to_update, QuantumBit)
        return type_to_update


def _evaluate_qarray_in_quantum_symbol(
    type_to_update: QuantumBitvector, scope: Scope, param_name: str
) -> QuantumBitvector:
    new_element_type = evaluate_type_in_quantum_symbol(
        type_to_update.element_type, scope, param_name
    )
    set_element_type(type_to_update, new_element_type)
    if type_to_update.length is not None:
        new_length = evaluate_classical_expression(
            type_to_update.length, scope
        ).as_type(int)
        set_length(type_to_update, new_length)
    return type_to_update


def _evaluate_qnum_in_quantum_symbol(
    type_to_update: QuantumNumeric, scope: Scope, param_name: str
) -> QuantumNumeric:
    if type_to_update.is_signed is not None:
        new_is_sign = evaluate_classical_expression(
            type_to_update.is_signed, scope
        ).as_type(bool)
        set_is_signed(type_to_update, new_is_sign, param_name)
    if type_to_update.fraction_digits is not None:
        new_fraction_digits = evaluate_classical_expression(
            type_to_update.fraction_digits, scope
        ).as_type(int)
        set_fraction_digits(type_to_update, new_fraction_digits, param_name)
    if type_to_update.size is not None:
        new_size = evaluate_classical_expression(type_to_update.size, scope).as_type(
            int
        )
        set_size(type_to_update, new_size, param_name)
    return type_to_update


def _evaluate_qstruct_in_quantum_symbol(
    type_to_update: TypeName, scope: Scope, param_name: str
) -> TypeName:
    new_fields = {
        field_name: evaluate_type_in_quantum_symbol(field_type, scope, param_name)
        for field_name, field_type in type_to_update.fields.items()
    }
    type_to_update.set_fields(new_fields)
    return type_to_update


def evaluate_types_in_quantum_symbols(
    symbols: list[QuantumSymbol], scope: Scope
) -> list[QuantumSymbol]:
    return [
        QuantumSymbol(
            handle=symbol.handle,
            quantum_type=evaluate_type_in_quantum_symbol(
                symbol.quantum_type, scope, str(symbol.handle)
            ),
        )
        for symbol in symbols
    ]


def _inject_quantum_arg_info_to_type(
    parameter_type: QuantumType, quantum_symbol: QuantumSymbol, param_name: str
) -> QuantumType:
    copy_type_information(
        quantum_symbol.quantum_type,
        parameter_type,
        param_name,
    )
    return parameter_type
