from collections import Counter
from typing import Any, Optional

import pydantic
from pydantic import ConfigDict

from classiq.interface.enum_utils import StrEnum
from classiq.interface.generator.generated_circuit_data import (
    OperationLevel,
    OperationParameter,
)
from classiq.interface.generator.hardware.hardware_data import SynthesisHardwareData
from classiq.interface.helpers.versioned_model import VersionedModel


class OperationType(StrEnum):
    REGULAR = "REGULAR"
    ALLOCATE = "ALLOCATE"
    FREE = "FREE"
    BIND = "BIND"
    ATOMIC = "ATOMIC"


class OperationData(pydantic.BaseModel):
    approximated_depth: Optional[int] = None
    width: int
    gate_count: Counter[str] = pydantic.Field(default_factory=dict)


class CircuitMetrics(pydantic.BaseModel):
    depth: int
    count_ops: dict[str, int]


class ProgramData(pydantic.BaseModel):
    hardware_data: SynthesisHardwareData
    circuit_metrics: CircuitMetrics


class OperationLink(pydantic.BaseModel):
    label: str
    inner_label: Optional[str] = None
    qubits: tuple[int, ...]
    type: str

    model_config = ConfigDict(frozen=True)

    def __hash__(self) -> int:
        return hash((type(self), self.label, self.qubits, self.type))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, OperationLink):
            return False
        return hash(self) == hash(other)


class OperationLinks(pydantic.BaseModel):
    inputs: list[OperationLink]
    outputs: list[OperationLink]

    @property
    def input_width(self) -> int:
        return sum(len(link.qubits) for link in self.inputs)

    @property
    def output_width(self) -> int:
        return sum(len(link.qubits) for link in self.outputs)


class AtomicGate(StrEnum):
    UNKNOWN = ""
    H = "H"
    X = "X"
    Y = "Y"
    Z = "Z"
    I = "I"  # noqa: E741
    S = "S"
    T = "T"
    SDG = "SDG"
    TDG = "TDG"
    PHASE = "PHASE"
    RX = "RX"
    RY = "RY"
    RZ = "RZ"
    R = "R"
    RXX = "RXX"
    RYY = "RYY"
    RZZ = "RZZ"
    CH = "CH"
    CX = "CX"
    CY = "CY"
    CZ = "CZ"
    CRX = "CRX"
    CRY = "CRY"
    CRZ = "CRZ"
    CPHASE = "CPHASE"
    SWAP = "SWAP"
    IDENTITY = "IDENTITY"
    U = "U"

    @property
    def is_control_gate(self) -> bool:
        return self.startswith("C")


class Operation(pydantic.BaseModel):
    name: str
    qasm_name: str = pydantic.Field(default="")
    details: str = pydantic.Field(default="")
    children: list["Operation"]
    operation_data: Optional[OperationData] = None
    operation_links: OperationLinks
    control_qubits: tuple[int, ...] = pydantic.Field(default_factory=tuple)
    auxiliary_qubits: tuple[int, ...]
    target_qubits: tuple[int, ...]
    parameters: list[OperationParameter] = pydantic.Field(default_factory=list)
    operation_level: OperationLevel
    operation_type: OperationType = pydantic.Field(
        description="Identifies unique operations that are visualized differently"
    )
    gate: AtomicGate = pydantic.Field(
        default=AtomicGate.UNKNOWN, description="Gate type"
    )
    is_daggered: bool = pydantic.Field(default=False)


class ProgramVisualModel(VersionedModel):
    main_operation: Operation
    program_data: ProgramData
