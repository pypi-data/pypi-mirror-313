from collections.abc import Mapping

from classiq.interface.exceptions import ClassiqError
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.model.handle_binding import HandleBinding
from classiq.interface.model.quantum_function_call import QuantumFunctionCall
from classiq.interface.model.quantum_function_declaration import (
    AnonQuantumFunctionDeclaration,
    AnonQuantumOperandDeclaration,
    QuantumFunctionDeclaration,
)
from classiq.interface.model.quantum_lambda_function import (
    QuantumLambdaFunction,
    QuantumOperand,
)

from classiq.qmod.semantics.error_manager import ErrorManager


def validate_call_arguments(
    fc: QuantumFunctionCall,
    function_dict: Mapping[str, QuantumFunctionDeclaration],
) -> None:
    pos_args = fc.positional_args
    pos_params = fc.func_decl.positional_arg_declarations
    if len(pos_args) != len(pos_params):
        ErrorManager().add_error(
            f"Function {fc.func_name} takes {len(pos_params)} arguments but "
            f"{len(pos_args)} were given."
        )
    for arg, param in zip(pos_args, pos_params):
        if not isinstance(arg, (Expression, HandleBinding)) and isinstance(
            param, AnonQuantumOperandDeclaration
        ):
            _check_operand_against_declaration(param, arg, function_dict, fc.func_name)
    check_no_overlapping_quantum_args(fc.ports, fc.func_name)


def _check_operand_against_declaration(
    operand_decl: AnonQuantumOperandDeclaration,
    operand_argument: QuantumOperand,
    function_dict: Mapping[str, QuantumFunctionDeclaration],
    func_name: str,
    in_list: bool = False,
) -> None:
    if isinstance(operand_argument, list):
        if in_list:
            ErrorManager().add_error(
                f"{str(operand_argument)!r} argument to {func_name!r} is not "
                f"a valid operand. Nested operand lists are not permitted."
            )
            return
        for arg in operand_argument:
            _check_operand_against_declaration(
                operand_decl, arg, function_dict, func_name, in_list=True
            )
        return
    operand_arg_decl: AnonQuantumFunctionDeclaration
    if isinstance(operand_argument, str):
        if operand_argument not in function_dict:
            ErrorManager().add_error(
                f"{operand_argument!r} argument to {func_name!r} is not a "
                f"registered function."
            )
            return
        operand_arg_decl = function_dict[operand_argument]
    elif isinstance(operand_argument, QuantumLambdaFunction):
        operand_arg_decl = operand_argument.func_decl
    else:
        raise ClassiqError(
            f"{str(operand_argument)!r} argument to {func_name!r} is not a "
            f"valid operand."
        )
    num_arg_parameters = len(operand_arg_decl.positional_arg_declarations)
    num_decl_parameters = len(operand_decl.positional_arg_declarations)
    if num_arg_parameters != num_decl_parameters:
        ErrorManager().add_error(
            f"Signature of argument {operand_argument!r} to {func_name!r} "
            f"does not match the signature of parameter {operand_decl.name!r}. "
            f"{operand_decl.name!r} accepts {num_decl_parameters} parameters but "
            f"{operand_argument!r} accepts {num_arg_parameters} parameters."
        )


def check_no_overlapping_quantum_args(
    args: list[HandleBinding], func_name: str
) -> None:
    for idx, arg in enumerate(args):
        for other_arg in args[idx + 1 :]:
            if arg.overlaps(other_arg):
                ErrorManager().add_error(
                    f"Cannot use the same part of variable {arg.name!r} in multiple "
                    f"arguments to function {func_name!r}."
                )
                break
