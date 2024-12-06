from typing import Literal

from classiq.qmod.builtins.functions.arithmetic import modular_increment
from classiq.qmod.builtins.functions.standard_gates import CX, IDENTITY, RY, H, X
from classiq.qmod.builtins.functions.utility_functions import hadamard_transform
from classiq.qmod.builtins.operations import control, if_, repeat
from classiq.qmod.cparam import CBool, CInt
from classiq.qmod.qfunc import qfunc
from classiq.qmod.qmod_parameter import CArray, CReal
from classiq.qmod.qmod_variable import Input, Output, QArray, QBit, QNum
from classiq.qmod.symbolic import (
    asin,
    atan,
    exp,
    floor,
    log,
    max as qmax,
    min as qmin,
    pi,
    sqrt,
)


@qfunc(external=True)
def allocate(
    num_qubits: CInt, out: Output[QArray[QBit, Literal["num_qubits"]]]
) -> None:
    """
    [Qmod core-library function]

    Allocates the specified number of qubits to a given quantum variable and initializes
    them in the zero state:

    $$
        \\left|\\text{out}\\right\\rangle = \\left|0\\right\\rangle^{\\otimes \\text{num_qubits}}
    $$

    Args:
        num_qubits: The number of qubits to allocate. Must be a positive integer.
        out: The quantum variable that will receive the allocated qubits. Must be uninitialized before allocation.

    Notes:
        1. If the output variable has been declared with a specific number of qubits, the number of qubits allocated must match the declared number.
        2. The synthesis engine automatically handles the allocation, either by drawing new qubits from the available pool or by reusing existing ones.
    """
    pass


@qfunc(external=True)
def allocate_num(
    num_qubits: CInt,
    is_signed: CBool,
    fraction_digits: CInt,
    out: Output[
        QNum[Literal["num_qubits"], Literal["is_signed"], Literal["fraction_digits"]]
    ],
) -> None:
    """
    [Qmod Classiq-library function]

    Initializes a quantum number with the given number of qubits, sign, and fractional digits.

    Args:
        num_qubits: The number of qubits to allocate.
        is_signed: Whether the number is signed or unsigned.
        fraction_digits: The number of fractional digits.
    """
    allocate(num_qubits, out)


@qfunc(external=True)
def free(in_: Input[QArray[QBit]]) -> None:
    """
    [Qmod core-library function]

    Releases the qubits allocated to a quantum variable, allowing them to be reused.

    Args:
        in_: The quantum variable that will be freed. Must be initialized before.

    Note:
        This operation does not uncompute the qubits. It is the responsibility of the user to ensure that the qubits are at the zero state before freeing them.
    """
    pass


@qfunc(external=True)
def prepare_state(
    probabilities: CArray[CReal],
    bound: CReal,
    out: Output[QArray[QBit, Literal["log(get_field(probabilities, 'len'), 2)"]]],
) -> None:
    """
    [Qmod core-library function]

    Initializes a quantum variable in a state corresponding to a given probability distribution:

    $$
        \\left|\\text{out}\\right\\rangle = \\sum_{i=0}^{\\text{len(probabilities)}-1} \\sqrt{\\text{probabilities}[i]} \\left|i\\right\\rangle
    $$

    with $i = 0, 1, 2, ..., \\text{len(amplitudes)}-1$ corresponding to computational basis states.

    Args:
        probabilities: The probability distribution to initialize the quantum variable. Must be a valid probability distribution, i.e., a list of non-negative real numbers that sum to 1. Must have a valid length (a power of 2).
        bound: An error bound, expressed as the $L^{2}$ norm between the expected and actual distributions. A larger bound can reduce the circuit size at the expense of accuracy. Must be a positive real number.
        out: The quantum variable that will receive the initialized state. Must be uninitialized.

    Notes:
        1. If the output variable has been declared with a specific number of qubits, the number of qubits formed by the distribution must match the declared number.
        2. The synthesis engine automatically handles the allocation, either by drawing new qubits from the available pool or by reusing existing ones.
    """
    pass


