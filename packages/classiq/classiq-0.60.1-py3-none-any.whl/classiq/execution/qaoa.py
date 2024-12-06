import math
from typing import Callable, Optional

import numpy as np
import scipy

from classiq.interface.executor.execution_preferences import ExecutionPreferences
from classiq.interface.executor.result import ExecutionDetails
from classiq.interface.model.model import SerializedModel

from classiq.execution import ExecutionSession
from classiq.qmod.builtins.functions import (
    RX,
    allocate,
    apply_to_all,
    hadamard_transform,
)
from classiq.qmod.builtins.operations import phase, repeat
from classiq.qmod.cparam import CReal
from classiq.qmod.create_model_function import create_model
from classiq.qmod.qfunc import qfunc
from classiq.qmod.qmod_parameter import CArray
from classiq.qmod.qmod_variable import Output, QVar
from classiq.synthesis import SerializedQuantumProgram, synthesize


def execute_qaoa(
    problem_vars: type[QVar],
    cost_func: Callable,
    num_layers: int,
    maxiter: int,
    execution_preferences: Optional[ExecutionPreferences] = None,
) -> tuple[SerializedModel, SerializedQuantumProgram, ExecutionDetails]:
    """
    Implements a simple QAOA algorithm, including the creation and synthesis of the QAOA
    ansatz and the classical optimization loop.

    Args:
        problem_vars: the quantum type (scalar, array, or struct) of the problem variable(s)
        cost_func: the arithmetic expression that evaluates the cost given an instance of the problem_vars type
        num_layers: the number of layers of the QAOA ansatz
        maxiter: the maximum number of iterations for the classical optimization loop
        execution_preferences: the execution settings for running the QAOA ansatz

    Returns:
        a tuple containing the model of the QAOA ansatz, the corresponding synthesized quantum program,
        and the result of the execution with the optimized parameters
    """

    @qfunc
    def main(
        params: CArray[CReal, num_layers * 2],  # type:ignore[valid-type]
        v: Output[problem_vars],  # type:ignore[valid-type]
    ) -> None:
        allocate(v.size, v)  # type:ignore[attr-defined]
        hadamard_transform(v)
        repeat(
            num_layers,
            lambda i: [  # type:ignore[arg-type]
                phase(-cost_func(v), params[i]),  # type:ignore[func-returns-value]
                apply_to_all(lambda q: RX(params[num_layers + i], q), v),
            ],
        )

    model = create_model(main)
    qprog = synthesize(model)

    with ExecutionSession(qprog, execution_preferences) as es:
        initial_params = (
            np.concatenate(
                (np.linspace(0, 1, num_layers), np.linspace(1, 0, num_layers))
            )
            * math.pi
        )
        final_params = scipy.optimize.minimize(
            lambda params: es.estimate_cost(
                lambda state: cost_func(state["v"]),
                {"params": params.tolist()},
            ),
            x0=initial_params,
            method="COBYLA",
            options={"maxiter": maxiter},
        ).x.tolist()
        result = es.sample({"params": final_params})

    return model, qprog, result
