from typing import Literal

from classiq.qmod.builtins.enums import Pauli
from classiq.qmod.builtins.structs import (
    PauliTerm,
)
from classiq.qmod.qfunc import qfunc
from classiq.qmod.qmod_parameter import CArray, CInt, CReal
from classiq.qmod.qmod_variable import QArray, QBit


@qfunc(external=True)
def single_pauli_exponent(
    pauli_string: CArray[Pauli],
    coefficient: CReal,
    qbv: QArray[QBit, Literal["get_field(pauli_string, 'len')"]],
) -> None:
    """
    [Qmod core-library function]

    Exponentiates the specified single Pauli operator multiplied by some coefficient.

    Args:
        pauli_string: The Pauli operator to be exponentiated.
        coefficient: A coefficient multiplying the Pauli operator.
        qbv: The target quantum variable of the exponentiation.
    """
    pass


@qfunc(external=True)
def suzuki_trotter(
    pauli_operator: CArray[PauliTerm],
    evolution_coefficient: CReal,
    order: CInt,
    repetitions: CInt,
    qbv: QArray[
        QBit, Literal["get_field(get_field(pauli_operator[0], 'pauli'), 'len')"]
    ],
) -> None:
    """
    [Qmod core-library function]

    Applies the Suzuki-Trotter decomposition to a Pauli operator. The Suzuki-Trotter decomposition is a method for approximating the exponential of a sum of operators by a product of exponentials of each operator.
    The Suzuki-Trotter decomposition of a given order nullifies the error of the Taylor series expansion of the product of exponentials up to that order.
    The error of a Suzuki-Trotter decomposition decreases as the order and number of repetitions increase.

    Args:
        pauli_operator: The Pauli operator to be exponentiated.
        evolution_coefficient: A global evolution coefficient multiplying the Pauli operator.
        order: The order of the Suzuki-Trotter decomposition.
        repetitions: The number of repetitions of the Suzuki-Trotter decomposition.
        qbv: The target quantum variable of the exponentiation.
    """
    pass


@qfunc(external=True)
def qdrift(
    pauli_operator: CArray[PauliTerm],
    evolution_coefficient: CReal,
    num_qdrift: CInt,
    qbv: QArray[
        QBit, Literal["get_field(get_field(pauli_operator[0], 'pauli'), 'len')"]
    ],
) -> None:
    """
    [Qmod core-library function]

    Exponentiates a Pauli operator using the QDrift method. The QDrift method is a stochastic method based on the Trotter decomposition for approximating the exponential of a sum of operators by a product of exponentials of each operator.
    The QDrift method randomizes the order of the operators in the product of exponentials to stochastically reduce the error of the approximation.
    The error of the QDrift method decreases as the number of QDrift steps increases.

    Args:
        pauli_operator: The Pauli operator to be exponentiated.
        evolution_coefficient: A global evolution coefficient multiplying the Pauli operator.
        num_qdrift : The number of QDrift steps.
        qbv: The target quantum variable of the exponentiation.
    """
    pass


@qfunc(external=True)
def exponentiation_with_depth_constraint(
    pauli_operator: CArray[PauliTerm],
    evolution_coefficient: CReal,
    max_depth: CInt,
    qbv: QArray[
        QBit, Literal["get_field(get_field(pauli_operator[0], 'pauli'), 'len')"]
    ],
) -> None:
    """
    [Qmod core-library function]

    Exponentiates a Pauli operator via the Suzuki-Trotter decomposition with a depth constraint.
    The Suzuki-Trotter decomposition is a method for approximating the exponential of a sum of operators by a product of exponentials of each operator.
    This function automatically determines the order and number of repetitions of the Suzuki-Trotter decomposition to minimize the error given a depth constraint.

    Args:
        pauli_operator: The Pauli operator to be exponentiated.
        evolution_coefficient: A global coefficient multiplying the Pauli operator.
        max_depth: The maximum depth of the exponentiation.
        qbv: The target quantum variable of the exponentiation.
    """
    pass
