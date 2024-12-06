from abc import abstractmethod
from typing import (
    TYPE_CHECKING,
    Generic,
    Optional,
    TypeVar,
    Union,
)

import sympy

from classiq.interface.exceptions import ClassiqInternalExpansionError
from classiq.interface.generator.expressions.evaluated_expression import (
    EvaluatedExpression,
)
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.model.handle_binding import HandleBinding
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.quantum_function_declaration import (
    NamedParamsQuantumFunctionDeclaration,
)
from classiq.interface.model.quantum_statement import QuantumOperation, QuantumStatement

from classiq.model_expansions.closure import Closure, FunctionClosure, GenerativeClosure
from classiq.model_expansions.function_builder import (
    FunctionContext,
    OperationBuilder,
    OperationContext,
)
from classiq.model_expansions.scope import QuantumSymbol, Scope
from classiq.model_expansions.sympy_conversion.sympy_to_python import (
    translate_sympy_quantum_expression,
)
from classiq.model_expansions.utils.counted_name_allocator import CountedNameAllocator
from classiq.qmod.quantum_function import GenerativeQFunc

if TYPE_CHECKING:
    from classiq.model_expansions.interpreter import Interpreter

QuantumStatementT = TypeVar("QuantumStatementT", bound=QuantumStatement)


class Emitter(Generic[QuantumStatementT]):
    def __init__(self, interpreter: "Interpreter") -> None:
        self._interpreter = interpreter

        self._scope_guard = self._interpreter._scope_guard
        self._machine_precision = self._interpreter._model.preferences.machine_precision
        self._expanded_functions_compilation_metadata = (
            self._interpreter._expanded_functions_compilation_metadata
        )
        self._functions_compilation_metadata = (
            self._interpreter._model.functions_compilation_metadata
        )
        self._generative_contexts: dict[str, OperationContext] = {}

    @abstractmethod
    def emit(self, statement: QuantumStatementT, /) -> None:
        pass

    def _expand_operation(self, closure: Closure) -> OperationContext:
        if closure.name in self._generative_contexts:
            if isinstance(closure, FunctionClosure):
                return FunctionContext(
                    closure=closure,
                    blocks=self._generative_contexts[closure.name].blocks,
                )
            return self._generative_contexts[closure.name]
        return self._interpreter._expand_operation(closure)

    @property
    def _builder(self) -> OperationBuilder:
        return self._interpreter._builder

    @property
    def _current_scope(self) -> Scope:
        return self._interpreter._current_scope

    @property
    def _top_level_scope(self) -> Scope:
        return self._interpreter._top_level_scope

    @property
    def _expanded_functions(self) -> dict[str, NativeFunctionDefinition]:
        return self._interpreter._expanded_functions

    @property
    def _counted_name_allocator(self) -> CountedNameAllocator:
        return self._interpreter._counted_name_allocator

    def _register_generative_context(
        self,
        op: QuantumOperation,
        context_name: str,
        block_names: Union[None, str, list[str]] = None,
        func_decl: Optional[NamedParamsQuantumFunctionDeclaration] = None,
    ) -> OperationContext:
        if isinstance(block_names, str):
            block_names = [block_names]
        block_names = block_names or ["body"]
        func_decl = func_decl or NamedParamsQuantumFunctionDeclaration(
            name=context_name
        )
        gen_closure = GenerativeClosure(
            name=func_decl.name,
            scope=Scope(parent=self._interpreter._current_scope),
            blocks={},
            generative_blocks={
                block_name: GenerativeQFunc(
                    op.get_generative_block(block_name), func_decl
                )
                for block_name in block_names
            },
        )
        context = self._interpreter._expand_operation(gen_closure)
        self._generative_contexts[context_name] = context
        op.clear_generative_blocks()
        return context

    def _evaluate_expression(self, expression: Expression) -> Expression:
        evaluated_expression = self._interpreter.evaluate(expression)
        if isinstance(evaluated_expression.value, sympy.Basic):
            new_expression = Expression(
                expr=translate_sympy_quantum_expression(evaluated_expression.value)
            )
        else:
            new_expression = Expression(expr=str(evaluated_expression.value))
        new_expression._evaluated_expr = EvaluatedExpression(
            value=evaluated_expression.value
        )
        return new_expression

    def emit_statement(self, statement: QuantumStatement) -> None:
        if isinstance(statement, QuantumOperation):
            self._update_captured_vars(statement)
        self._builder.emit_statement(statement)

    def _update_captured_vars(self, op: QuantumOperation) -> None:
        handles = (
            [(handle, PortDeclarationDirection.Input) for handle in op.inputs]
            + [(handle, PortDeclarationDirection.Output) for handle in op.outputs]
            + [(handle, PortDeclarationDirection.Inout) for handle in op.inouts]
        )
        for handle, direction in handles:
            self._capture_handle(handle, direction)

    def _capture_handle(
        self, handle: HandleBinding, direction: PortDeclarationDirection
    ) -> None:
        if handle.name not in self._current_scope:
            return
        defining_function = self._current_scope[handle.name].defining_function
        if defining_function is None:
            raise ClassiqInternalExpansionError
        symbol: QuantumSymbol = self._interpreter.evaluate(handle).value
        self._builder.current_block.captured_vars.capture_handle(
            handle=symbol.handle,
            quantum_type=symbol.quantum_type,
            defining_function=defining_function,
            direction=direction,
        )
