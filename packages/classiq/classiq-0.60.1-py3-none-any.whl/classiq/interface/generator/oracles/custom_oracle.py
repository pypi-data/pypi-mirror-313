from typing import Any

import pydantic

from classiq.interface.exceptions import ClassiqValueError
from classiq.interface.generator.function_params import parse_function_params_values
from classiq.interface.generator.oracles.oracle_abc import (
    ArithmeticIODict,
    OracleABC,
    VariableBinResultMap,
    VariableTypedResultMap,
)
from classiq.interface.generator.user_defined_function_params import CustomFunction

QubitState = str


class CustomOracle(OracleABC[QubitState]):
    custom_oracle: str = pydantic.Field(description="Oracle function")
    custom_oracle_params: CustomFunction = pydantic.Field(
        description="Oracle function parameters",
        default_factory=CustomFunction,
    )

    @pydantic.model_validator(mode="before")
    @classmethod
    def _parse_oracle(cls, values: Any) -> dict[str, Any]:
        if isinstance(values, dict):
            parse_function_params_values(
                values=values,
                params_key="custom_oracle_params",
                discriminator_key="custom_oracle",
                param_classes={CustomFunction},
                default_parser_class=CustomFunction,
            )
        return values

    @pydantic.field_validator("custom_oracle_params")
    @classmethod
    def _validate_names_match_oracle(
        cls, custom_oracle_params: CustomFunction
    ) -> CustomFunction:
        if set(custom_oracle_params.input_decls.keys()) != set(
            custom_oracle_params.output_decls.keys()
        ):
            raise ClassiqValueError("Oracle IO names must be identical")
        if any(
            custom_oracle_params.output_decls[name].size != input_decl.size
            for name, input_decl in custom_oracle_params.input_decls.items()
        ):
            raise ClassiqValueError("Oracle IO sizes must be identical")
        return custom_oracle_params

    def _get_register_transputs(self) -> ArithmeticIODict:
        return {**self.custom_oracle_params.input_decls}

    def binary_result_to_typed_result(
        self, bin_result: VariableBinResultMap
    ) -> VariableTypedResultMap[QubitState]:
        return bin_result

    def is_good_result(
        self, problem_result: VariableTypedResultMap[QubitState]
    ) -> bool:
        return True
