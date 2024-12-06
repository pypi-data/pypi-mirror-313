import pydantic

from classiq.interface.generator.arith.register_user_input import RegisterArithmeticInfo
from classiq.interface.generator.function_params import FunctionParams
from classiq.interface.generator.grover_operator import GroverOperator

ESTIMATED_AMPLITUDE_OUTPUT_NAME: str = "ESTIMATED_AMPLITUDE_OUTPUT"


class AmplitudeEstimation(FunctionParams):
    """
    Creates a quantum circuit for amplitude estimation
    Provide the state preparation and oracle within the GroverOperator parameter
    Choose estimation accuracy with the estimation_register_size parameter
    """

    grover_operator: GroverOperator = pydantic.Field(
        description="The Grover Operator used in the algorithm. "
        "Composed of the oracle and the state preparation operator."
    )

    estimation_register_size: pydantic.PositiveInt = pydantic.Field(
        description="The number of qubits used to estimate the amplitude. "
        "Bigger register provides a better estimate of the good states' amplitude."
    )

    def _create_ios(self) -> None:
        self._inputs = dict()
        self._outputs = {
            ESTIMATED_AMPLITUDE_OUTPUT_NAME: RegisterArithmeticInfo(
                size=self.estimation_register_size
            ),
            **self.grover_operator.outputs,
        }
