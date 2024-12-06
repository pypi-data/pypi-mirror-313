import json
from functools import cached_property
from types import TracebackType
from typing import Any, Callable, Optional, Union, cast

import numpy as np

from classiq.interface.chemistry.operator import PauliOperator, pauli_integers_to_str
from classiq.interface.exceptions import ClassiqValueError
from classiq.interface.execution.primitives import EstimateInput, PrimitivesInput
from classiq.interface.executor.execution_preferences import ExecutionPreferences
from classiq.interface.executor.result import (
    EstimationResult,
    ExecutionDetails,
    ParsedState,
)
from classiq.interface.generator.functions.qmod_python_interface import QmodPyStruct
from classiq.interface.generator.quantum_program import QuantumProgram

from classiq._internals import async_utils
from classiq._internals.api_wrapper import ApiWrapper
from classiq._internals.client import client
from classiq.applications.combinatorial_helpers.pauli_helpers.pauli_utils import (
    _pauli_dict_to_pauli_terms,
    _pauli_terms_to_qmod,
)
from classiq.execution.jobs import ExecutionJob
from classiq.qmod.builtins import PauliTerm
from classiq.qmod.builtins.classical_execution_primitives import (
    CARRAY_SEPARATOR,
    ExecutionParams,
)
from classiq.synthesis import SerializedQuantumProgram

Hamiltonian = Union[list[QmodPyStruct], list[PauliTerm]]
Program = Union[SerializedQuantumProgram, QuantumProgram]
ParsedExecutionParams = dict[str, Union[float, int]]
ExecutionParameters = Optional[Union[ExecutionParams, list[ExecutionParams]]]
ParsedExecutionParameters = Optional[
    Union[ParsedExecutionParams, list[ParsedExecutionParams]]
]


SAVE_RESULT = "\nsave({'result': result})\n"


class SupportedPrimitives:
    SAMPLE = "sample"
    BATCH_SAMPLE = "batch_sample"
    ESTIMATE = "estimate"
    BATCH_ESTIMATE = "batch_estimate"


def _deserialize_program(program: Program) -> QuantumProgram:
    return (
        program
        if isinstance(program, QuantumProgram)
        else QuantumProgram.model_validate(json.loads(program))
    )


def hamiltonian_to_pauli_terms(hamiltonian: Hamiltonian) -> list[PauliTerm]:
    if isinstance(hamiltonian[0], PauliTerm):
        return cast(list[PauliTerm], hamiltonian)
    else:
        return _pauli_dict_to_pauli_terms(cast(list[QmodPyStruct], hamiltonian))


def to_hamiltonian_str(hamiltonian: Hamiltonian) -> str:
    return _pauli_terms_to_qmod(hamiltonian_to_pauli_terms(hamiltonian))


def _hamiltonian_to_pauli_operator(hamiltonian: Hamiltonian) -> PauliOperator:
    pauli_list = [
        (
            pauli_integers_to_str(elem.pauli),  # type: ignore[arg-type]
            elem.coefficient,
        )
        for elem in hamiltonian_to_pauli_terms(hamiltonian)
    ]
    return PauliOperator(pauli_list=pauli_list)


def serialize(
    item: Union[float, int, tuple[int, ...], tuple[float, ...]]
) -> Union[str, list]:
    if isinstance(item, tuple):
        return list(item)
    return str(item)


def parse_params(params: ExecutionParams) -> ParsedExecutionParams:
    result = {}
    for key, values in params.items():
        if isinstance(values, list):
            for index, value in enumerate(values):
                new_key = f"{key}{CARRAY_SEPARATOR}{index}"
                result[new_key] = value
        elif isinstance(values, (int, float)):
            result[key] = values
        else:
            raise TypeError("Parameters were provided in un-supported format")
    return result


