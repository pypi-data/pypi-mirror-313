from typing import Any, Optional

import pydantic
from pydantic import ConfigDict
from pydantic_core.core_schema import ValidationInfo
from typing_extensions import Self

from classiq.interface.exceptions import ClassiqMismatchIOsError, ClassiqValueError
from classiq.interface.generator.arith.register_user_input import RegisterArithmeticInfo
from classiq.interface.generator.function_param_list_without_self_reference import (
    function_param_library_without_self_reference,
)
from classiq.interface.generator.function_params import (
    DEFAULT_ZERO_NAME,
    FunctionParams,
    IOName,
    parse_function_params_values,
)
from classiq.interface.generator.hamiltonian_evolution.exponentiation import (
    Exponentiation,
)
from classiq.interface.generator.user_defined_function_params import CustomFunction

PHASE_ESTIMATION_DEFAULT_OUTPUT_NAME = "PHASE_ESTIMATION"
CUSTOM_FUNCTIONS_IO_MISMATCH_ERROR = (
    "Custom function provided to the QPE has different input and output names."
)


class ExponentiationScaling(pydantic.BaseModel):
    """
    Details of exponentiation scaling for phase estimation.
    """

    max_depth: pydantic.PositiveInt = pydantic.Field(
        description="The max_depth of the smallest exponentiation",
    )
    max_depth_scaling_factor: pydantic.NonNegativeFloat = pydantic.Field(
        default=2.0,
        description="The scaling factor of the exponentiation max_depth; defaults to 2.",
    )
    model_config = ConfigDict(frozen=True)


class ExponentiationSpecification(pydantic.BaseModel):
    """
    Specifications of individual Exponentiation details for each qubit; only valid if Exponentiation is given as unitary_params for PhaseEstimation.
    This sets the optimization to ExponentiationOptimization.MINIMIZE_ERROR and overrides the max_depth constraints.
    """

    scaling: Optional[ExponentiationScaling] = pydantic.Field(
        default=None,
        description="The scaling of the exponentiation functions.",
    )
    max_depths: Optional[tuple[pydantic.NonNegativeInt, ...]] = pydantic.Field(
        default=None,
        description="The max_depth of each exponentiation function; overrides scaling.",
    )
    model_config = ConfigDict(frozen=True)

    @pydantic.model_validator(mode="after")
    def _validate_exponentiation_specification(self) -> Self:
        if self.scaling is None and self.max_depths is None:
            raise ClassiqValueError("At least one specification must be provided.")
        return self


class PhaseEstimation(FunctionParams):
    """
    Quantum phase estimation of a given unitary function.
    """

    size: pydantic.PositiveInt = pydantic.Field(
        description="The number of qubits storing the estimated phase."
    )
    unitary: str = pydantic.Field(
        description="The unitary function for phase estimation.",
    )
    unitary_params: FunctionParams = pydantic.Field(
        description="The unitary function parameters.",
        default_factory=CustomFunction,
    )
    exponentiation_specification: Optional[ExponentiationSpecification] = (
        pydantic.Field(
            default=None,
            description="The specifications for phase estimation of exponentiation functions.",
        )
    )

    _output_name: IOName = pydantic.PrivateAttr(
        default=PHASE_ESTIMATION_DEFAULT_OUTPUT_NAME
    )

    @property
    def output_name(self) -> str:
        return self._output_name

    def _create_ios(self) -> None:
        self._inputs = {**self.unitary_params.inputs}
        self._outputs = {**self.unitary_params.outputs}
        self._outputs[self._output_name] = RegisterArithmeticInfo(size=self.size)
        self._create_zero_input_registers({DEFAULT_ZERO_NAME: self.size})

    @pydantic.model_validator(mode="before")
    @classmethod
    def _validate_composite_name(cls, values: Any) -> dict[str, Any]:
        if not isinstance(values, dict):
            return values
        unitary_params = values.get("unitary_params")
        unitary = values.get("unitary")

        if isinstance(unitary_params, CustomFunction) and not unitary:
            raise ClassiqValueError(
                "`PhaseEstimation` of a user define function (`CustomFunction`) must receive the function name from the `unitary` field"
            )
        return values

    @pydantic.model_validator(mode="before")
    @classmethod
    def _parse_function_params(
        cls, values: Any, info: ValidationInfo
    ) -> dict[str, Any]:
        vals = info.data.copy() if info.data else {}
        if isinstance(values, dict):
            vals = values
        elif isinstance(values, PhaseEstimation):
            vals = values.model_dump()

        parse_function_params_values(
            values=vals,
            params_key="unitary_params",
            discriminator_key="unitary",
            param_classes=function_param_library_without_self_reference.param_list,
            default_parser_class=CustomFunction,
        )
        return vals

    @pydantic.field_validator("unitary_params")
    @classmethod
    def _validate_unitary_params(cls, unitary_params: FunctionParams) -> FunctionParams:
        if not unitary_params.is_powerable():
            if isinstance(unitary_params, CustomFunction):
                raise ClassiqMismatchIOsError(CUSTOM_FUNCTIONS_IO_MISMATCH_ERROR)
            raise ClassiqValueError(
                f"Phase estimation of {unitary_params.discriminator()} is currently not supported."
            )
        return unitary_params

    @pydantic.field_validator("exponentiation_specification")
    @classmethod
    def _validate_exponentiation_specification(
        cls,
        exponentiation_specification: Optional[ExponentiationSpecification],
        validation_info: ValidationInfo,
    ) -> Optional[ExponentiationSpecification]:
        if exponentiation_specification is None:
            return exponentiation_specification
        unitary_params = validation_info.data.get("unitary_params")
        if not isinstance(unitary_params, Exponentiation):
            raise ClassiqValueError(
                "exponentiation_specification is only valid for Exponentiation unitary_params."
            )
        if exponentiation_specification.max_depths is not None and len(
            exponentiation_specification.max_depths
        ) != validation_info.data.get("size"):
            raise ClassiqValueError(
                "Length of max_depths must match the provided size."
            )
        return exponentiation_specification
