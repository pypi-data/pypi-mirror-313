from typing import Literal

from classiq.qmod.builtins.functions.qft_functions import qft
from classiq.qmod.builtins.functions.standard_gates import PHASE
from classiq.qmod.builtins.operations import bind, repeat, within_apply
from classiq.qmod.cparam import CInt
from classiq.qmod.qfunc import qfunc
from classiq.qmod.qmod_parameter import CArray, CReal
from classiq.qmod.qmod_variable import Output, QArray, QBit, QNum
from classiq.qmod.symbolic import pi


@qfunc(external=True)
def unitary(
    elements: CArray[CArray[CReal]],
    target: QArray[QBit, Literal["log(get_field(elements[0], 'len'), 2)"]],
) -> None:
    """
    [Qmod core-library function]

    Applies a unitary matrix on a quantum state.

    Args:
        elements:  A 2d array of complex numbers representing the unitary matrix. This matrix must be unitary.
        target: The quantum state to apply the unitary on. Should be of corresponding size.
    """
    pass


@qfunc(external=True)
def add(
    left: QArray[QBit],
    right: QArray[QBit],
    result: Output[
        QArray[
            QBit, Literal["Max(get_field(left, 'len'), get_field(right, 'len')) + 1"]
        ]
    ],
) -> None:
    pass


@qfunc(external=True)
def modular_add(left: QArray[QBit], right: QArray[QBit]) -> None:
    pass


@qfunc(external=True)
def modular_add_constant(left: CReal, right: QNum) -> None:
    pass


@qfunc(external=True)
def integer_xor(left: QArray[QBit], right: QArray[QBit]) -> None:
    pass


@qfunc(external=True)
def real_xor_constant(left: CReal, right: QNum) -> None:
    pass


@qfunc(external=True)
def modular_increment(a: CInt, x: QNum) -> None:
    """
    [Qmod Classiq-library function]

    Adds $a$ to $x$ modulo the range of $x$, assumed that $x$ is a non-negative integer and $a$ is an integer.
    Mathematically it is described as:

    $$
        x = (x+a)\\ \\mod \\ 2^{x.size}-1
    $$

    Args:
        a: A classical integer to be added to x.
        x: A quantum number that is assumed to be non-negative integer.

    """
    array_cast: QArray = QArray("array_cast")
    within_apply(
        lambda: (  # type:ignore[arg-type]
            bind(x, array_cast),  # type:ignore[func-returns-value]
            qft(array_cast),
        ),
        lambda: repeat(
            x.size, lambda i: PHASE(a * 2 * pi * 2**i / (2**x.size), array_cast[i])
        ),
    )
