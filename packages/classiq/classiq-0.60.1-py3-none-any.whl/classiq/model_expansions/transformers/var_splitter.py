import ast
from dataclasses import dataclass
from itertools import chain
from typing import TYPE_CHECKING, Callable, TypeVar, cast

from classiq.interface.exceptions import (
    ClassiqExpansionError,
    ClassiqInternalExpansionError,
)
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.visitor import NodeType, Transformer
from classiq.interface.model.bind_operation import BindOperation
from classiq.interface.model.handle_binding import (
    HandleBinding,
    NestedHandleBinding,
    SlicedHandleBinding,
)
from classiq.interface.model.quantum_expressions.quantum_expression import (
    QuantumExpressionOperation,
)
from classiq.interface.model.quantum_type import (
    QuantumBitvector,
    QuantumScalar,
    QuantumType,
)
from classiq.interface.model.variable_declaration_statement import (
    VariableDeclarationStatement,
)

from classiq.model_expansions.scope import QuantumSymbol, Scope
from classiq.model_expansions.visitors.variable_references import VarRefCollector

AST_NODE = TypeVar("AST_NODE", bound=NodeType)


@dataclass(frozen=True)
class SymbolPart:
    source_handle: HandleBinding
    target_var_name: str
    target_var_type: QuantumType

    @property
    def target_var_handle(self) -> HandleBinding:
        return HandleBinding(name=self.target_var_name)


SymbolParts = dict[QuantumSymbol, list[SymbolPart]]
PartNamer = Callable[[str], str]


