from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from classiq.interface.exceptions import ClassiqInternalExpansionError
from classiq.interface.generator.expressions.qmod_struct_instance import (
    QmodStructInstance,
)
from classiq.interface.generator.functions.type_name import Struct
from classiq.interface.generator.visitor import Visitor
from classiq.interface.helpers.pydantic_model_helpers import nameables_to_dict
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_call import ArgValue, QuantumFunctionCall
from classiq.interface.model.quantum_function_declaration import (
    PositionalArg,
    QuantumFunctionDeclaration,
    QuantumOperandDeclaration,
)
from classiq.interface.model.quantum_lambda_function import (
    QuantumCallable,
    QuantumLambdaFunction,
)
from classiq.interface.model.quantum_statement import QuantumStatement

from classiq.model_expansions.closure import (
    FunctionClosure,
    GenerativeClosure,
    GenerativeFunctionClosure,
)
from classiq.model_expansions.scope import Evaluated, QuantumSymbol
from classiq.qmod.generative import generative_mode_context, set_frontend_interpreter
from classiq.qmod.model_state_container import QMODULE
from classiq.qmod.qmod_parameter import CParamStruct
from classiq.qmod.qmod_variable import QNum, _create_qvar_for_qtype
from classiq.qmod.quantum_callable import QCallable
from classiq.qmod.quantum_expandable import (
    QExpandable,
    QLambdaFunction,
    QTerminalCallable,
)
from classiq.qmod.quantum_function import QFunc
from classiq.qmod.semantics.static_semantics_visitor import resolve_function_calls
from classiq.qmod.symbolic_expr import SymbolicExpr

if TYPE_CHECKING:
    from classiq.model_expansions.interpreter import Interpreter


class LenList(list):
    @property
    def len(self) -> int:
        return len(self)

    def __getitem__(self, item: Any) -> Any:
        if isinstance(item, QNum):
            return SymbolicExpr(f"{self}[{item}]", True)
        return super().__getitem__(item)

    @classmethod
    def wrap(cls, obj: Any) -> Any:
        if not isinstance(obj, list):
            return obj
        return LenList([cls.wrap(item) for item in obj])


def translate_ast_arg_to_python_qmod(param: PositionalArg, evaluated: Evaluated) -> Any:
    if isinstance(param, PortDeclaration):
        quantum_symbol = evaluated.as_type(QuantumSymbol)
        return _create_qvar_for_qtype(
            quantum_symbol.quantum_type, quantum_symbol.handle
        )
    if isinstance(param, QuantumOperandDeclaration):
        if param.is_list:
            return QTerminalCallable(
                QuantumOperandDeclaration(
                    name=param.name,
                    positional_arg_declarations=param.positional_arg_declarations,
                    is_list=True,
                ),
            )
        else:
            func = evaluated.as_type(FunctionClosure)
            return QTerminalCallable(
                QuantumFunctionDeclaration(
                    name=param.name if func.is_lambda else func.name,
                    positional_arg_declarations=func.positional_arg_declarations,
                ),
            )
    classical_value = evaluated.value
    if isinstance(classical_value, QmodStructInstance):
        return CParamStruct(
            expr=param.name,
            struct_type=Struct(name=classical_value.struct_declaration.name),
            qmodule=QMODULE,
        )
    return LenList.wrap(classical_value)


class _InterpreterExpandable(QFunc):
    def __init__(self, interpreter: "Interpreter"):
        super().__init__(lambda: None)
        self._interpreter = interpreter

    def append_statement_to_body(self, stmt: QuantumStatement) -> None:
        current_operation = self._interpreter._builder._operations[-1]
        dummy_function = NativeFunctionDefinition(
            name=current_operation.name,
            positional_arg_declarations=current_operation.positional_arg_declarations,
            body=self._interpreter._builder._current_statements + [stmt],
        )
        resolve_function_calls(dummy_function, self._get_function_declarations())
        stmt = dummy_function.body[-1]
        with generative_mode_context(False):
            self._interpreter.emit_statement(stmt)

    def _get_function_declarations(self) -> Mapping[str, QuantumFunctionDeclaration]:
        return {
            name: QuantumFunctionDeclaration(
                name=name,
                positional_arg_declarations=evaluated.value.positional_arg_declarations,
            )
            for name, evaluated in self._interpreter._current_scope.items()
            if isinstance(evaluated, Evaluated)
            and isinstance(evaluated.value, FunctionClosure)
        } | nameables_to_dict(self._interpreter._get_function_declarations())


