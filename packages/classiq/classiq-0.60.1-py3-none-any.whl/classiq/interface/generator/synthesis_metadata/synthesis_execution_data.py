from typing import Optional

import pydantic
import sympy

from classiq.interface.backend.pydantic_backend import PydanticExecutionParameter
from classiq.interface.exceptions import ClassiqValueError
from classiq.interface.generator.parameters import ParameterType


class FunctionExecutionData(pydantic.BaseModel):
    power_parameter: Optional[ParameterType] = pydantic.Field(default=None)

    @property
    def power_var(self) -> Optional[str]:
        if self.power_parameter is None:
            return None
        power_vars = sympy.sympify(self.power_parameter).free_symbols
        if len(power_vars) != 1:
            raise ClassiqValueError(
                f"Power parameter expression: {self.power_parameter} must contain exactly one variable"
            )
        return str(list(power_vars)[0])


class ExecutionData(pydantic.BaseModel):
    function_execution: dict[str, FunctionExecutionData] = pydantic.Field(
        default_factory=dict
    )

    @property
    def execution_parameters(
        self,
    ) -> set[PydanticExecutionParameter]:
        return {
            function_execution_data.power_var
            for function_execution_data in self.function_execution.values()
            if function_execution_data.power_var is not None
        }
