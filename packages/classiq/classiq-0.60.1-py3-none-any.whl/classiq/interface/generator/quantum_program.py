import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Union

import pydantic
from typing_extensions import TypeAlias

from classiq.interface.exceptions import (
    ClassiqMissingOutputFormatError,
    ClassiqStateInitializationError,
)
from classiq.interface.execution.primitives import PrimitivesInput
from classiq.interface.executor import quantum_code
from classiq.interface.executor.quantum_instruction_set import QuantumInstructionSet
from classiq.interface.executor.register_initialization import RegisterInitialization
from classiq.interface.generator.circuit_code.circuit_code import CircuitCodeInterface
from classiq.interface.generator.circuit_code.types_and_constants import (
    DEFAULT_INSTRUCTION_SET,
    INSTRUCTION_SET_TO_FORMAT,
    VENDOR_TO_INSTRUCTION_SET,
    CodeAndSyntax,
)
from classiq.interface.generator.generated_circuit_data import (
    FunctionDebugInfoInterface,
    GeneratedCircuitData,
)
from classiq.interface.generator.hardware.hardware_data import SynthesisHardwareData
from classiq.interface.generator.model.model import ExecutionModel
from classiq.interface.generator.synthesis_metadata.synthesis_duration import (
    SynthesisStepDurations,
)
from classiq.interface.helpers.versioned_model import VersionedModel
from classiq.interface.ide.visual_model import CircuitMetrics

RegisterName: TypeAlias = str
InitialConditions: TypeAlias = dict[RegisterName, int]


class TranspiledCircuitData(CircuitCodeInterface):
    depth: int
    count_ops: dict[str, int]
    logical_to_physical_input_qubit_map: list[int]
    logical_to_physical_output_qubit_map: list[int]

    def get_circuit_metrics(self) -> CircuitMetrics:
        return CircuitMetrics(depth=self.depth, count_ops=self.count_ops)


def get_uuid_as_str() -> str:
    return str(uuid.uuid4())


def _get_formatted_utc_current_time() -> str:
    # The purpose of this method is to replicate the behavior of
    # datetime.utcnow().isoformat(), since `utcnow` is now deprecated
    return datetime.now(timezone.utc).isoformat().split("+")[0]


class QuantumProgram(VersionedModel, CircuitCodeInterface):
    hardware_data: SynthesisHardwareData
    initial_values: Optional[InitialConditions] = pydantic.Field(default=None)
    data: GeneratedCircuitData
    model: ExecutionModel
    transpiled_circuit: Optional[TranspiledCircuitData] = pydantic.Field(default=None)
    creation_time: str = pydantic.Field(default_factory=_get_formatted_utc_current_time)
    synthesis_duration: Optional[SynthesisStepDurations] = pydantic.Field(default=None)
    debug_info: Optional[list[FunctionDebugInfoInterface]] = pydantic.Field(
        default=None
    )
    program_id: str = pydantic.Field(default_factory=get_uuid_as_str)
    execution_primitives_input: Optional[PrimitivesInput] = pydantic.Field(default=None)

    def _hardware_agnostic_program_code(self) -> CodeAndSyntax:
        circuit_code = self.program_circuit.get_code_by_priority()
        if circuit_code is not None:
            return circuit_code

        raise ClassiqMissingOutputFormatError(
            missing_formats=list(INSTRUCTION_SET_TO_FORMAT.values())
        )

    def _default_program_code(self) -> CodeAndSyntax:
        if self.hardware_data.backend_data is None:
            return self._hardware_agnostic_program_code()

        backend_provider = self.hardware_data.backend_data.hw_provider
        instruction_set: QuantumInstructionSet = VENDOR_TO_INSTRUCTION_SET.get(
            backend_provider, DEFAULT_INSTRUCTION_SET
        )
        return self.program_circuit.get_code(instruction_set), instruction_set

    def to_base_program(self) -> quantum_code.QuantumBaseCode:
        code, syntax = self._default_program_code()
        return quantum_code.QuantumBaseCode(code=code, syntax=syntax)

    def to_program(
        self,
        initial_values: Optional[InitialConditions] = None,
        instruction_set: Optional[QuantumInstructionSet] = None,
    ) -> quantum_code.QuantumCode:
        initial_values = initial_values or self.initial_values

        if instruction_set is not None:
            code, syntax = (
                self.program_circuit.get_code(instruction_set),
                instruction_set,
            )
        else:
            code, syntax = self._default_program_code()

        if initial_values is not None:
            registers_initialization = self.get_registers_initialization(
                initial_values=initial_values
            )
        else:
            registers_initialization = None
        return quantum_code.QuantumCode(
            code=code,
            syntax=syntax,
            output_qubits_map=self.data.qubit_mapping.physical_outputs,
            registers_initialization=registers_initialization,
            synthesis_execution_data=self.data.execution_data,
        )

    def _get_initialization_qubits(self, name: str) -> tuple[int, ...]:
        qubits = self.data.qubit_mapping.logical_inputs.get(name)
        if qubits is None:
            raise ClassiqStateInitializationError(
                f"Cannot initialize register {name}, it does not appear in circuit inputs"
            )
        return qubits

    def get_registers_initialization(
        self, initial_values: InitialConditions
    ) -> dict[RegisterName, RegisterInitialization]:
        return {
            name: RegisterInitialization(
                name=name,
                qubits=list(self._get_initialization_qubits(name)),
                initial_condition=init_value,
            )
            for name, init_value in initial_values.items()
        }

    def save_results(self, filename: Optional[Union[str, Path]] = None) -> None:
        """
        Saves quantum program results as json into a file.
            Parameters:
                filename (Union[str, Path]): Optional, path + filename of file.
                                             If filename supplied add `.json` suffix.
            Returns:
                  None
        """
        if filename is None:
            filename = f"synthesised_circuit_{self.creation_time}.json"

        with open(filename, "w") as file:
            file.write(self.model_dump_json(indent=4))

    @classmethod
    def from_qprog(cls, qprog: str) -> "QuantumProgram":
        """
        Creates a `QuantumProgram` instance from a raw quantum program string.

        Args:
            qprog: The raw quantum program in string format.

        Returns:
            QuantumProgram: The `QuantumProgram` instance.
        """
        return cls.model_validate_json(qprog)

    @property
    def _can_use_transpiled_code(self) -> bool:
        return self.data.execution_data is None

    @property
    def program_circuit(self) -> CircuitCodeInterface:
        return (
            self.transpiled_circuit
            if self.transpiled_circuit and self._can_use_transpiled_code
            else self
        )