@qfunc(external=True)
def prepare_amplitudes(
    amplitudes: CArray[CReal],
    bound: CReal,
    out: Output[QArray[QBit, Literal["log(get_field(amplitudes, 'len'), 2)"]]],
) -> None:
    """
    [Qmod core-library function]

    Initializes a quantum variable in a state corresponding to the given amplitudes:

    $$
        \\left|\\text{out}\\right\\rangle = \\sum_{i=0}^{\\text{len(amplitudes)}-1} \\text{amplitudes}[i] \\left|i\\right\\rangle
    $$

    with $i = 0, 1, 2, ..., \\text{len(amplitudes)}-1$ corresponding to computational basis states.

    Args:
        amplitudes: The amplitudes to initialize the quantum variable. Must be a valid real quantum state vector, i.e., the sum of squares should be 1. Must have a valid length (a power of 2).
        bound: An error bound, expressed as the $L^{2}$ norm between the expected and actual distributions. A larger bound can reduce the circuit size at the expense of accuracy. Must be a positive real number.
        out: The quantum variable that will receive the initialized state. Must be uninitialized.

    Notes:
        1. If the output variable has been declared with a specific number of qubits, the number of qubits formed by the distribution must match the declared number.
        2. The synthesis engine automatically handles the allocation, either by drawing new qubits from the available pool or by reusing existing ones.
    """
    pass


@qfunc(external=True)
def inplace_prepare_state(
    probabilities: CArray[CReal],
    bound: CReal,
    target: QArray[QBit, Literal["log(get_field(probabilities, 'len'), 2)"]],
) -> None:
    """
    [Qmod core-library function]

    Transforms a given quantum variable in the state |0> to the state per the specified probability distribution
    (similar to `prepare_state` but preformed on an initialized variable).

    Args:
        probabilities: The probability distribution corresponding to the quantum variable state. Must be a valid probability distribution, i.e., a list of non-negative real numbers that sum to 1. Must have a valid length (a power of 2).
        bound: An error bound, expressed as the $L^{2}$ norm between the expected and actual distributions. A larger bound can reduce the circuit size at the expense of accuracy. Must be a positive real number.
        target: The quantum variable to act upon.

    This is useful as part of quantum building blocks like the Grover diffuser operator, $\\left|\\psi\\right\\rangle\\left\\langle\\psi\\right| \\left( 2\\left|0\\right\\rangle\\left\\langle0\\right| - \\mathcal{I} \\right)$, where the output state of the oracle is reflected about this state.

    """
    pass


@qfunc(external=True)
def inplace_prepare_amplitudes(
    amplitudes: CArray[CReal],
    bound: CReal,
    target: QArray[QBit, Literal["log(get_field(amplitudes, 'len'), 2)"]],
) -> None:
    """
    [Qmod core-library function]

    Transforms a given quantum variable in the state |0> to the state per the specified amplitudes
    (similar to `prepare_amplitudes` but preformed on an initialized variable).

    Args:
        amplitudes: The amplitudes to initialize the quantum variable. Must be a valid real quantum state vector, i.e., the sum of squares should be 1. Must have a valid length (a power of 2).
        bound: An error bound, expressed as the $L^{2}$ norm between the expected and actual distributions. A larger bound can reduce the circuit size at the expense of accuracy. Must be a positive real number.
        target: The quantum variable to act upon.

    This is useful as part of quantum building blocks like the Grover diffuser operator, $\\left|\\psi\\right\\rangle\\left\\langle\\psi\\right| \\left( 2\\left|0\\right\\rangle\\left\\langle0\\right| - \\mathcal{I} \\right)$, where the output state of the oracle is reflected about this state.

    """
    pass


def prepare_uniform_trimmed_state_apply_rotation(
    size_lsb: CInt, lsbs_val: CInt, rotation_var: QBit
) -> None:
    # max hold for the case where the value is on the left side
    # the fraction in the sqrt is the wanted amount of probability
    # in the left side divided by the total amount
    RY(
        -2 * (asin(sqrt(qmin((2 ** (size_lsb)) / lsbs_val, 1))) + pi / 4) + pi,
        rotation_var,
    )


