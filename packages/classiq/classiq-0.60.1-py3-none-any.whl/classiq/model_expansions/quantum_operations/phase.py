from typing import TYPE_CHECKING

import sympy
from sympy import sympify

from classiq.interface.exceptions import ClassiqExpansionError
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.model.bind_operation import BindOperation
from classiq.interface.model.handle_binding import HANDLE_ID_SEPARATOR, HandleBinding
from classiq.interface.model.phase_operation import PhaseOperation
from classiq.interface.model.quantum_function_call import QuantumFunctionCall
from classiq.interface.model.quantum_type import (
    QuantumBitvector,
    QuantumNumeric,
    QuantumScalar,
)
from classiq.interface.model.variable_declaration_statement import (
    VariableDeclarationStatement,
)
from classiq.interface.model.within_apply_operation import WithinApply

from classiq.applications.combinatorial_helpers.transformations.ising_converter import (
    _find_sub_list_items,
    _get_vars,
    _refine_ising_expr,
    _to_ising_symbolic_objective_function,
)
from classiq.model_expansions.quantum_operations.expression_operation import (
    ExpressionOperationEmitter,
)
from classiq.qmod.builtins.functions.exponentiation import suzuki_trotter
from classiq.qmod.semantics.error_manager import ErrorManager


class PhaseEmitter(ExpressionOperationEmitter[PhaseOperation]):
    def _negate_expression(self, expression: Expression, /) -> Expression:
        return self._evaluate_expression(
            expression.model_copy(update=dict(expr=f"-({expression.expr})"))
        )

    def emit(self, phase_op: PhaseOperation, /) -> None:
        phase_expression = self._evaluate_op_expression(phase_op)
        phase_op = phase_op.model_copy(update=dict(expression=phase_expression))
        arrays_with_subscript = self.split_symbols(
            phase_op.expression, self._counted_name_allocator.allocate
        )
        if len(arrays_with_subscript) > 0:
            self._emit_with_split(phase_op, phase_op.expression, arrays_with_subscript)
            return

        phase_op = phase_op.model_copy(
            update=dict(expression=self._negate_expression(phase_op.expression))
        )
        phase_op = self._evaluate_types_in_expression(phase_op, phase_op.expression)
        if len(phase_op.var_handles) == 0:
            ErrorManager().add_error(
                "Cannot perform phase operation on an expression with no quantum variables."
            )
            return

        aux_name = self._counted_name_allocator.allocate("phase_aux")
        if len(phase_op.var_handles) > 1:
            split_join = True
            evolution_variable = HandleBinding(name=aux_name)
        else:
            split_join = False
            evolution_variable = phase_op.var_handles[0]
        expression = self._evaluate_op_expression(phase_op)
        expression_evolution_function = QuantumFunctionCall(
            function=suzuki_trotter.func_decl.name,
            positional_args=[
                _convert_cost_expression_to_hamiltonian(
                    expression.expr,
                    {
                        var.name: self._current_scope[var.name].value.quantum_type
                        for var in phase_op.var_handles
                    },
                ),
                phase_op.theta,
                Expression(expr="1"),
                Expression(expr="1"),
                evolution_variable,
            ],
            source_ref=phase_op.source_ref,
        )
        expression_evolution_function.set_func_decl(suzuki_trotter.func_decl)

        if split_join:
            self._interpreter.emit_statement(
                VariableDeclarationStatement(
                    name=aux_name, quantum_type=QuantumBitvector()
                )
            )
            self._interpreter.emit_statement(
                WithinApply(
                    compute=[
                        BindOperation(
                            in_handles=phase_op.var_handles,
                            out_handles=[HandleBinding(name=aux_name)],
                        )
                    ],
                    action=[expression_evolution_function],
                    source_ref=phase_op.source_ref,
                )
            )
        else:
            self._interpreter.emit_statement(
                expression_evolution_function,
            )


def _get_single_bit_vars_expression(
    expr: sympy.Expr, vars_info: dict[str, QuantumScalar]
) -> tuple[sympy.Expr, list[sympy.Symbol]]:
    bit_vars = []
    for var_name, var_info in vars_info.items():
        size = var_info.size_in_bits
        var = sympy.Symbol(var_name)
        if size == 1:
            bits = [var]
            is_signed = False
            fraction_places = 0
        else:
            if TYPE_CHECKING:
                assert isinstance(var_info, QuantumNumeric)
            bits = [
                sympy.Symbol(f"{var_name}{HANDLE_ID_SEPARATOR}{i}__split__")
                for i in range(size)
            ]
            is_signed = var_info.sign_value
            fraction_places = var_info.fraction_digits_value
        bit_vars.extend(bits)
        split_var = 0
        for i, bit in enumerate(bits):
            if is_signed and i == size - 1:  # sign bit (MSB)
                split_var -= bit * 2 ** (size - 1 - fraction_places)
            else:
                split_var += bit * 2 ** (i - fraction_places)
        expr = expr.subs(var, split_var)
    return expr, bit_vars


def _convert_ising_sympy_to_pauli_terms(
    ising_expr: sympy.Expr, ordered_sympy_vars: list[sympy.Symbol]
) -> str:
    pauli_terms: list[str] = []
    coefficients = ising_expr.as_coefficients_dict(*ordered_sympy_vars)
    for expr_term in ising_expr.args:
        expr_vars = _get_vars(expr_term)
        z_vec = _find_sub_list_items(ordered_sympy_vars, expr_vars)
        pauli_elements = ["I"] * len(z_vec)
        for index, is_z_op in enumerate(z_vec):
            if is_z_op:
                pauli_elements[len(z_vec) - index - 1] = (
                    "Z"  # reminder: Pauli reverses the order!
                )
        term_var = sympy.Mul(
            *(var for i, var in enumerate(ordered_sympy_vars) if z_vec[i])
        )
        coeff = float(coefficients[term_var])
        paulis = [f"Pauli.{pauli}" for pauli in pauli_elements]
        pauli_terms.append(
            # fmt: off
                    "struct_literal("
                    "PauliTerm,"
                    f"pauli=[{', '.join(paulis)}],"
                    f"coefficient={Expression(expr=str(coeff))},"
                    ")"
            # fmt: on,
        )
    return f"[{', '.join(pauli_terms)}]"


def _convert_cost_expression_to_hamiltonian(
    expr: str,
    vars: dict[str, QuantumScalar],
) -> Expression:
    sympy_expr = sympify(expr)
    single_bit_vars_expression, single_bit_vars = _get_single_bit_vars_expression(
        sympy_expr, vars
    )
    if not single_bit_vars_expression.is_polynomial():
        raise ClassiqExpansionError(f"phased expression {expr!r} is not polynomial")

    ising_expr = _to_ising_symbolic_objective_function(single_bit_vars_expression)
    ising_expr = _refine_ising_expr(ising_expr)

    return Expression(
        expr=_convert_ising_sympy_to_pauli_terms(ising_expr, single_bit_vars)
    )
