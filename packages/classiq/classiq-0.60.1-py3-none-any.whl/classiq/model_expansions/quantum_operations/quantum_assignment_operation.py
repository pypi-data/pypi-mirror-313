import ast
import re

from classiq.interface.exceptions import (
    ClassiqExpansionError,
    ClassiqInternalExpansionError,
)
from classiq.interface.generator.compiler_keywords import INPLACE_ARITH_AUX_VAR_PREFIX
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.model.handle_binding import HandleBinding
from classiq.interface.model.inplace_binary_operation import (
    BinaryOperation,
    InplaceBinaryOperation,
)
from classiq.interface.model.quantum_expressions.arithmetic_operation import (
    ArithmeticOperation,
    ArithmeticOperationKind,
)
from classiq.interface.model.quantum_expressions.quantum_expression import (
    QuantumAssignmentOperation,
)
from classiq.interface.model.quantum_function_call import QuantumFunctionCall
from classiq.interface.model.quantum_type import QuantumNumeric
from classiq.interface.model.variable_declaration_statement import (
    VariableDeclarationStatement,
)
from classiq.interface.model.within_apply_operation import WithinApply

from classiq.model_expansions.capturing.mangling_utils import demangle_handle
from classiq.model_expansions.evaluators.quantum_type_utils import copy_type_information
from classiq.model_expansions.quantum_operations.expression_operation import (
    ExpressionOperationEmitter,
)
from classiq.model_expansions.scope import QuantumSymbol
from classiq.model_expansions.transformers.var_splitter import SymbolParts
from classiq.model_expansions.visitors.boolean_expression_transformers import (
    BooleanExpressionFuncLibAdapter,
    BooleanExpressionOptimizer,
)
from classiq.qmod import builtins
from classiq.qmod.builtins.functions import X, allocate

HANDLE_ERROR_MESSAGE = (
    "Quantum variable '{handle_str}' cannot appear on both sides of the assignment"
)


def _is_constant(expr: str) -> bool:
    try:
        float(expr)
        return True
    except ValueError:
        return False


def _is_zero(expr: str) -> bool:
    return _is_constant(expr) and float(expr) == 0


def _is_variable(expr: str) -> bool:
    return re.fullmatch("[a-zA-Z_][a-zA-Z0-9_]*", expr) is not None