@qfunc(external=True)
def _prepare_uniform_trimmed_state_step(
    size_lsb: CInt, ctrl_val: CInt, lsbs_val: CInt, ctrl_var: QNum, rotation_var: QBit
) -> None:
    if_(
        lsbs_val != 0,  # stop condition
        lambda: control(
            ctrl_var == ctrl_val,
            lambda: prepare_uniform_trimmed_state_apply_rotation(
                size_lsb, lsbs_val, rotation_var
            ),
        ),
    )


@qfunc(external=True)
def prepare_uniform_trimmed_state(m: CInt, q: QArray[QBit]) -> None:
    """
    [Qmod Classiq-library function]

    Initializes a quantum variable in a uniform superposition of the first `m` computational basis states:

    $$
        \\left|\\text{q}\\right\\rangle = \\frac{1}{\\sqrt{m}}\\sum_{i=0}^{m-1}{|i\\rangle}
    $$

    The number of allocated qubits would be $\\left\\lceil\\log_2{m}\\right\\rceil$.
    The function is especially useful when `m` is not a power of 2.

    Args:
        m: The number of states to load in the superposition.
        q: The quantum variable that will receive the initialized state. Must be uninitialized.

    Notes:
        1. If the output variable has been declared with a specific number of qubits, it must match the number of allocated qubits.
        2. The synthesis engine automatically handles the allocation, either by drawing new qubits from the available pool or by reusing existing ones.
    """
    hadamard_transform(q)

    if_(
        m < 2**q.len,
        # initial step without control
        lambda: prepare_uniform_trimmed_state_apply_rotation(
            q.len - 1,  # type:ignore[arg-type]
            m,
            q[q.len - 1],
        ),
    )

    repeat(
        qmax(q.len - 1, 0),
        lambda i: _prepare_uniform_trimmed_state_step(
            q.len - i - 2,
            floor(m / (2 ** (q.len - i - 1))),
            m % (2 ** (q.len - i - 1)),
            q[q.len - i - 1 : q.len],
            q[q.len - i - 2],
        ),
    )


@qfunc(external=True)
def prepare_uniform_interval_state(start: CInt, end: CInt, q: QArray[QBit]) -> None:
    """
    [Qmod Classiq-library function]

    Initializes a quantum variable in a uniform superposition of the specified interval in the computational basis states:

    $$
        \\left|\\text{q}\\right\\rangle = \\frac{1}{\\sqrt{\\text{end} - \\text{start}}}\\sum_{i=\\text{start}}^{\\text{end}-1}{|i\\rangle}
    $$

    The number of allocated qubits would be $\\left\\lceil\\log_2{\\left(\\text{end}\\right)}\\right\\rceil$.

    Args:
        start: The lower bound of the interval to load (inclusive).
        end: The upper bound of the interval to load (exclusive).
        q: The quantum variable that will receive the initialized state. Must be uninitialized.

    Notes:
        1. If the output variable has been declared with a specific number of qubits, it must match the number of allocated qubits.
        2. The synthesis engine automatically handles the allocation, either by drawing new qubits from the available pool or by reusing existing ones.
    """
    prepare_uniform_trimmed_state(end - start, q)
    modular_increment(start, q)


@qfunc(external=True)
def prepare_ghz_state(size: CInt, q: Output[QArray[QBit]]) -> None:
    """
    [Qmod Classiq-library function]

    Initializes a quantum variable in a Greenberger-Horne-Zeilinger (GHZ) state. i.e., a balanced superposition of all ones and all zeros, on an arbitrary number of qubits..

    Args:
        size: The number of qubits in the GHZ state. Must be a positive integer.
        q: The quantum variable that will receive the initialized state. Must be uninitialized.

    Notes:
        The synthesis engine automatically handles the allocation, either by drawing new qubits from the available pool or by reusing existing ones.


    """

    def inner_lop(step: CInt) -> None:
        repeat(
            count=2**step,
            iteration=lambda control_index: if_(
                condition=control_index + 2**step >= size,
                then=lambda: IDENTITY(q[0]),
                else_=lambda: CX(q[control_index], q[control_index + 2**step]),
            ),
        )

    allocate(size, q)
    H(q[0])
    repeat(floor(log(size - 1, 2)) + 1, inner_lop)  # type:ignore[arg-type]


