import ast
from collections.abc import Mapping
from enum import EnumMeta
from typing import Any, Optional

from sympy import sympify

from classiq.interface.exceptions import ClassiqExpansionError
from classiq.interface.generator.constant import Constant
from classiq.interface.generator.expressions.evaluated_expression import (
    EvaluatedExpression,
)
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.expressions.expression_constants import (
    CPARAM_EXECUTION_SUFFIX,
)
from classiq.interface.generator.expressions.expression_types import ExpressionValue
from classiq.interface.generator.expressions.sympy_supported_expressions import (
    SYMPY_SUPPORTED_EXPRESSIONS,
)

from classiq.model_expansions.atomic_expression_functions_defs import (
    ATOMIC_EXPRESSION_FUNCTIONS,
    qmod_val_to_python,
)
from classiq.model_expansions.model_tables import SymbolTable
from classiq.model_expansions.sympy_conversion.expression_to_sympy import (
    translate_to_sympy,
)
from classiq.model_expansions.sympy_conversion.sympy_to_python import sympy_to_python
from classiq.qmod import symbolic


def evaluate_constants(constants: list[Constant]) -> dict[str, EvaluatedExpression]:
    result: dict[str, EvaluatedExpression] = {}
    for constant in constants:
        result[constant.name] = evaluate(constant.value, result)
    return result


def evaluate_constants_as_python(constants: list[Constant]) -> dict[str, Any]:
    evaluated = evaluate_constants(constants)
    return {
        constant.name: qmod_val_to_python(
            evaluated[constant.name].value, constant.const_type
        )
        for constant in constants
    }


def evaluate(
    expr: Expression,
    locals_dict: Mapping[str, EvaluatedExpression],
    uninitialized_locals: Optional[set[str]] = None,
) -> EvaluatedExpression:
    model_locals: dict[str, ExpressionValue] = {}
    model_locals.update(ATOMIC_EXPRESSION_FUNCTIONS)
    model_locals.update(SymbolTable.enum_table.enums)
    # locals override builtin-functions
    model_locals.update({name: expr.value for name, expr in locals_dict.items()})
    uninitialized_locals = uninitialized_locals or set()

    _validate_undefined_vars(expr.expr, model_locals, uninitialized_locals)

    sympy_expr = translate_to_sympy(expr.expr)
    try:
        sympify_result = sympify(sympy_expr, locals=model_locals)
    except (TypeError, IndexError) as e:
        raise ClassiqExpansionError(str(e)) from None
    except AttributeError as e:
        if isinstance(e.obj, EnumMeta):
            raise ClassiqExpansionError(
                f"Enum {e.obj.__name__} has no member {e.name!r}. Available members: "
                f"{', '.join(e.obj.__members__)}"
            ) from e
        raise

    return EvaluatedExpression(
        value=sympy_to_python(sympify_result, locals=model_locals)
    )


def _validate_undefined_vars(
    expr: str,
    model_locals: dict[str, ExpressionValue],
    uninitialized_locals: Optional[set[str]],
) -> None:
    uninitialized_locals = uninitialized_locals or set()
    id_visitor = _VarsCollector()
    id_visitor.visit(ast.parse(expr))
    identifiers = id_visitor.vars
    undefined_vars = (
        identifiers
        - model_locals.keys()
        - set(SYMPY_SUPPORTED_EXPRESSIONS)
        - set(symbolic.__all__)
        - uninitialized_locals
    )

    # Ignore expanded execution parameters
    undefined_vars = {
        var for var in undefined_vars if not var.endswith(CPARAM_EXECUTION_SUFFIX)
    }

    if len(undefined_vars) == 1:
        undefined_var = undefined_vars.__iter__().__next__()
        raise ClassiqExpansionError(f"Variable {undefined_var!r} is undefined")
    elif len(undefined_vars) > 1:
        raise ClassiqExpansionError(f"Variables {list(undefined_vars)} are undefined")


class _VarsCollector(ast.NodeTransformer):
    def __init__(self) -> None:
        self.vars: set[str] = set()

    def visit_Name(self, node: ast.Name) -> None:
        self.vars.add(node.id)

    def visit_Call(self, node: ast.Call) -> None:
        func = node.func
        self.visit(func)
        if not isinstance(func, ast.Name) or func.id != "struct_literal":
            for arg in node.args:
                self.visit(arg)
        for kw in node.keywords:
            self.visit(kw)