def format_parameters(execution_params: ExecutionParameters) -> str:
    parsed_parameters: ParsedExecutionParameters = None
    if execution_params is None:
        return ""
    if isinstance(execution_params, dict):
        parsed_parameters = parse_params(execution_params)

    elif isinstance(execution_params, list):
        parsed_parameters = [
            parse_params(ep) if isinstance(ep, dict) else ep for ep in execution_params
        ]

    execution_params = cast(ExecutionParams, parsed_parameters)
    return json.dumps(execution_params, default=serialize, indent=2)


def create_estimate_execution_code(operation: str, **kwargs: Any) -> str:
    hamiltonian = kwargs.get("hamiltonian", "")
    parameters = kwargs.get("parameters", "")
    return f"\nresult = {operation}([{hamiltonian}], {parameters})" + SAVE_RESULT


def create_sample_execution_code(operation: str, **kwargs: Any) -> str:
    parameters = kwargs.get("parameters", "")
    return f"\nresult = {operation}({parameters})" + SAVE_RESULT


operation_handlers: dict[str, Callable[[str], str]] = {
    "estimate": create_estimate_execution_code,
    "batch_estimate": create_estimate_execution_code,
    "sample": create_sample_execution_code,
    "batch_sample": create_sample_execution_code,
}


def generate_code_snippet(operation: str, **kwargs: Any) -> str:
    handler = operation_handlers.get(operation)
    if handler:
        return handler(operation, **kwargs)
    raise ClassiqValueError(f"Unsupported operation type: {operation}")