@qfunc(external=True)
def prepare_exponential_state(rate: CInt, q: QArray[QBit]) -> None:
    """

    [Qmod Classiq-library function]

    Prepares a quantum state with exponentially decreasing amplitudes. The state is prepared in the computational basis, with the amplitudes of the states decreasing exponentially with the index of the state:

    $$
        P(n) = \\frac{1}{Z} e^{- \\text{rate} \\cdot n}
    $$

    Args:
        rate: The rate of the exponential decay.
        q: The quantum register to prepare.
    """
    repeat(q.len, lambda i: RY(2.0 * atan(exp((-rate * 2.0**i) / 2.0)), q[i]))


@qfunc(external=True)
def prepare_bell_state(state_num: CInt, q: Output[QArray[QBit, Literal[2]]]) -> None:
    """
    [Qmod Classiq-library function]

    Initializes a quantum array of size 2 in one of the four Bell states.

    Args:
        state_num: The number of the Bell state to be prepared. Must be an integer between 0 and 3.
        q: The quantum variable that will receive the initialized state. Must be uninitialized.

    Bell States:
        The four Bell states are defined as follows (each state correlates to an integer between 0 and 3 as defined by the `state_num` argument):

        If `state_num` = 0 the function prepares the Bell state:

        $$
            \\left|\\Phi^+\\right\\rangle = \\frac{1}{\\sqrt{2}} \\left( \\left| 00 \\right\\rangle + \\left| 11 \\right\\rangle \\right)
        $$

        If `state_num` = 1 the function prepares the Bell state:

        $$
            \\left|\\Phi^-\\right\\rangle = \\frac{1}{\\sqrt{2}} \\left( \\left| 00 \\right\\rangle - \\left| 11 \\right\\rangle \\right)
        $$

        If `state_num` = 2 the function prepares the Bell state:

        $$
            \\left|\\Psi^+\\right\\rangle = \\frac{1}{\\sqrt{2}} \\left( \\left| 01 \\right\\rangle + \\left| 10 \\right\\rangle \\right)
        $$

        If `state_num` = 3 the function prepares the Bell state:

        $$
            \\left|\\Psi^-\\right\\rangle = \\frac{1}{\\sqrt{2}} \\left( \\left| 01 \\right\\rangle - \\left| 10 \\right\\rangle \\right)
        $$

    Notes:
        The synthesis engine automatically handles the allocation, either by drawing new qubits from the available pool or by reusing existing ones.


    """
    allocate(2, q)
    inplace_prepare_int(state_num, q)
    H(q[0])
    CX(q[0], q[1])


@qfunc(external=True)
def inplace_prepare_int(value: CInt, target: QArray[QBit]) -> None:
    """
    [Qmod Classiq-library function]

    Transitions a quantum variable in the zero state $|0\\rangle$ into the computational basis state $|\\text{value}\\rangle$.
    In the general case, the function performs a bitwise-XOR, i.e. transitions the state $|\\psi\\rangle$ into $|\\psi \\oplus \\text{value}\\rangle$.

    Args:
        value: The value to assign to the quantum variable.
        target: The quantum variable to act upon.

    Note:
        If the value cannot fit into the quantum variable, it is truncated, i.e. treated as the value modulo $2^\\text{target.size}$.
    """
    repeat(
        target.len,
        lambda index: if_(
            (floor(value / (2**index)) % 2) == 1,
            lambda: X(target[index]),
            lambda: IDENTITY(target[index]),
        ),
    )


@qfunc(external=True)
def prepare_int(
    value: CInt,
    out: Output[QNum[Literal["floor(log(value, 2)) + 1"]]],
) -> None:
    """
    [Qmod Classiq-library function]

    Initializes a quantum variable to the computational basis state $|\\text{value}\\rangle$.
    The number of allocated qubits is automatically computed from the value, and is the minimal number required for representation in the computational basis.

    Args:
        value: The value to assign to the quantum variable.
        out: The allocated quantum variable. Must be uninitialized.

    Note:
        If the output variable has been declared with a specific number of qubits, it must match the number of allocated qubits.
    """
    allocate(floor(log(value, 2)) + 1, out)
    inplace_prepare_int(value, out)
