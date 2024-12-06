from collections.abc import Mapping

from classiq.interface.exceptions import ClassiqError
from classiq.interface.model.quantum_function_call import QuantumFunctionCall
from classiq.interface.model.quantum_function_declaration import (
    AnonQuantumOperandDeclaration,
    QuantumFunctionDeclaration,
)
from classiq.interface.model.quantum_lambda_function import (
    QuantumLambdaFunction,
)


def annotate_function_call_decl(
    fc: QuantumFunctionCall,
    function_dict: Mapping[str, QuantumFunctionDeclaration],
) -> None:
    if fc._func_decl is None:
        func_decl = function_dict.get(fc.func_name)
        if func_decl is None:
            raise ClassiqError(
                f"Error resolving function {fc.func_name}, the function is not found in included library."
            )
        fc.set_func_decl(func_decl)

    for arg, param in zip(fc.positional_args, fc.func_decl.positional_arg_declarations):
        if not isinstance(param, AnonQuantumOperandDeclaration):
            continue
        args: list
        if isinstance(arg, list):
            args = arg
        else:
            args = [arg]
        for qlambda in args:
            if isinstance(qlambda, QuantumLambdaFunction):
                qlambda.set_op_decl(param)
