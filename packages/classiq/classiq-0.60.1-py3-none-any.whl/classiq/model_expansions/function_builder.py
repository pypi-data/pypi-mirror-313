from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Generic, Optional, TypeVar

from classiq.interface.exceptions import ClassiqInternalExpansionError
from classiq.interface.generator.compiler_keywords import (
    EXPANDED_KEYWORD,
    LAMBDA_KEYWORD,
)
from classiq.interface.generator.functions.builtins.internal_operators import (
    WITHIN_APPLY_NAME,
)
from classiq.interface.model.model import MAIN_FUNCTION_NAME
from classiq.interface.model.native_function_definition import (
    NativeFunctionDefinition,
)
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_declaration import (
    PositionalArg,
)
from classiq.interface.model.quantum_statement import QuantumStatement
from classiq.interface.source_reference import SourceReference

from classiq.model_expansions.capturing.captured_vars import (
    CapturedVars,
    validate_captured_directions,
)
from classiq.model_expansions.closure import Closure, FunctionClosure
from classiq.model_expansions.scope import Scope

ClosureType = TypeVar("ClosureType", bound=Closure)


@dataclass
class Block:
    statements: list[QuantumStatement] = field(default_factory=list)
    captured_vars: CapturedVars = field(default_factory=CapturedVars)


@dataclass
class OperationContext(Generic[ClosureType]):
    closure: ClosureType
    blocks: dict[str, Block] = field(default_factory=dict)

    @property
    def name(self) -> str:
        return self.closure.name

    @property
    def positional_arg_declarations(self) -> Sequence[PositionalArg]:
        return self.closure.positional_arg_declarations

    def statements(self, block_name: str) -> list[QuantumStatement]:
        return self.blocks[block_name].statements


@dataclass
class FunctionContext(OperationContext[FunctionClosure]):
    @classmethod
    def create(cls, original_function: FunctionClosure) -> "FunctionContext":
        return cls(original_function, {"body": Block()})

    @property
    def body(self) -> list[QuantumStatement]:
        return self.statements("body")

    @property
    def is_lambda(self) -> bool:
        return self.closure.is_lambda


class OperationBuilder:
    def __init__(self, functions_scope: Scope) -> None:
        self._operations: list[OperationContext] = []
        self._blocks: list[str] = []
        self._functions_scope = functions_scope
        self._current_source_ref: Optional[SourceReference] = None

    @property
    def current_operation(self) -> Closure:
        return self._operations[-1].closure

    @property
    def current_function(self) -> FunctionClosure:
        return self._get_last_function(self._operations)

    @property
    def parent_function(self) -> FunctionClosure:
        return self._get_last_function(self._operations[:-1])

    @staticmethod
    def _get_last_function(operations: list[OperationContext]) -> FunctionClosure:
        for operation in reversed(operations):
            if isinstance(operation.closure, FunctionClosure):
                return operation.closure
        raise ClassiqInternalExpansionError("No function found")

    @property
    def current_block(self) -> Block:
        return self._operations[-1].blocks[self._blocks[-1]]

    @property
    def _current_statements(self) -> list[QuantumStatement]:
        return self.current_block.statements

    def emit_statement(self, statement: QuantumStatement) -> None:
        if self._current_source_ref is not None:
            statement.source_ref = self._current_source_ref
        self._current_statements.append(statement)

    @property
    def current_statement(self) -> QuantumStatement:
        return self._current_statements[-1]

    @contextmanager
    def block_context(self, block_name: str) -> Iterator[None]:
        self._blocks.append(block_name)
        self._operations[-1].blocks[block_name] = Block()
        yield
        captured_vars = self.current_block.captured_vars
        if (
            not isinstance(self.current_operation, FunctionClosure)
            and self.current_operation.name != WITHIN_APPLY_NAME
        ):
            validate_captured_directions(captured_vars)
        self.current_operation.captured_vars.update(
            captured_vars.filter(self.current_function)
        )
        self._blocks.pop()

    @contextmanager
    def operation_context(
        self, original_operation: Closure
    ) -> Iterator[OperationContext]:
        context: OperationContext
        if isinstance(original_operation, FunctionClosure):
            context = FunctionContext.create(original_operation)
        else:
            context = OperationContext(closure=original_operation)
        self._operations.append(context)
        yield context
        self._finalize_within_apply()
        self._propagate_captured_vars()
        self._operations.pop()

    def _finalize_within_apply(self) -> None:
        if self.current_operation.name != WITHIN_APPLY_NAME:
            return
        within_captured_vars = self._operations[-1].blocks["within"].captured_vars
        self.current_operation.captured_vars.update(
            within_captured_vars.filter(self.current_function).negate()
        )

    def _propagate_captured_vars(self) -> None:
        captured_vars = self.current_operation.captured_vars
        if isinstance(self.current_operation, FunctionClosure):
            captured_vars = captured_vars.set_propagated()
        validate_captured_directions(captured_vars)
        if len(self._operations) < 2:
            return
        parent_block = self._operations[-2].blocks[self._blocks[-1]]
        parent_block.captured_vars.update(captured_vars.filter(self.parent_function))

    @contextmanager
    def source_ref_context(
        self, source_ref: Optional[SourceReference]
    ) -> Iterator[None]:
        previous_source_ref = self._current_source_ref
        self._current_source_ref = source_ref
        yield
        self._current_source_ref = previous_source_ref

    def create_definition(
        self, function_context: FunctionContext
    ) -> NativeFunctionDefinition:
        name = function_context.name
        if name != MAIN_FUNCTION_NAME:
            idx = 0
            new_name = name
            while idx == 0 or new_name in self._functions_scope:
                new_name = f"{name}_{LAMBDA_KEYWORD + '_0_0_' if function_context.is_lambda else ''}{EXPANDED_KEYWORD}_{idx}"
                idx += 1
            name = new_name

        new_parameters: list[PortDeclaration] = [
            param
            for param in function_context.positional_arg_declarations
            if isinstance(param, PortDeclaration)
        ]

        return NativeFunctionDefinition(
            name=name,
            body=function_context.body,
            positional_arg_declarations=new_parameters,
        )