class ExecutionSession:
    """
    A session for executing a quantum program.
    `ExecutionSession` allows to execute the quantum program with different parameters and operations without the need to re-synthesize the model.
    The session must be closed in order to ensure resources are properly cleaned up. It's recommended to use `ExecutionSession` as a context manager for this purpose. Alternatively, you can directly use the `close` method.

    Attributes:
        quantum_program (Union[SerializedQuantumProgram, QuantumProgram]): The quantum program to execute.
        execution_preferences (Optional[ExecutionPreferences]): Execution preferences for the Quantum Program.
    """

    def __init__(
        self,
        quantum_program: Program,
        execution_preferences: Optional[ExecutionPreferences] = None,
    ):
        self.program: QuantumProgram = _deserialize_program(quantum_program)
        self.update_execution_preferences(execution_preferences)
        # When the primitives are called, we always override the
        # classical_execution_code, and we don't want the conversion route to fail
        # because cmain is expected in some cases
        self.program.model.classical_execution_code = "dummy"

        self._async_client = client().async_client()

    def __enter__(self) -> "ExecutionSession":
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.close()

    def close(self) -> None:
        """
        Close the session and clean up its resources.
        """
        async_utils.run(self._async_client.aclose())

    @cached_property
    def _execution_input(self) -> dict:
        return async_utils.run(
            ApiWrapper.call_convert_quantum_program(self.program, self._async_client)
        )

    def _execute(
        self, classical_execution_code: str, primitives_input: PrimitivesInput
    ) -> ExecutionJob:
        execution_input = self._execution_input.copy()
        execution_input["classical_execution_code"] = classical_execution_code
        # The use of `model_dump_json` is necessary for complex numbers serialization
        execution_input["primitives_input"] = json.loads(
            primitives_input.model_dump_json()
        )
        result = async_utils.run(
            ApiWrapper.call_execute_execution_input(execution_input, self._async_client)
        )
        return ExecutionJob(details=result)

    def update_execution_preferences(
        self, execution_preferences: Optional[ExecutionPreferences]
    ) -> None:
        """
        Update the execution preferences for the session.

        Args:
            execution_preferences: The execution preferences to update.

        Returns:
            None
        """
        if execution_preferences is not None:
            self.program.model.execution_preferences = execution_preferences

    def sample(self, parameters: Optional[ExecutionParams] = None) -> ExecutionDetails:
        """
        Samples the quantum program with the given parameters, if any.

        Args:
            parameters: The values to set for the parameters of the quantum program when sampling. Each key should be the name of a parameter in the quantum program (parameters of the main function), and the value should be the value to set for that parameter.

        Returns:
            The result of the sampling.
        """
        job = self.submit_sample(parameters=parameters)
        return job.get_sample_result(_http_client=self._async_client)

    def submit_sample(
        self, parameters: Optional[ExecutionParams] = None
    ) -> ExecutionJob:
        """
        Initiates an execution job with the `sample` primitive.

        This is a non-blocking version of `sample`: it gets the same parameters and initiates the same execution job, but instead
        of waiting for the result, it returns the job object immediately.

        Args:
            parameters: The values to set for the parameters of the quantum program when sampling. Each key should be the name of a parameter in the quantum program (parameters of the main function), and the value should be the value to set for that parameter.

        Returns:
            The execution job.
        """
        classical_execution_code = generate_code_snippet(
            SupportedPrimitives.SAMPLE, parameters=format_parameters(parameters)
        )
        execution_primitives_input = PrimitivesInput(
            sample=[parse_params(parameters)] if parameters is not None else [{}]
        )
        return self._execute(classical_execution_code, execution_primitives_input)

    def batch_sample(self, parameters: list[ExecutionParams]) -> list[ExecutionDetails]:
        """
        Samples the quantum program multiple times with the given parameters for each iteration. The number of samples is determined by the length of the parameters list.

        Args:
            parameters: A list of the parameters for each iteration. Each item is a dictionary where each key should be the name of a parameter in the quantum program (parameters of the main function), and the value should be the value to set for that parameter.

        Returns:
            List[ExecutionDetails]: The results of all the sampling iterations.
        """
        job = self.submit_batch_sample(parameters=parameters)
        return job.get_batch_sample_result(_http_client=self._async_client)

    def submit_batch_sample(self, parameters: list[ExecutionParams]) -> ExecutionJob:
        """
        Initiates an execution job with the `batch_sample` primitive.

        This is a non-blocking version of `batch_sample`: it gets the same parameters and initiates the same execution job, but instead
        of waiting for the result, it returns the job object immediately.

        Args:
            parameters: A list of the parameters for each iteration. Each item is a dictionary where each key should be the name of a parameter in the quantum program (parameters of the main function), and the value should be the value to set for that parameter.

        Returns:
            The execution job.
        """
        classical_execution_code = generate_code_snippet(
            SupportedPrimitives.BATCH_SAMPLE, parameters=format_parameters(parameters)
        )
        execution_primitives_input = PrimitivesInput(
            sample=[parse_params(params) for params in parameters]
        )
        return self._execute(classical_execution_code, execution_primitives_input)

    def estimate(
        self, hamiltonian: Hamiltonian, parameters: Optional[ExecutionParams] = None
    ) -> EstimationResult:
        """
        Estimates the expectation value of the given Hamiltonian using the quantum program.

        Args:
            hamiltonian: The Hamiltonian to estimate the expectation value of.
            parameters: The values to set for the parameters of the quantum program when estimating.  Each key should be the name of a parameter in the quantum program (parameters of the main function), and the value should be the value to set for that parameter.

        Returns:
            EstimationResult: The result of the estimation.
        """
        job = self.submit_estimate(hamiltonian=hamiltonian, parameters=parameters)
        return job.get_estimate_result(_http_client=self._async_client)

    def submit_estimate(
        self, hamiltonian: Hamiltonian, parameters: Optional[ExecutionParams] = None
    ) -> ExecutionJob:
        """
        Initiates an execution job with the `estimate` primitive.

        This is a non-blocking version of `estimate`: it gets the same parameters and initiates the same execution job, but instead
        of waiting for the result, it returns the job object immediately.

        Args:
            hamiltonian: The Hamiltonian to estimate the expectation value of.
            parameters: The values to set for the parameters of the quantum program when estimating.  Each key should be the name of a parameter in the quantum program (parameters of the main function), and the value should be the value to set for that parameter.

        Returns:
            The execution job.
        """
        classical_execution_code = generate_code_snippet(
            SupportedPrimitives.ESTIMATE,
            parameters=format_parameters(parameters),
            hamiltonian=to_hamiltonian_str(hamiltonian),
        )
        execution_primitives_input = PrimitivesInput(
            estimate=EstimateInput(
                hamiltonian=_hamiltonian_to_pauli_operator(hamiltonian),
                parameters=(
                    [parse_params(parameters)] if parameters is not None else [{}]
                ),
            )
        )
        return self._execute(classical_execution_code, execution_primitives_input)

    def batch_estimate(
        self, hamiltonian: Hamiltonian, parameters: list[ExecutionParams]
    ) -> list[EstimationResult]:
        """
        Estimates the expectation value of the given Hamiltonian multiple times using the quantum program, with the given parameters for each iteration. The number of estimations is determined by the length of the parameters list.

        Args:
            hamiltonian: The Hamiltonian to estimate the expectation value of.
            parameters: A list of the parameters for each iteration. Each item is a dictionary where each key should be the name of a parameter in the quantum program (parameters of the main function), and the value should be the value to set for that parameter.

        Returns:
            List[EstimationResult]: The results of all the estimation iterations.
        """
        job = self.submit_batch_estimate(hamiltonian=hamiltonian, parameters=parameters)
        return job.get_batch_estimate_result(_http_client=self._async_client)

    def submit_batch_estimate(
        self, hamiltonian: Hamiltonian, parameters: list[ExecutionParams]
    ) -> ExecutionJob:
        """
        Initiates an execution job with the `batch_estimate` primitive.

        This is a non-blocking version of `batch_estimate`: it gets the same parameters and initiates the same execution job, but instead
        of waiting for the result, it returns the job object immediately.

        Args:
            hamiltonian: The Hamiltonian to estimate the expectation value of.
            parameters: A list of the parameters for each iteration. Each item is a dictionary where each key should be the name of a parameter in the quantum program (parameters of the main function), and the value should be the value to set for that parameter.

        Returns:
            The execution job.
        """
        classical_execution_code = generate_code_snippet(
            SupportedPrimitives.BATCH_ESTIMATE,
            parameters=format_parameters(parameters),
            hamiltonian=to_hamiltonian_str(hamiltonian),
        )
        execution_primitives_input = PrimitivesInput(
            estimate=EstimateInput(
                hamiltonian=_hamiltonian_to_pauli_operator(hamiltonian),
                parameters=[parse_params(params) for params in parameters],
            )
        )
        return self._execute(classical_execution_code, execution_primitives_input)

    def estimate_cost(
        self,
        cost_func: Callable[[ParsedState], float],
        parameters: Optional[ExecutionParams] = None,
        quantile: float = 1.0,
    ) -> float:
        """
        Estimates circuit cost using a classical cost function.

        Args:
            cost_func: classical circuit sample cost function
            parameters: execution parameters sent to 'sample'
            quantile: drop cost values outside the specified quantile

        Returns:
            cost estimation

        See Also:
            sample
        """
        if quantile < 0 or quantile > 1:
            raise ClassiqValueError("'quantile' must be between 0 and 1")
        res = self.sample(parameters)

        counts = np.array(res.parsed_counts)
        costs = np.vectorize(lambda sample: cost_func(sample.state))(counts)
        shots = np.vectorize(lambda sample: sample.shots)(counts)

        if quantile == 1:
            return float(np.average(costs, weights=shots))
        costs = np.repeat(costs, shots)
        sort_idx = costs.argsort()
        sort_idx = sort_idx[: int(quantile * len(costs))]
        costs = costs[sort_idx]
        if costs.size == 0:
            return np.nan
        return float(np.average(costs))
