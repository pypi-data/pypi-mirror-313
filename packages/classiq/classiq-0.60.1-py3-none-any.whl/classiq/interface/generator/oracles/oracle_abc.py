import abc
from collections.abc import Sequence
from typing import Generic, Optional, TypeVar

import numpy as np

from classiq.interface.exceptions import ClassiqOracleError
from classiq.interface.executor.result import State
from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.function_params import ArithmeticIODict, FunctionParams
from classiq.interface.generator.generated_circuit_data import IOQubitMapping

ProblemResultType = TypeVar("ProblemResultType")

VariableBinResultMap = dict[str, State]
VariableTypedResultMap = dict[str, ProblemResultType]


class OracleABC(abc.ABC, FunctionParams, Generic[ProblemResultType]):
    def get_power_order(self) -> Optional[int]:
        return 2

    @abc.abstractmethod
    def _get_register_transputs(self) -> ArithmeticIODict:
        pass

    def _create_ios(self) -> None:
        self._inputs = self._get_register_transputs()
        self._outputs = {**self._inputs}

    def is_good_state(self, state: str, indices: IOQubitMapping) -> bool:
        bin_result = self.split_state_by_variables(state, indices)
        problem_result = self.binary_result_to_typed_result(bin_result)
        return self.is_good_result(problem_result)

    def split_state_by_variables(
        self, state: str, indices: IOQubitMapping
    ) -> VariableBinResultMap:
        self._check_indices(indices)

        input_values: VariableBinResultMap = {}
        state_as_array = np.array(list(state))
        for var_name, var_indices in indices.items():
            var_string = "".join(
                state_as_array[sorted(_reverse_endianness(var_indices, len(state)))]
            )
            input_values[var_name] = var_string
        return input_values

    @abc.abstractmethod
    def binary_result_to_typed_result(
        self, bin_result: VariableBinResultMap
    ) -> VariableTypedResultMap[ProblemResultType]:
        pass

    @abc.abstractmethod
    def is_good_result(
        self, problem_result: VariableTypedResultMap[ProblemResultType]
    ) -> bool:
        pass

    def variables(self) -> list[RegisterUserInput]:
        return [
            RegisterUserInput.from_arithmetic_info(info=info, name=name)
            for name, info in self._inputs.items()
        ]

    def _check_indices(self, indices: IOQubitMapping) -> None:
        if set(indices.keys()) != {reg.name for reg in self.variables()}:
            raise ClassiqOracleError(
                "Argument name mismatch between indices and registers"
            )


def _reverse_endianness(indices: Sequence[int], state_length: int) -> list[int]:
    return [state_length - 1 - index for index in indices]
