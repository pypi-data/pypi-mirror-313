from typing import Union

import sympy

from classiq.interface.exceptions import ClassiqExpansionError
from classiq.interface.generator.expressions.evaluated_expression import (
    EvaluatedExpression,
)
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.builtins.internal_operators import (
    POWER_OPERATOR_NAME,
)
from classiq.interface.model.power import Power

from classiq.model_expansions.closure import Closure
from classiq.model_expansions.quantum_operations.call_emitter import CallEmitter
from classiq.model_expansions.scope import Scope


class PowerEmitter(CallEmitter[Power]):
    _power_value: Union[int, sympy.Basic]
    _power_expr: Expression

    def emit(self, power: Power, /) -> None:
        if power.is_generative():
            context = self._register_generative_context(power, POWER_OPERATOR_NAME)
            power = power.model_copy(update={"body": context.statements("body")})

        self._power = power
        self._power_value = self._get_power_value()
        self._power_expr = Expression(
            expr=str(self._power_value), source_ref=power.power.source_ref
        )
        self._power_expr._evaluated_expr = EvaluatedExpression(value=self._power_value)

        if len(power.body) > 1 and isinstance(self._power_value, sympy.Basic):
            self._emit_wrapped()
            return

        self._emit_as_operation(power)

    def _emit_as_operation(self, power: Power) -> None:
        power_operation = Closure(
            name=POWER_OPERATOR_NAME,
            blocks=dict(body=self._power.body),
            scope=Scope(parent=self._current_scope),
        )
        context = self._expand_operation(power_operation)
        self.emit_statement(
            Power(
                body=context.statements("body"),
                power=self._power_expr,
                source_ref=power.source_ref,
            )
        )

    def _emit_wrapped(self) -> None:
        wrapping_function = self._create_expanded_wrapping_function(
            POWER_OPERATOR_NAME, self._power.body
        )
        self.emit_statement(
            Power(
                body=[wrapping_function],
                power=self._power_expr,
                source_ref=self._power.source_ref,
            )
        )

    def _get_power_value(self) -> Union[int, sympy.Basic]:
        power_value = self._interpreter.evaluate(self._power.power).value
        if isinstance(power_value, int) and power_value < 0:
            raise ClassiqExpansionError(
                f"power exponent must be non-negative, got {power_value}"
            )
        return power_value
