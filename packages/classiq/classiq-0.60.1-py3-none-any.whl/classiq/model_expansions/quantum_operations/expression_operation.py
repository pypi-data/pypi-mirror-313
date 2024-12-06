import ast
from typing import Generic, TypeVar, Union

from classiq.interface.exceptions import ClassiqInternalExpansionError
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.visitor import NodeType
from classiq.interface.model.control import Control
from classiq.interface.model.quantum_expressions.quantum_expression import (
    QuantumAssignmentOperation,
    QuantumExpressionOperation,
)
from classiq.interface.model.quantum_type import (
    QuantumNumeric,
)
from classiq.interface.model.within_apply_operation import WithinApply

from classiq.model_expansions.quantum_operations.call_emitter import CallEmitter
from classiq.model_expansions.scope import QuantumSymbol
from classiq.model_expansions.transformers.var_splitter import SymbolParts
from classiq.model_expansions.visitors.variable_references import VarRefCollector

ExpressionOperationT = TypeVar("ExpressionOperationT", bound=QuantumExpressionOperation)
AST_NODE = TypeVar("AST_NODE", bound=NodeType)


class ExpressionOperationEmitter(
    Generic[ExpressionOperationT], CallEmitter[ExpressionOperationT]
):
    def _emit_with_split(
        self,
        op: ExpressionOperationT,
        expression: Expression,
        symbol_parts: SymbolParts,
    ) -> None:
        for var_decl in self.get_var_decls(symbol_parts):
            self._interpreter.emit_statement(var_decl)
        bind_ops = self.get_bind_ops(symbol_parts)

        new_expression = self.rewrite(expression, symbol_parts)
        if len(self.split_symbols(new_expression, lambda name: name)) > 0:
            raise ClassiqInternalExpansionError(
                f"Did not replace all handles in expression: {expression.expr!r} -> "
                f"{new_expression.expr!r}"
            )
        new_op = op.model_copy(update=dict(expression=new_expression))
        new_op = self._get_updated_op_split_symbols(new_op, symbol_parts)

        self._interpreter.emit_statement(
            WithinApply(
                compute=bind_ops,
                action=[new_op],
                source_ref=op.source_ref,
            )
        )

    def _get_updated_op_split_symbols(
        self,
        op: ExpressionOperationT,
        symbol_mapping: SymbolParts,
    ) -> ExpressionOperationT:
        return op

    def _evaluate_op_expression(self, op: ExpressionOperationT) -> Expression:
        return self._evaluate_expression(op.expression)

    def _evaluate_types_in_expression(
        self, op: ExpressionOperationT, expression: Expression
    ) -> ExpressionOperationT:
        op_with_evaluated_types = op.model_copy(update={"expression": expression})
        vrc = VarRefCollector()
        vrc.visit(ast.parse(op_with_evaluated_types.expression.expr))
        handles = vrc.var_handles
        op_with_evaluated_types.set_var_handles(handles)
        op_with_evaluated_types.initialize_var_types(
            {
                handle.name: self._interpreter.evaluate(handle)
                .as_type(QuantumSymbol)
                .quantum_type
                for handle in handles
            },
            self._machine_precision,
        )
        return op_with_evaluated_types

    @staticmethod
    def _all_vars_boolean(op: QuantumExpressionOperation) -> bool:
        if not all(
            var_type.has_size_in_bits and var_type.size_in_bits == 1
            for var_type in op.var_types.values()
        ):
            return False
        return not any(
            isinstance(var_type, QuantumNumeric)
            and (var_type.sign_value or var_type.fraction_digits_value > 0)
            for var_type in op.var_types.values()
        )

    @staticmethod
    def _is_res_boolean(op: Union[QuantumAssignmentOperation, Control]) -> bool:
        if not (op.result_type.has_size_in_bits and op.result_type.size_in_bits == 1):
            return False
        return not (
            isinstance(op.result_type, QuantumNumeric)
            and (op.result_type.sign_value or op.result_type.fraction_digits_value > 0)
        )
