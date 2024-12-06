from typing import get_args

from classiq.interface.generator.expressions.evaluated_expression import (
    EvaluatedExpression,
)
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.expressions.expression_types import ExpressionValue
from classiq.interface.model.handle_binding import HandleBinding

from classiq.model_expansions.expression_evaluator import evaluate
from classiq.model_expansions.scope import Evaluated, QuantumSymbol, Scope


def evaluate_classical_expression(expr: Expression, scope: Scope) -> Evaluated:
    all_symbols = scope.items()
    locals_dict = {
        name: EvaluatedExpression(value=evaluated.value)
        for name, evaluated in all_symbols
        if isinstance(evaluated.value, get_args(ExpressionValue))
    } | {
        name: EvaluatedExpression(
            value=evaluated.value.quantum_type.get_proxy(HandleBinding(name=name))
        )
        for name, evaluated in all_symbols
        if isinstance(evaluated.value, QuantumSymbol)
        and evaluated.value.quantum_type.has_size_in_bits
    }
    uninitialized_locals = {
        name
        for name, evaluated in all_symbols
        if isinstance(evaluated.value, QuantumSymbol)
        and not evaluated.value.quantum_type.has_size_in_bits
    }

    ret = evaluate(expr, locals_dict, uninitialized_locals)
    return Evaluated(value=ret.value)
