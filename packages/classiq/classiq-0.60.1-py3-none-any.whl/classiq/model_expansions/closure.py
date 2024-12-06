import dataclasses
import json
import uuid
from collections.abc import Collection, Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field
from functools import singledispatch
from symtable import Symbol
from typing import Any, Optional

from typing_extensions import Self

from classiq.interface.exceptions import ClassiqInternalExpansionError
from classiq.interface.generator.functions.builtins.internal_operators import (
    All_BUILTINS_OPERATORS,
)
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_declaration import (
    NamedParamsQuantumFunctionDeclaration,
    PositionalArg,
    QuantumOperandDeclaration,
)
from classiq.interface.model.quantum_statement import QuantumStatement

from classiq import ClassicalParameterDeclaration
from classiq.model_expansions.capturing.captured_vars import CapturedVars
from classiq.model_expansions.expression_renamer import ExpressionRenamer
from classiq.model_expansions.scope import (
    Evaluated,
    QuantumSymbol,
    Scope,
    evaluated_to_str as evaluated_classical_param_to_str,
)
from classiq.qmod.builtins.functions import permute
from classiq.qmod.quantum_function import GenerativeQFunc


@dataclass(frozen=True)
class Closure:
    name: str
    blocks: dict[str, Sequence[QuantumStatement]]
    scope: Scope
    positional_arg_declarations: Sequence[PositionalArg] = tuple()
    captured_vars: CapturedVars = field(default_factory=CapturedVars)

    @property
    def port_declarations(self) -> dict[str, PortDeclaration]:
        return {
            param.name: param
            for param in self.positional_arg_declarations
            if isinstance(param, PortDeclaration)
        }

    @contextmanager
    def freeze(self) -> Iterator[None]:
        with self.scope.freeze(), self.captured_vars.freeze():
            yield


@dataclass(frozen=True)
class GenerativeClosure(Closure):
    generative_blocks: dict[str, GenerativeQFunc] = None  # type:ignore[assignment]


@dataclass(frozen=True)
class FunctionClosure(Closure):
    is_lambda: bool = False
    is_atomic: bool = False
    signature_scope: Scope = field(default_factory=Scope)
    _depth: Optional[int] = None

    @property
    def depth(self) -> int:
        if self._depth is None:
            raise ClassiqInternalExpansionError
        return self._depth

    # creates a unique id for the function closure based on the arguments values.
    # The closure is changing across the interpreter flow so it's closure_id may change
    @property
    def closure_id(self) -> str:
        # builtins operators have side effects, so  generate a unique id for than
        # may create a bugs. Therefore, with each call to closure_id a new id is
        # created
        if self.is_lambda or self.name in All_BUILTINS_OPERATORS:
            signature = str(uuid.uuid4())
        else:
            signature = _generate_closure_id(
                self.positional_arg_declarations, self.scope.data.values()
            )
        return f"{self.name}__{signature}"

    @property
    def body(self) -> Sequence[QuantumStatement]:
        if self.name == permute.func_decl.name:
            # permute is an old Qmod "generative" function that doesn't have a body
            return []
        return self.blocks["body"]

    @classmethod
    def create(
        cls,
        name: str,
        scope: Scope,
        body: Optional[Sequence[QuantumStatement]] = None,
        positional_arg_declarations: Sequence[PositionalArg] = tuple(),
        expr_renamer: Optional[ExpressionRenamer] = None,
        is_lambda: bool = False,
        is_atomic: bool = False,
        **kwargs: Any,
    ) -> Self:
        if expr_renamer:
            positional_arg_declarations = (
                expr_renamer.rename_positional_arg_declarations(
                    positional_arg_declarations
                )
            )
            if body is not None:
                body = expr_renamer.visit(body)

        blocks = {"body": body} if body is not None else {}
        return cls(
            name,
            blocks,
            scope,
            positional_arg_declarations,
            CapturedVars(),
            is_lambda,
            is_atomic,
            **kwargs,
        )

    def with_new_declaration(
        self, declaration: NamedParamsQuantumFunctionDeclaration
    ) -> Self:
        fields: dict = self.__dict__ | {
            "name": declaration.name,
            "positional_arg_declarations": declaration.positional_arg_declarations,
        }
        return type(self)(**fields)

    def set_depth(self, depth: int) -> Self:
        return dataclasses.replace(self, _depth=depth)

    def copy_scope(self) -> Self:  # Remove when scoping is normal (CAD-24980)
        return dataclasses.replace(
            self, scope=Scope(self.scope.data, parent=self.scope.parent)
        )


@dataclass(frozen=True)
class GenerativeFunctionClosure(GenerativeClosure, FunctionClosure):
    pass


def _generate_closure_id(
    args_declaration: Sequence[PositionalArg], evaluated_args: Collection[Evaluated]
) -> str:
    args_signature: dict = {}
    for arg_declara, eval_arg in zip(args_declaration, evaluated_args):
        args_signature |= _generate_arg_id(arg_declara, eval_arg)
    return json.dumps(args_signature)


def _generate_arg_id(
    arg_declaration: PositionalArg, evaluated_arg: Evaluated
) -> dict[str, str]:
    arg_value = evaluated_arg.value
    arg_name = arg_declaration.name
    if isinstance(arg_declaration, ClassicalParameterDeclaration):
        return {arg_name: evaluated_classical_param_to_str(arg_value)}
    if isinstance(arg_declaration, PortDeclaration):
        return {arg_name: _evaluated_port_to_str(arg_value)}
    if isinstance(arg_declaration, QuantumOperandDeclaration):
        return {arg_name: _evaluated_operand_to_str(arg_value)}


def _evaluated_arg_to_str(arg: Any) -> str:
    if isinstance(arg, str):
        return arg
    return str(uuid.uuid4())


@singledispatch
def _evaluated_port_to_str(arg: Any) -> str:
    return _evaluated_arg_to_str(arg)


@_evaluated_port_to_str.register
def _evaluated_quantum_symbol_to_str(port: QuantumSymbol) -> str:
    return port.quantum_type.model_dump_json(exclude_none=True, exclude={"name"})


@_evaluated_port_to_str.register
def _evaluated_symbol_to_str(port: Symbol) -> str:
    return repr(port)


@singledispatch
def _evaluated_operand_to_str(arg: Any) -> str:
    return _evaluated_arg_to_str(arg)


@_evaluated_operand_to_str.register
def _evaluated_one_operand_to_str(operand: FunctionClosure) -> str:
    return operand.closure_id


@_evaluated_operand_to_str.register
def _evaluated_list_operands_to_str(operands: list) -> str:
    return json.dumps([_evaluated_operand_to_str(ope) for ope in operands])
