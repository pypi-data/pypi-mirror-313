from typing import Any, Final, Optional

import networkx as nx
import pydantic
from pydantic_core.core_schema import ValidationInfo

from classiq.interface.exceptions import ClassiqValueError
from classiq.interface.generator.arith import arithmetic_expression_parser
from classiq.interface.generator.arith.arithmetic_expression_abc import (
    ArithmeticExpressionABC,
)
from classiq.interface.generator.arith.arithmetic_param_getters import (
    id2op,
    operation_allows_target,
)
from classiq.interface.generator.arith.arithmetic_result_builder import (
    ArithmeticResultBuilder,
)
from classiq.interface.generator.arith.register_user_input import RegisterArithmeticInfo
from classiq.interface.model.quantum_type import (
    QuantumType,
    quantum_var_to_register,
    register_info_to_quantum_type,
)

ARITHMETIC_EXPRESSION_TARGET_NAME: Final[str] = "arithmetic_target"
ARITHMETIC_EXPRESSION_RESULT_NAME: Final[str] = "expression_result"
ARITHMETIC_EXPRESSION_GARBAGE_NAME: Final[str] = "expression_garbage"


class Arithmetic(ArithmeticExpressionABC):
    target: Optional[RegisterArithmeticInfo] = None
    inputs_to_save: set[str] = pydantic.Field(default_factory=set)

    @pydantic.field_validator("inputs_to_save")
    @classmethod
    def _validate_inputs_to_save(
        cls, inputs_to_save: set[str], info: ValidationInfo
    ) -> set[str]:
        assert all(reg in info.data.get("definitions", {}) for reg in inputs_to_save)
        return inputs_to_save

    @staticmethod
    def _validate_expression_graph(graph: nx.DiGraph, values: dict[str, Any]) -> None:
        target = values.get("target")
        if target is None:
            return

        # Check that the expression graph allows setting the target of the expression
        if not all(
            degree or operation_allows_target(id2op(node))
            for node, degree in graph.out_degree
        ):
            raise ClassiqValueError("Expression does not support target assignment")

    def _create_ios(self) -> None:
        self._inputs = {
            name: register
            for name, register in self.definitions.items()
            if name in self._get_literal_set()
            and isinstance(register, RegisterArithmeticInfo)
        }
        self._outputs = {
            name: self._inputs[name]
            for name in self.inputs_to_save
            if name in self._inputs
        }
        # TODO: avoid calling the result builder again, as it is called in validation
        result_builder = ArithmeticResultBuilder(
            graph=arithmetic_expression_parser.parse_expression(self.expression),
            definitions=self.definitions,
            machine_precision=self.machine_precision,
        )
        self._outputs[ARITHMETIC_EXPRESSION_RESULT_NAME] = result_builder.result
        if result_builder.garbage:
            self._outputs[ARITHMETIC_EXPRESSION_GARBAGE_NAME] = result_builder.garbage
        if self.target:
            self._inputs[ARITHMETIC_EXPRESSION_TARGET_NAME] = self.target


def get_arithmetic_params(
    expr_str: str,
    var_types: dict[str, QuantumType],
    machine_precision: int,
    enable_target: bool = False,
) -> Arithmetic:
    return Arithmetic(
        expression=expr_str,
        definitions={
            name: quantum_var_to_register(name, qtype)
            for name, qtype in var_types.items()
        },
        inputs_to_save=set(var_types.keys()),
        # FIXME: generalize inout target to multiple qubits
        target=RegisterArithmeticInfo(size=1) if enable_target else None,
        machine_precision=machine_precision,
    )


def compute_arithmetic_result_type(
    expr_str: str, var_types: dict[str, QuantumType], machine_precision: int
) -> QuantumType:
    arith_param = get_arithmetic_params(expr_str, var_types, machine_precision)
    return register_info_to_quantum_type(
        arith_param.outputs[ARITHMETIC_EXPRESSION_RESULT_NAME]
    )
