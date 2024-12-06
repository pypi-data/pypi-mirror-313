from typing import Any, Union

import pydantic
from pydantic_core.core_schema import ValidationInfo

from classiq.interface.exceptions import ClassiqValueError
from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.function_params import (
    ArithmeticIODict,
    FunctionParams,
    parse_function_params_values,
)
from classiq.interface.generator.state_preparation import StatePreparation
from classiq.interface.generator.user_defined_function_params import CustomFunction

GroverStatePreparation = Union[StatePreparation, CustomFunction]


class GroverDiffuser(FunctionParams):
    variables: list[RegisterUserInput]
    state_preparation: str = pydantic.Field(
        default="", description="State preparation function"
    )
    state_preparation_params: GroverStatePreparation = pydantic.Field(
        description="State preparation function parameters",
        default_factory=CustomFunction,
    )

    def _create_ios(self) -> None:
        self._inputs = {reg.name: reg for reg in self.variables}
        self._outputs = {reg.name: reg for reg in self.variables}

    @pydantic.model_validator(mode="before")
    @classmethod
    def _validate_state_preparation_name(cls, values: Any) -> dict[str, Any]:
        if (
            isinstance(values, dict)
            and isinstance(values.get("state_preparation_params"), CustomFunction)
            and not values.get("state_preparation")
        ):
            raise ClassiqValueError(
                "Must receive the function name from the `state_preparation` field for user defined functions"
            )
        return values

    @pydantic.model_validator(mode="before")
    @classmethod
    def _parse_state_preparation(cls, values: Any) -> dict[str, Any]:
        if isinstance(values, dict):
            parse_function_params_values(
                values=values,
                params_key="state_preparation_params",
                discriminator_key="state_preparation",
                param_classes={StatePreparation, CustomFunction},
                default_parser_class=CustomFunction,
            )
        return values

    @pydantic.field_validator("variables")
    @classmethod
    def _validate_variables(
        cls, variables: list[RegisterUserInput]
    ) -> list[RegisterUserInput]:
        names = {reg.name for reg in variables}
        assert len(variables) == len(names), "Repeating names not allowed"
        return variables

    @pydantic.field_validator("state_preparation_params")
    @classmethod
    def _validate_state_preparation(
        cls, state_preparation_params: GroverStatePreparation, info: ValidationInfo
    ) -> GroverStatePreparation:
        variables = info.data.get("variables", list())
        sp_inputs = state_preparation_params.inputs_full(strict_zero_ios=False)
        sp_outputs = state_preparation_params.outputs
        if len(sp_inputs) == 1 and len(sp_outputs) == 1:
            var_size = sum(reg.size for reg in variables)
            assert (
                state_preparation_params.num_input_qubits(strict_zero_ios=False)
                == var_size
            )
            assert state_preparation_params.num_output_qubits == var_size
        else:
            variable_names_and_sizes = cls._names_and_sizes(
                {var.name: var for var in variables}
            )
            assert cls._names_and_sizes(sp_inputs) == variable_names_and_sizes
            assert cls._names_and_sizes(sp_outputs) == variable_names_and_sizes
        return state_preparation_params

    @staticmethod
    def _names_and_sizes(transputs: ArithmeticIODict) -> set[tuple[str, int]]:
        return {(name, reg.size) for name, reg in transputs.items()}