class QuantumAssignmentOperationEmitter(
    ExpressionOperationEmitter[QuantumAssignmentOperation]
):
    def emit(self, op: QuantumAssignmentOperation, /) -> None:
        new_expression = self._evaluate_op_expression(op)
        if self._skip_assignment(op, new_expression.expr):
            return
        arrays_with_subscript = self.split_symbols(
            new_expression, self._counted_name_allocator.allocate
        )
        if len(arrays_with_subscript) > 0:
            self._emit_with_split(op, new_expression, arrays_with_subscript)
            return

        self._emit_op(new_expression, op)

    def _emit_op(self, expression: Expression, op: QuantumAssignmentOperation) -> None:
        op = self._evaluate_types_in_expression(op, expression)
        if isinstance(op, ArithmeticOperation):
            self._emit_arithmetic_op(op, expression)
            return
        self._emit_general_assignment_operation(op)

    def _emit_arithmetic_op(
        self, op: ArithmeticOperation, expression: Expression
    ) -> None:
        op, expression, is_bool_opt = self._optimize_boolean_expression(op, expression)
        if op.is_inplace:
            self._emit_inplace_arithmetic_op(op, expression, is_bool_opt)
        else:
            self._emit_general_assignment_operation(op)

    def _emit_inplace_arithmetic_op(
        self, op: ArithmeticOperation, expression: Expression, is_bool_opt: bool
    ) -> None:
        target = self._interpreter.evaluate(op.result_var).as_type(QuantumSymbol)
        if (
            op.operation_kind != ArithmeticOperationKind.InplaceXor
            or op.result_type.size_in_bits > 1
            or not self._is_res_boolean(op)
            or target.quantum_type.size_in_bits > 1
            or _is_constant(expression.expr)
        ):
            _validate_naive_inplace_handles(op)
            self._build_naive_inplace(op, expression)
            return

        op, expression, to_invert = self._adapt_boolean_inplace(
            op, expression, is_bool_opt
        )
        self._emit_general_assignment_operation(op)
        if not to_invert:
            return

        call = QuantumFunctionCall(
            function=builtins.functions.X.__name__,  # type:ignore[attr-defined]
            positional_args=[op.result_var],
            source_ref=op.source_ref,
        )
        call.set_func_decl(X.func_decl)
        self._interpreter.emit_statement(call)

    def _emit_general_assignment_operation(
        self, op: QuantumAssignmentOperation
    ) -> None:
        result = self._interpreter.evaluate(op.result_var).as_type(QuantumSymbol)
        copy_type_information(op.result_type, result.quantum_type, str(result.handle))
        self.emit_statement(op)

    def _optimize_boolean_expression(
        self, op: ArithmeticOperation, expression: Expression
    ) -> tuple[ArithmeticOperation, Expression, bool]:
        if (
            self._interpreter._is_frontend
            or op.operation_kind
            not in (
                ArithmeticOperationKind.Assignment,
                ArithmeticOperationKind.InplaceXor,
            )
            or not self._all_vars_boolean(op)
            or not self._is_res_boolean(op)
        ):
            return op, expression, False
        optimizer = BooleanExpressionOptimizer()
        optimized_expression = Expression(
            expr=ast.unparse(optimizer.visit(ast.parse(expression.expr)))
        )
        optimized_expression = self._evaluate_expression(optimized_expression)
        optimized_op = op.model_copy(update=dict(expression=optimized_expression))
        return optimized_op, optimized_expression, optimizer.is_convertible

    def _adapt_boolean_inplace(
        self, op: ArithmeticOperation, expression: Expression, is_bool_opt: bool
    ) -> tuple[ArithmeticOperation, Expression, bool]:
        adapter = BooleanExpressionFuncLibAdapter(is_bool_opt)
        adapted_expression = self._evaluate_expression(
            Expression(expr=ast.unparse(adapter.visit(ast.parse(expression.expr))))
        )
        adapted_op = op.model_copy(update=dict(expression=adapted_expression))
        return adapted_op, adapted_expression, adapter.to_invert

    def _build_naive_inplace(
        self, qe: ArithmeticOperation, new_expression: Expression
    ) -> None:
        if qe.operation_kind == ArithmeticOperationKind.InplaceXor:
            op = BinaryOperation.Xor
        elif qe.operation_kind == ArithmeticOperationKind.InplaceAdd:
            op = BinaryOperation.Addition
        else:
            raise ClassiqInternalExpansionError(
                f"Unrecognized operation kind {qe.operation_kind!r}"
            )

        if _is_constant(new_expression.expr):
            self._interpreter.emit_statement(
                InplaceBinaryOperation(
                    operation=op,
                    target=qe.result_var,
                    value=new_expression,
                )
            )
            return

        if _is_variable(new_expression.expr):
            value_var = self._interpreter.evaluate(new_expression.expr).value
            if isinstance(value_var, QuantumSymbol):
                self._interpreter.emit_statement(
                    InplaceBinaryOperation(
                        operation=op,
                        target=qe.result_var,
                        value=value_var.handle,
                    )
                )
                return

        aux_var = self._counted_name_allocator.allocate(INPLACE_ARITH_AUX_VAR_PREFIX)
        self._interpreter.emit_statement(
            VariableDeclarationStatement(name=aux_var, quantum_type=QuantumNumeric())
        )
        arith_expression = ArithmeticOperation(
            result_var=HandleBinding(name=aux_var),
            expression=new_expression,
            operation_kind=ArithmeticOperationKind.Assignment,
        )
        inplace_store = InplaceBinaryOperation(
            operation=op,
            target=qe.result_var,
            value=HandleBinding(name=aux_var),
        )
        self._interpreter.emit_statement(
            WithinApply(compute=[arith_expression], action=[inplace_store])
        )

    def _skip_assignment(self, op: QuantumAssignmentOperation, expr: str) -> bool:
        if not isinstance(op, ArithmeticOperation) or not _is_zero(expr):
            return False
        if op.operation_kind != ArithmeticOperationKind.Assignment:
            return True
        allocate_call = QuantumFunctionCall(
            function=allocate.func_decl.name,
            positional_args=[Expression(expr="1"), op.result_var],
        )
        allocate_call.set_func_decl(allocate.func_decl)
        self._interpreter.emit_statement(allocate_call)
        return True

    def _get_updated_op_split_symbols(
        self, op: QuantumAssignmentOperation, symbol_parts: SymbolParts
    ) -> QuantumAssignmentOperation:
        return op.model_copy(
            update=dict(result_var=self.rewrite(op.result_var, symbol_parts))
        )


def _validate_naive_inplace_handles(qe: ArithmeticOperation) -> None:
    if qe.result_var in qe.var_handles:
        raise ClassiqExpansionError(
            HANDLE_ERROR_MESSAGE.format(handle_str=str(demangle_handle(qe.result_var)))
        )
