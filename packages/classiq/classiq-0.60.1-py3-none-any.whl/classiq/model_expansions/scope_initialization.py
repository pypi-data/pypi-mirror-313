from collections.abc import Sequence

from classiq.interface.exceptions import ClassiqError
from classiq.interface.generator.constant import Constant
from classiq.interface.generator.expressions.expression_constants import (
    CPARAM_EXECUTION_SUFFIX,
)
from classiq.interface.model.classical_parameter_declaration import (
    ClassicalParameterDeclaration,
)
from classiq.interface.model.handle_binding import HandleBinding
from classiq.interface.model.model import MAIN_FUNCTION_NAME, Model
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_declaration import PositionalArg

from classiq.model_expansions.closure import FunctionClosure, GenerativeFunctionClosure
from classiq.model_expansions.evaluators.classical_expression import (
    evaluate_classical_expression,
)
from classiq.model_expansions.evaluators.parameter_types import (
    evaluate_type_in_quantum_symbol,
)
from classiq.model_expansions.expression_renamer import ExpressionRenamer
from classiq.model_expansions.scope import Evaluated, QuantumSymbol, Scope
from classiq.qmod.builtins import BUILTIN_CONSTANTS
from classiq.qmod.builtins.functions import (
    CORE_LIB_DECLS,
    OPEN_LIB_DECLS,
    STD_QMOD_OPERATORS,
)
from classiq.qmod.quantum_function import GenerativeQFunc


def get_main_renamer(
    functions: Sequence[NativeFunctionDefinition],
) -> ExpressionRenamer:
    for func in functions:
        if func.name == MAIN_FUNCTION_NAME:
            return ExpressionRenamer.from_positional_arg_declarations(
                func.positional_arg_declarations, CPARAM_EXECUTION_SUFFIX
            )
    return ExpressionRenamer(var_mapping={})


def add_constants_to_scope(constants: list[Constant], scope: Scope) -> None:
    for constant in constants:
        scope[constant.name] = Evaluated(
            value=evaluate_classical_expression(constant.value, scope).value
        )


def _add_functions_to_scope(
    functions: list[NativeFunctionDefinition], scope: Scope
) -> None:
    for function in functions:
        scope[function.name] = Evaluated(
            value=FunctionClosure.create(
                name=function.name,
                positional_arg_declarations=function.positional_arg_declarations,
                body=function.body,
                scope=Scope(parent=scope),
            )
        )


def _add_generative_functions_to_scope(
    functions: list[GenerativeQFunc], scope: Scope
) -> None:
    for function in functions:
        scope[function.func_decl.name] = Evaluated(
            value=GenerativeFunctionClosure.create(
                name=function.func_decl.name,
                positional_arg_declarations=function.func_decl.positional_arg_declarations,
                scope=Scope(parent=scope),
                generative_blocks={"body": function},
            )
        )


def _init_builtins_scope(scope: Scope) -> None:
    for builtin_function in CORE_LIB_DECLS:
        scope[builtin_function.name] = Evaluated(
            value=FunctionClosure.create(
                name=builtin_function.name,
                positional_arg_declarations=builtin_function.positional_arg_declarations,
                scope=Scope(parent=scope),
                is_atomic=True,
            )
        )
    for builtin_function in STD_QMOD_OPERATORS:
        scope[builtin_function.name] = Evaluated(
            value=FunctionClosure.create(
                name=builtin_function.name,
                positional_arg_declarations=builtin_function.positional_arg_declarations,
                scope=Scope(parent=scope),
            )
        )
    for func_decl in OPEN_LIB_DECLS:
        if func_decl.name not in scope:
            scope[func_decl.name] = Evaluated(
                value=FunctionClosure.create(
                    name=func_decl.name,
                    positional_arg_declarations=func_decl.positional_arg_declarations,
                    scope=Scope(parent=scope),
                    is_atomic=True,
                )
            )
    for constant in BUILTIN_CONSTANTS:
        value = constant.value
        if not value.is_evaluated():
            raise ClassiqError(
                f"Unevaluated built-in constants not supported. Offending constant: "
                f"{constant.name} = {value}"
            )
        scope[constant.name] = Evaluated(value=value.value.value)


def add_entry_point_params_to_scope(
    parameters: Sequence[PositionalArg], main_closure: FunctionClosure
) -> None:
    for parameter in parameters:
        if isinstance(parameter, PortDeclaration):
            main_closure.scope[parameter.name] = Evaluated(
                value=QuantumSymbol(
                    handle=HandleBinding(name=parameter.name),
                    quantum_type=evaluate_type_in_quantum_symbol(
                        parameter.quantum_type, main_closure.scope, parameter.name
                    ),
                ),
                defining_function=main_closure,
            )
        elif isinstance(parameter, ClassicalParameterDeclaration):
            main_closure.scope[parameter.name] = Evaluated(
                value=parameter.classical_type.as_symbolic(parameter.name),
                defining_function=main_closure,
            )


def init_top_level_scope(
    model: Model, generative_functions: list[GenerativeQFunc], scope: Scope
) -> None:
    _add_functions_to_scope(model.functions, scope)
    _add_generative_functions_to_scope(generative_functions, scope)
    add_constants_to_scope(model.constants, scope)
    _init_builtins_scope(scope)
