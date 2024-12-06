import math
from collections.abc import Sequence
from typing import Any, Generic, TypeVar

import pydantic
from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic_core.core_schema import ValidationInfo

from classiq.interface.exceptions import ClassiqError
from classiq.interface.generator.arith.register_user_input import RegisterArithmeticInfo
from classiq.interface.generator.function_params import FunctionParams
from classiq.interface.helpers.hashable_pydantic_base_model import (
    HashablePydanticBaseModel,
)

STATE_NAME: str = "state"
TARGET_NAME: str = "target"
_REL_TOLERANCE: float = 0.01

Breakpoint = TypeVar("Breakpoint")


class AffineMap(HashablePydanticBaseModel):
    slope: float = Field(default=1.0)
    offset: float = Field(default=0.0)

    def evaluate(self, x: float) -> float:
        return self.offset + self.slope * x

    def image_bounds(self, domain_bounds: tuple[float, float]) -> tuple[float, float]:
        return self.evaluate(domain_bounds[0]), self.evaluate(domain_bounds[1])

    model_config = ConfigDict(frozen=True)


class PiecewiseLinearAmplitudeLoadingABC(
    FunctionParams, BaseModel, Generic[Breakpoint]
):
    num_qubits: int = Field()
    breakpoints: Sequence[int] = Field()
    affine_maps: Sequence[AffineMap] = Field()

    def _create_ios(self) -> None:
        self._inputs = {
            STATE_NAME: RegisterArithmeticInfo(size=self.num_qubits),
            TARGET_NAME: RegisterArithmeticInfo(size=1),
        }
        self._outputs = {**self._inputs}

    @property
    def _max_index(self) -> int:
        return 2**self.num_qubits - 1

    def _get_image_bounds(self) -> tuple[float, float]:
        piece_bounds: Sequence[tuple[float, float]] = [
            affine_map.image_bounds((self.breakpoints[idx], self.breakpoints[idx + 1]))
            for idx, affine_map in enumerate(self.affine_maps)
        ]
        bottom = min(min(piece) for piece in piece_bounds)
        top = max(max(piece) for piece in piece_bounds)
        return bottom, top

    @field_validator("breakpoints", mode="before")
    @classmethod
    def _validate_breakpoints(cls, breakpoints: Sequence[int]) -> Sequence[int]:
        return cls.validate_breakpoints(breakpoints)

    @classmethod
    def validate_breakpoints(cls, breakpoints: Sequence[int]) -> Sequence[int]:
        assert len(breakpoints) == len(
            set(breakpoints)
        ), "Repeated breakpoints encountered"
        assert list(breakpoints) == sorted(breakpoints), "Breakpoints not sorted"
        return list(map(int, breakpoints))

    @pydantic.model_validator(mode="before")
    @classmethod
    def _validate_lengths(cls, values: Any) -> dict[str, Any]:
        breakpoints = values.get("breakpoints", list())
        affine_maps = values.get("affine_maps", list())
        num_qubits = values.get("num_qubits", int)
        if isinstance(values, dict):
            breakpoints = values.get("breakpoints", list())
            affine_maps = values.get("affine_maps", list())
            num_qubits = values.get("num_qubits", int)
        elif isinstance(values, PiecewiseLinearAmplitudeLoadingABC):
            breakpoints = values.breakpoints
            affine_maps = values.affine_maps
            num_qubits = values.num_qubits
            values = values.__dict__

        assert len(breakpoints) - 1 == len(
            affine_maps
        ), "Size mismatch between the number of slopes and breakpoints. The number of breakpoints should be the number of slopes + 1"
        assert (
            len(breakpoints) <= num_qubits**2
        ), "Number of breakpoints must be equal to or smaller than num_qubits**2"
        return values


class PiecewiseLinearRotationAmplitudeLoading(PiecewiseLinearAmplitudeLoadingABC[int]):
    pass

    @field_validator("breakpoints")
    @classmethod
    def _validate_breakpoints_field(
        cls, breakpoints: Sequence[int], info: ValidationInfo
    ) -> Sequence[int]:
        num_qubits = info.data.get("num_qubits")
        assert isinstance(num_qubits, int), "Must have an integer number of qubits"
        assert min(breakpoints) == 0, "First breakpoint must be 0"
        assert (
            max(breakpoints) == 2**num_qubits - 1
        ), f"Last breakpoint must be {2**num_qubits - 1}"
        return PiecewiseLinearAmplitudeLoadingABC.validate_breakpoints(
            breakpoints=breakpoints
        )


class PiecewiseLinearAmplitudeLoading(PiecewiseLinearAmplitudeLoadingABC[float]):
    rescaling_factor: float = Field(default=0.25 * math.pi)

    def rescaled(self) -> PiecewiseLinearRotationAmplitudeLoading:
        c, d = self._get_image_bounds()
        if math.isclose(c, d):
            raise ClassiqError("Cannot rescale flat linear maps")

        a, b = self.breakpoints[0], self.breakpoints[-1]

        normalized_breakpoints: list[int] = [
            round(self._max_index * (point - a) / (b - a)) for point in self.breakpoints
        ]

        normalized_affine_maps: list[AffineMap] = list()
        for affine_map in self.affine_maps:
            normalized_slope = (
                2 * affine_map.slope * self.rescaling_factor * (b - a)
            ) / (self._max_index * (d - c))
            normalized_offset = (
                (2 * self.rescaling_factor * (affine_map.evaluate(a) - c)) / (d - c)
                - self.rescaling_factor
                + math.pi / 4
            )
            normalized_affine_maps.append(
                AffineMap(slope=normalized_slope, offset=normalized_offset)
            )
        return PiecewiseLinearRotationAmplitudeLoading(
            num_qubits=self.num_qubits,
            breakpoints=normalized_breakpoints,
            affine_maps=normalized_affine_maps,
        )

    @staticmethod
    def _descaled_value(
        *, scaled_expectation_value: float, rescaling_factor: float
    ) -> float:
        return 0.5 * ((scaled_expectation_value - 0.5) / rescaling_factor + 1)

    def compute_expectation_value(self, scaled_expectation_value: float) -> float:
        bounds = self._get_image_bounds()
        image_bottom, image_top = min(bounds), max(bounds)
        return image_bottom + (image_top - image_bottom) * self._descaled_value(
            rescaling_factor=self.rescaling_factor,
            scaled_expectation_value=scaled_expectation_value,
        )
