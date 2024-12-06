from math import floor, log
from typing import Union

from classiq.interface.exceptions import ClassiqError
from classiq.interface.finance.function_input import FinanceFunctionInput
from classiq.interface.finance.gaussian_model_input import GaussianModelInput
from classiq.interface.finance.log_normal_model_input import LogNormalModelInput
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.model.handle_binding import HandleBinding
from classiq.interface.model.model import Model, SerializedModel
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_call import QuantumFunctionCall
from classiq.interface.model.quantum_lambda_function import QuantumLambdaFunction
from classiq.interface.model.quantum_type import QuantumBitvector
from classiq.interface.model.variable_declaration_statement import (
    VariableDeclarationStatement,
)

from classiq.applications.libraries.qmci_library import QMCI_LIBRARY
from classiq.qmod.utilities import qmod_val_to_expr_str

_OUTPUT_VARIABLE_NAME = "payoff_estimation"


def construct_finance_model(
    finance_model_input: Union[LogNormalModelInput, GaussianModelInput],
    finance_function_input: FinanceFunctionInput,
    phase_port_size: int,
) -> SerializedModel:
    if isinstance(finance_model_input, LogNormalModelInput):
        finance_model = f"struct_literal(LogNormalModel, num_qubits={finance_model_input.num_qubits}, mu={finance_model_input.mu}, sigma={finance_model_input.sigma})"
        finance_function = "log_normal_finance"
        post_process_function = "log_normal_finance_post_process"
        total_num_qubits = finance_model_input.num_qubits
    elif isinstance(finance_model_input, GaussianModelInput):
        finance_model = f"struct_literal(GaussianModel, num_qubits={finance_model_input.num_qubits}, normal_max_value={finance_model_input.normal_max_value}, default_probabilities={finance_model_input.default_probabilities}, rhos={finance_model_input.rhos}, loss={finance_model_input.loss}, min_loss={finance_model_input.min_loss})"
        finance_function = "gaussian_finance"
        post_process_function = "gaussian_finance_post_process"
        total_num_qubits = (
            finance_model_input.num_qubits
            + len(finance_model_input.rhos)
            + floor(log(sum(finance_model_input.loss), 2))
            + 1
        )
    else:
        raise ClassiqError(f"Invalid model input: {finance_model_input}")

    polynomial_degree = 0
    if finance_function_input.polynomial_degree is not None:
        polynomial_degree = finance_function_input.polynomial_degree

    tail_probability = 0.0
    if finance_function_input.tail_probability is not None:
        tail_probability = finance_function_input.tail_probability

    finance_function_object = f"struct_literal(FinanceFunction, f={qmod_val_to_expr_str(finance_function_input.f)}, threshold={finance_function_input.condition.threshold}, larger={finance_function_input.condition.larger}, polynomial_degree={polynomial_degree}, use_chebyshev_polynomial_approximation={finance_function_input.use_chebyshev_polynomial_approximation}, tail_probability={tail_probability})"
    num_unitary_qubits = total_num_qubits + 1

    model = Model(
        functions=[
            *QMCI_LIBRARY,
            NativeFunctionDefinition(
                name="main",
                positional_arg_declarations=[
                    PortDeclaration(
                        name="phase_port",
                        quantum_type=QuantumBitvector(
                            length=Expression(expr=f"{phase_port_size}")
                        ),
                        direction=PortDeclarationDirection.Output,
                    ),
                ],
                body=[
                    VariableDeclarationStatement(name="unitary_port"),
                    QuantumFunctionCall(
                        function="allocate",
                        positional_args=[
                            Expression(expr=f"{num_unitary_qubits}"),
                            HandleBinding(name="unitary_port"),
                        ],
                    ),
                    QuantumFunctionCall(
                        function="allocate_num",
                        positional_args=[
                            Expression(expr=f"{phase_port_size}"),
                            Expression(expr="False"),
                            Expression(expr=f"{phase_port_size}"),
                            HandleBinding(name="phase_port"),
                        ],
                    ),
                    QuantumFunctionCall(
                        function="qmci",
                        positional_args=[
                            QuantumLambdaFunction(
                                pos_rename_params=["state", "ind"],
                                body=[
                                    QuantumFunctionCall(
                                        function=finance_function,
                                        positional_args=[
                                            Expression(expr=finance_model),
                                            Expression(expr=finance_function_object),
                                            HandleBinding(name="state"),
                                            HandleBinding(name="ind"),
                                        ],
                                    ),
                                ],
                            ),
                            HandleBinding(name="phase_port"),
                            HandleBinding(name="unitary_port"),
                        ],
                    ),
                ],
            ),
        ],
        classical_execution_code=f"""
phase_port_size = {phase_port_size}
counts = sample()
save({{"counts": counts}})
probability_estimation = qae_with_qpe_result_post_processing(
    estimation_register_size=phase_port_size,
    estimation_method=1,
    result=counts
)
save({{"probability_estimation": probability_estimation}})
{_OUTPUT_VARIABLE_NAME} = {post_process_function}({finance_model}, {finance_function_object}, probability_estimation)
save({{"{_OUTPUT_VARIABLE_NAME}": {_OUTPUT_VARIABLE_NAME}}})
""".strip(),
    )
    return model.get_model()