class VarSplitter:
    def __init__(self, scope: Scope):
        self._scope = scope

    def split_symbols(self, expression: Expression, namer: PartNamer) -> SymbolParts:
        vrc = VarRefCollector(ignore_duplicated_handles=True)
        vrc.visit(ast.parse(expression.expr))
        symbol_names_to_split = dict.fromkeys(
            handle.name
            for handle in vrc.var_handles
            if isinstance(self._scope[handle.name].value, QuantumSymbol)
            and isinstance(handle, NestedHandleBinding)
        )

        symbol_handles = {
            symbol: list(
                dict.fromkeys(
                    handle.collapse()
                    for handle in vrc.var_handles
                    if handle.name == symbol.handle.name
                )
            )
            for symbol_name in symbol_names_to_split
            if isinstance(
                symbol := self._scope[symbol_name].value,
                QuantumSymbol,
            )
        }

        return {
            symbol: [
                SymbolPart(
                    source_handle=part.handle,
                    target_var_name=namer(part.handle.identifier),
                    target_var_type=part.quantum_type,
                )
                for part in self._get_symbol_parts(symbol, handles)
            ]
            for symbol, handles in symbol_handles.items()
        }

    def _get_symbol_parts(
        self, symbol: QuantumSymbol, target_parts: list[HandleBinding]
    ) -> list[QuantumSymbol]:
        for i in range(len(target_parts)):
            for j in range(i + 1, len(target_parts)):
                if target_parts[i].overlaps(target_parts[j]):
                    raise ClassiqInternalExpansionError(
                        f"Handles {str(target_parts[i])!r} and "
                        f"{str(target_parts[j])!r} overlapping in expression"
                    )
        return self._get_symbol_parts_unsafe(symbol, target_parts)

    def _get_symbol_parts_unsafe(
        self, symbol: QuantumSymbol, target_parts: list[HandleBinding]
    ) -> list[QuantumSymbol]:
        if all(
            symbol.handle == target_part or symbol.handle not in target_part.prefixes()
            for target_part in target_parts
        ) or isinstance(symbol.quantum_type, QuantumScalar):
            return [symbol]

        if isinstance(symbol.quantum_type, QuantumBitvector):
            return self._get_array_parts(symbol, target_parts)

        return self._get_struct_parts(symbol, target_parts)

    def _get_array_parts(
        self, symbol: QuantumSymbol, target_parts: list[HandleBinding]
    ) -> list[QuantumSymbol]:
        if TYPE_CHECKING:
            assert isinstance(symbol.quantum_type, QuantumBitvector)

        if not symbol.quantum_type.has_length:
            raise ClassiqExpansionError(
                f"Could not determine the length of quantum array " f"{symbol.handle}."
            )
        target_slices = {
            target_part.start.to_int_value(): target_part.end.to_int_value()
            for target_part in target_parts
            if isinstance(target_part, SlicedHandleBinding)
            and symbol.handle == target_part.base_handle
        }

        symbol_parts: list[QuantumSymbol] = []
        idx = 0
        while idx < symbol.quantum_type.length_value:
            if idx in target_slices:
                stop = target_slices[idx]
                if stop <= idx:
                    raise ClassiqInternalExpansionError(
                        f"Illegal sliced handle {str(symbol[idx: stop].handle)!r}"
                    )
                symbol_parts.append(symbol[idx:stop])
                idx = stop
            else:
                symbol_parts.extend(
                    self._get_symbol_parts_unsafe(symbol[idx], target_parts)
                )
                idx += 1

        return symbol_parts

    def _get_struct_parts(
        self, symbol: QuantumSymbol, target_parts: list[HandleBinding]
    ) -> list[QuantumSymbol]:
        return list(
            chain.from_iterable(
                self._get_symbol_parts_unsafe(field_symbol, target_parts)
                for field_symbol in symbol.fields.values()
            )
        )

    @staticmethod
    def get_bind_ops(symbol_parts: SymbolParts) -> list[BindOperation]:
        return [
            BindOperation(
                in_handles=[symbol.handle],
                out_handles=[part.target_var_handle for part in parts],
            )
            for symbol, parts in symbol_parts.items()
        ]

    @staticmethod
    def get_var_decls(symbol_parts: SymbolParts) -> list[VariableDeclarationStatement]:
        return [
            VariableDeclarationStatement(
                name=part.target_var_name,
                quantum_type=part.target_var_type,
            )
            for part in chain.from_iterable(symbol_parts.values())
        ]

    def rewrite(self, subject: AST_NODE, symbol_mapping: SymbolParts) -> AST_NODE:
        if len(symbol_mapping) == 0:
            return subject
        handle_replacements = {
            part.source_handle: part.target_var_handle
            for parts in symbol_mapping.values()
            for part in parts
        }

        class ReplaceSplitVars(Transformer):
            @staticmethod
            def visit_HandleBinding(handle: HandleBinding) -> HandleBinding:
                handle = handle.collapse()
                for handle_to_replace, replacement in handle_replacements.items():
                    handle = handle.replace_prefix(handle_to_replace, replacement)
                return handle

            @staticmethod
            def visit_Expression(expr: Expression) -> Expression:
                return self._rewrite_expression(symbol_mapping, expr)

            def visit_QuantumExpressionOperation(
                self, op: QuantumExpressionOperation
            ) -> QuantumExpressionOperation:
                op = cast(QuantumExpressionOperation, self.generic_visit(op))
                previous_var_handles = list(op._var_handles)
                op._var_handles = self.visit(op._var_handles)
                op._var_types = {
                    new_handle.name: op._var_types.get(
                        new_handle.name, op._var_types[previous_handle.name]
                    )
                    for previous_handle, new_handle in zip(
                        previous_var_handles, op._var_handles
                    )
                }
                return op

        return ReplaceSplitVars().visit(subject)

    def _rewrite_expression(
        self,
        symbol_mapping: SymbolParts,
        expression: Expression,
    ) -> Expression:
        vrc = VarRefCollector(ignore_duplicated_handles=True)
        vrc.visit(ast.parse(expression.expr))

        handle_names = {
            part.source_handle: part.target_var_name
            for parts in symbol_mapping.values()
            for part in parts
        }
        new_expr_str = expression.expr
        for handle in vrc.var_handles:
            collapsed_handle = handle.collapse()
            if collapsed_handle in handle_names:
                new_expr_str = new_expr_str.replace(
                    str(handle), handle_names[collapsed_handle]
                )
                if handle.qmod_expr != str(handle):
                    new_expr_str = new_expr_str.replace(
                        handle.qmod_expr, handle_names[collapsed_handle]
                    )

        new_expr = Expression(expr=new_expr_str)
        new_expr._evaluated_expr = expression._evaluated_expr
        return new_expr
