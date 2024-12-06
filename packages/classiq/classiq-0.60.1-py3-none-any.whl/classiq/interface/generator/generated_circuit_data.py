import logging
from typing import Any, Literal, Optional, Union

import pydantic
from pydantic import ConfigDict
from typing_extensions import TypeAlias

from classiq.interface.enum_utils import StrEnum
from classiq.interface.generator.control_state import ControlState
from classiq.interface.generator.register_role import RegisterRole
from classiq.interface.generator.synthesis_metadata.synthesis_execution_data import (
    ExecutionData,
)

_logger = logging.getLogger(__name__)
ParameterName = str
IOQubitMapping: TypeAlias = dict[str, tuple[int, ...]]

CLASSIQ_HIERARCHY_SEPARATOR: Literal["."] = "."

VISUALIZATION_HIDE_LIST = [
    "apply_to_all",
    "repeat",
    "control",
    "mcx",
    "iteration",
    "stmt_block",
]


def last_name_in_call_hierarchy(name: str) -> str:
    return name.split(CLASSIQ_HIERARCHY_SEPARATOR)[-1]


class QubitMapping(pydantic.BaseModel):
    logical_inputs: IOQubitMapping = pydantic.Field(default_factory=dict)
    logical_outputs: IOQubitMapping = pydantic.Field(default_factory=dict)
    physical_inputs: IOQubitMapping = pydantic.Field(default_factory=dict)
    physical_outputs: IOQubitMapping = pydantic.Field(default_factory=dict)


class GeneratedRegister(pydantic.BaseModel):
    name: str
    role: RegisterRole
    qubit_indexes_relative: list[int]
    qubit_indexes_absolute: list[int]

    def __len__(self) -> int:
        return self.qubit_indexes_relative.__len__()

    @property
    def width(self) -> int:
        return len(self)


class GeneratedFunction(pydantic.BaseModel):
    name: str
    control_states: list[ControlState]
    registers: list[GeneratedRegister] = list()
    depth: Optional[int] = pydantic.Field(default=None)
    width: Optional[int] = pydantic.Field(default=None)
    dangling_inputs: dict[str, GeneratedRegister] = dict()
    dangling_outputs: dict[str, GeneratedRegister] = dict()

    def __getitem__(self, key: Union[int, str]) -> GeneratedRegister:
        if isinstance(key, int):
            return self.registers[key]
        if isinstance(key, str):
            for register in self.registers:
                if key == register.name:
                    return register
        raise KeyError(key)

    def get(self, key: Union[int, str]) -> Optional[GeneratedRegister]:
        try:
            return self.__getitem__(key)
        except KeyError:
            return None

    @property
    def should_appear_in_visualization(self) -> bool:
        return all(
            hide_regex not in last_name_in_call_hierarchy(self.name.lower())
            for hide_regex in VISUALIZATION_HIDE_LIST
        )


class GeneratedCircuitData(pydantic.BaseModel):
    width: int
    circuit_parameters: list[ParameterName] = pydantic.Field(default_factory=list)
    qubit_mapping: QubitMapping = pydantic.Field(default_factory=QubitMapping)
    execution_data: Optional[ExecutionData] = pydantic.Field(default=None)

    @classmethod
    def from_empty_logic_flow(cls) -> "GeneratedCircuitData":
        return cls(width=0)


class OperationLevel(StrEnum):
    QMOD_FUNCTION_CALL = "QMOD_CALL"
    QMOD_STATEMENT = "QMOD_STATEMENT"
    ENGINE_FUNCTION_CALL = "ENGINE_CALL"
    UNKNOWN = "UNKNOWN"


class OperationParameter(pydantic.BaseModel):
    label: str
    value: Optional[str] = None


class FunctionDebugInfoInterface(pydantic.BaseModel):
    generated_function: Optional[GeneratedFunction] = pydantic.Field(default=None)
    children: list["FunctionDebugInfoInterface"]
    relative_qubits: tuple[int, ...]
    absolute_qubits: Optional[tuple[int, ...]] = pydantic.Field(default=None)
    is_basis_gate: Optional[bool] = pydantic.Field(default=None)
    is_inverse: bool = pydantic.Field(default=False)
    is_allocate_or_free: bool = pydantic.Field(default=False)
    level: OperationLevel = pydantic.Field(default=OperationLevel.UNKNOWN)
    parameters: list[OperationParameter] = list()
    port_to_passed_variable_map: dict[str, str] = pydantic.Field(default={})

    model_config = ConfigDict(extra="allow")
    # Temporary field to store the override debug info for parallel old/new visualization
    override_debug_info: Optional["FunctionDebugInfoInterface"] = None

    @property
    def name(self) -> str:
        if self.generated_function is None:
            return ""
        return self.generated_function.name

    @property
    def registers(self) -> list[GeneratedRegister]:
        if self.generated_function is None:
            return list()
        return self.generated_function.registers

    @property
    def is_controlled(self) -> bool:
        if self.generated_function is None:
            return False
        return len(self.generated_function.control_states) > 0

    @property
    def control_states(self) -> list[ControlState]:
        if self.generated_function is None:
            return list()
        return self.generated_function.control_states

    @staticmethod
    def create_parameters_from_dict(
        parameters: dict[str, str]
    ) -> list[OperationParameter]:
        return [
            OperationParameter(label=key, value=value)
            for key, value in parameters.items()
        ]

    def update(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def propagate_absolute_qubits(self) -> None:
        if self.absolute_qubits is None:
            return

        for register in self.registers:
            register.qubit_indexes_absolute = list(
                _get_absolute_from_relative(
                    self.absolute_qubits, tuple(register.qubit_indexes_relative)
                )
            )

        for child in self.children:
            child.absolute_qubits = _get_absolute_from_relative(
                self.absolute_qubits, child.relative_qubits
            )
            child.propagate_absolute_qubits()

    def inverse(self) -> None:
        self.is_inverse = not self.is_inverse
        for child in self.children:
            child.inverse()
        self.children = self.children[::-1]


def _get_absolute_from_relative(
    absolute_qubits: tuple[int, ...], relative_qubits: tuple[int, ...]
) -> tuple[int, ...]:
    if max(relative_qubits) >= len(absolute_qubits):
        _logger.warning(
            "Invalid qubit computation (relative qubits: %s, absolute qubits: %s)",
            relative_qubits,
            absolute_qubits,
        )
        return tuple()
    return tuple(absolute_qubits[relative_qubit] for relative_qubit in relative_qubits)
