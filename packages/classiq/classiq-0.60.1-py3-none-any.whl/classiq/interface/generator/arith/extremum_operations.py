import abc
from collections.abc import Iterable
from typing import Any

import pydantic

from classiq.interface.exceptions import ClassiqValueError
from classiq.interface.generator.arith import argument_utils, number_utils
from classiq.interface.generator.arith.argument_utils import RegisterOrConst
from classiq.interface.generator.arith.arithmetic_operations import (
    MODULO_WITH_FRACTION_PLACES_ERROR_MSG,
    ArithmeticOperationParams,
)
from classiq.interface.generator.arith.binary_ops import (
    DEFAULT_LEFT_ARG_NAME,
    DEFAULT_RIGHT_ARG_NAME,
)
from classiq.interface.generator.arith.register_user_input import RegisterArithmeticInfo
from classiq.interface.generator.function_params import get_zero_input_name

Numeric = (float, int)


class Extremum(ArithmeticOperationParams):
    left_arg: RegisterOrConst
    right_arg: RegisterOrConst

    @pydantic.model_validator(mode="before")
    @classmethod
    def _validate_one_is_register(cls, values: Any) -> dict[str, Any]:
        if isinstance(values, dict):
            left_arg = values.get("left_arg")
            right_arg = values.get("right_arg")
            if isinstance(left_arg, Numeric) and isinstance(right_arg, Numeric):
                raise ClassiqValueError("One argument must be a register")
            if left_arg is right_arg and isinstance(left_arg, pydantic.BaseModel):
                # In case both arguments refer to the same object, copy it.
                # This prevents changes performed on one argument from affecting the other.
                values["right_arg"] = left_arg.model_copy(deep=True)
        return values

    def _create_ios(self) -> None:
        self._inputs = dict()
        if isinstance(self.left_arg, RegisterArithmeticInfo):
            self._inputs[DEFAULT_LEFT_ARG_NAME] = self.left_arg
        if isinstance(self.right_arg, RegisterArithmeticInfo):
            self._inputs[DEFAULT_RIGHT_ARG_NAME] = self.right_arg
        zero_input_name = get_zero_input_name(self.output_name)
        self._zero_inputs = {zero_input_name: self.result_register}
        self._outputs = {**self._inputs, self.output_name: self.result_register}

    def is_inplaced(self) -> bool:
        return False

    def get_params_inplace_options(self) -> Iterable["Extremum"]:
        return ()

    @classmethod
    @abc.abstractmethod
    def _bound_calculator(cls, arg1: float, arg2: float) -> float:
        pass

    @staticmethod
    def _less_qubits_arg(
        arg1: RegisterOrConst, arg2: RegisterOrConst
    ) -> RegisterOrConst:
        if not isinstance(arg1, RegisterArithmeticInfo):
            return arg1
        if not isinstance(arg2, RegisterArithmeticInfo):
            return arg2
        return arg1 if arg1.size <= arg2.size else arg2

    @classmethod
    @abc.abstractmethod
    def preferred_arg(
        cls, arg1: RegisterOrConst, arg2: RegisterOrConst
    ) -> RegisterOrConst:
        pass

    def _get_result_register(self) -> RegisterArithmeticInfo:
        eff_left_arg = argument_utils.limit_fraction_places(
            self.left_arg, self.machine_precision
        )
        eff_right_arg = argument_utils.limit_fraction_places(
            self.right_arg, self.machine_precision
        )
        if argument_utils.arg_bounds_overlap((eff_left_arg, eff_right_arg)):
            return self._get_general_case_result_register(eff_left_arg, eff_right_arg)
        return argument_utils.as_arithmetic_info(
            self.preferred_arg(eff_left_arg, eff_right_arg)
        )

    def _get_general_case_result_register(
        self, eff_left_arg: RegisterOrConst, eff_right_arg: RegisterOrConst
    ) -> RegisterArithmeticInfo:
        integer_part_size = max(
            argument_utils.integer_part_size(eff_left_arg),
            argument_utils.integer_part_size(eff_right_arg),
        )
        fraction_places = max(
            argument_utils.fraction_places(eff_left_arg),
            argument_utils.fraction_places(eff_right_arg),
        )
        required_size = integer_part_size + fraction_places
        bounds = (
            self._bound_calculator(
                argument_utils.lower_bound(eff_left_arg),
                argument_utils.lower_bound(eff_right_arg),
            ),
            self._bound_calculator(
                argument_utils.upper_bound(eff_left_arg),
                argument_utils.upper_bound(eff_right_arg),
            ),
        )
        if self.output_size:
            if fraction_places:
                raise ValueError(MODULO_WITH_FRACTION_PLACES_ERROR_MSG)
            max_bounds = RegisterArithmeticInfo.get_maximal_bounds(
                size=self.output_size, is_signed=False, fraction_places=0
            )
            bounds = number_utils.bounds_cut(bounds, max_bounds)
        size = self.output_size or required_size
        is_signed = self._include_sign and min(bounds) < 0
        return RegisterArithmeticInfo(
            size=size,
            fraction_places=fraction_places,
            is_signed=is_signed,
            bounds=self._legal_bounds(
                bounds,
                RegisterArithmeticInfo.get_maximal_bounds(
                    size=size, is_signed=is_signed, fraction_places=fraction_places
                ),
            ),
        )


class Min(Extremum):
    output_name = "min_value"

    @classmethod
    def _bound_calculator(cls, arg1: float, arg2: float) -> float:
        return min(arg1, arg2)

    @classmethod
    def preferred_arg(
        cls, arg1: RegisterOrConst, arg2: RegisterOrConst
    ) -> RegisterOrConst:
        min1, min2 = min(argument_utils.bounds(arg1)), min(argument_utils.bounds(arg2))
        if min1 < min2:
            return arg1
        if min2 < min1:
            return arg2
        return cls._less_qubits_arg(arg1, arg2)


class Max(Extremum):
    output_name = "max_value"

    @classmethod
    def _bound_calculator(cls, arg1: float, arg2: float) -> float:
        return max(arg1, arg2)

    @classmethod
    def preferred_arg(
        cls, arg1: RegisterOrConst, arg2: RegisterOrConst
    ) -> RegisterOrConst:
        max1, max2 = max(argument_utils.bounds(arg1)), max(argument_utils.bounds(arg2))
        if max1 > max2:
            return arg1
        if max2 > max1:
            return arg2
        return cls._less_qubits_arg(arg1, arg2)