def emit_generative_statements(
    interpreter: "Interpreter",
    operation: GenerativeClosure,
    args: list[Evaluated],
) -> None:
    python_qmod_args = [
        translate_ast_arg_to_python_qmod(param, arg)
        for param, arg in zip(operation.positional_arg_declarations, args)
    ]
    interpreter_expandable = _InterpreterExpandable(interpreter)
    QExpandable.STACK.append(interpreter_expandable)
    QCallable.CURRENT_EXPANDABLE = interpreter_expandable
    set_frontend_interpreter(interpreter)
    for block_name, generative_function in operation.generative_blocks.items():
        with interpreter._builder.block_context(block_name), generative_mode_context(
            True
        ):
            generative_function._py_callable(*python_qmod_args)


def emit_operands_as_declarative(
    interpreter: "Interpreter", param: PositionalArg, arg: Evaluated
) -> ArgValue:
    if not isinstance(param, QuantumOperandDeclaration):
        return arg.emit()
    value = arg.value
    if isinstance(value, list):
        return [
            _expand_operand_as_declarative(interpreter, param, item) for item in value
        ]
    if isinstance(value, GenerativeFunctionClosure):
        return _expand_operand_as_declarative(interpreter, param, value)
    if isinstance(value, FunctionClosure):
        if value.is_lambda:
            raise ClassiqInternalExpansionError
        _register_declarative_function(interpreter, value.name)
        return value.name
    raise ClassiqInternalExpansionError


def _expand_operand_as_declarative(
    interpreter: "Interpreter",
    param: QuantumOperandDeclaration,
    arg: GenerativeFunctionClosure,
) -> QuantumCallable:
    if not arg.is_lambda:
        _register_declarative_function(interpreter, arg.name)
        return arg.name
    val = QLambdaFunction(param, arg.generative_blocks["body"]._py_callable)
    with generative_mode_context(False):
        val.expand()
        _DecFuncVisitor(interpreter).visit(val.body)
    qlambda = QuantumLambdaFunction(
        pos_rename_params=val.infer_rename_params(),
        body=val.body,
    )
    qlambda.set_op_decl(param)
    return qlambda


def _register_declarative_function(interpreter: "Interpreter", func_name: str) -> None:
    if func_name in nameables_to_dict(list(interpreter._expanded_functions.values())):
        return

    for user_gen_func in interpreter._generative_functions:
        if user_gen_func.func_decl.name == func_name:
            break
    else:
        return

    with generative_mode_context(False):
        dec_func = QFunc(user_gen_func._py_callable)
        dec_func.expand()
        dec_func_def = QMODULE.native_defs[func_name]
        interpreter._expanded_functions[func_name] = dec_func_def
        _DecFuncVisitor(interpreter).visit(dec_func_def)


class _DecFuncVisitor(Visitor):
    def __init__(self, interpreter: "Interpreter"):
        self._interpreter = interpreter

    def visit_QuantumFunctionCall(self, call: QuantumFunctionCall) -> None:
        _register_declarative_function(self._interpreter, call.func_name)
        for arg in call.positional_args:
            if isinstance(arg, str):
                arg = [arg]
            if isinstance(arg, list):
                for possible_func_name in arg:
                    if isinstance(possible_func_name, str):
                        _register_declarative_function(
                            self._interpreter, possible_func_name
                        )
