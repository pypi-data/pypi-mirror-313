import ast
import re

import numexpr  # type: ignore[import]

from classiq.interface.exceptions import ClassiqArithmeticError, ClassiqValueError
from classiq.interface.generator.arith import number_utils
from classiq.interface.generator.arith.arithmetic import Arithmetic
from classiq.interface.generator.arith.arithmetic_expression_abc import (
    ArithmeticExpressionABC,
)
from classiq.interface.generator.arith.register_user_input import RegisterArithmeticInfo
from classiq.interface.generator.oracles.oracle_abc import (
    ArithmeticIODict,
    OracleABC,
    VariableBinResultMap,
    VariableTypedResultMap,
)


class ArithmeticOracle(OracleABC[float], ArithmeticExpressionABC):
    @staticmethod
    def _validate_ast_obj(ast_obj: ast.AST) -> None:
        if not isinstance(ast_obj, ast.Expression):
            raise ClassiqValueError("Must be an expression")
        if not isinstance(ast_obj.body, (ast.Compare, ast.BoolOp)):
            raise ClassiqValueError("Must be a comparison expression")

    def get_arithmetic_expression_params(self) -> Arithmetic:
        return Arithmetic(
            machine_precision=self.machine_precision,
            expression=self.expression,
            definitions=self.definitions,
            uncomputation_method=self.uncomputation_method,
            qubit_count=self.qubit_count,
            target=RegisterArithmeticInfo(size=1),
            inputs_to_save=set(self.definitions.keys()),
        )

    def _get_register_transputs(self) -> ArithmeticIODict:
        return {
            name: register
            for name, register in self.definitions.items()
            if name in self._get_literal_set()
            and isinstance(register, RegisterArithmeticInfo)
        }

    def is_good_result(self, problem_result: VariableTypedResultMap[float]) -> bool:
        expression = self._simplify_negations_of_boolean_variables(
            expression=self.expression, input_definitions=self.inputs
        )
        for var_name, value in problem_result.items():
            expression = re.sub(r"\b" + var_name + r"\b", str(value), expression)
        try:
            return bool(numexpr.evaluate(expression).item())
        except TypeError:
            raise ClassiqArithmeticError(
                f"Cannot evaluate expression {expression}"
            ) from None

    @staticmethod
    def _simplify_negations_of_boolean_variables(
        expression: str, input_definitions: dict[str, RegisterArithmeticInfo]
    ) -> str:
        for var_name in input_definitions:
            if getattr(input_definitions[var_name], "size", 0) == 1:
                expression = re.sub(
                    rf"~\s*{var_name}\b", f"(1 - {var_name})", expression
                )
        return expression

    def binary_result_to_typed_result(
        self, bin_result: VariableBinResultMap
    ) -> VariableTypedResultMap[float]:
        typed_result: VariableTypedResultMap[float] = {}
        for var_name, var_string in bin_result.items():
            var = self.inputs[var_name]
            var_value = number_utils.binary_to_float_or_int(
                var_string, var.fraction_places, var.is_signed
            )
            typed_result[var_name] = var_value
        return typed_result
