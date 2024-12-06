from classiq.qmod.builtins.classical_functions import qft_const_adder_phase
from classiq.qmod.builtins.functions.qft_functions import qft, qft_no_swap
from classiq.qmod.builtins.functions.standard_gates import PHASE, SWAP, X
from classiq.qmod.builtins.functions.state_preparation import allocate
from classiq.qmod.builtins.operations import bind, control, invert, repeat, within_apply
from classiq.qmod.cparam import CInt
from classiq.qmod.qfunc import qfunc
from classiq.qmod.qmod_variable import QArray, QBit, QNum
from classiq.qmod.symbolic import min, mod_inverse


@qfunc(external=True)
def _check_msb(ref: CInt, x: QArray[QBit], aux: QBit) -> None:
    within_apply(
        lambda: invert(lambda: qft_no_swap(x)), lambda: _ctrl_x(ref, x[0], aux)
    )


@qfunc(external=True)
def _ctrl_x(
    ref: CInt, ctrl: QNum, aux: QBit
) -> None:  # TODO: remove qfunc when expressions of QBit is supported
    control(ctrl == ref, lambda: X(aux))


@qfunc(external=True)
def qft_space_add_const(value: CInt, phi_b: QArray[QBit]) -> None:
    """
    [Qmod Classiq-library function]

    Adds a constant to a quantum number (in the Fourier space) using the Quantum Fourier Transform (QFT) Adder algorithm.
    Assuming that the input `phi_b` has `n` qubits, the result will be $\\phi_b+=value \\mod 2^n$.

    To perform the full algorithm, use:
    within_apply(lambda: QFT(phi_b), qft_space_add_const(value, phi_b))

    Args:
        value: The constant to add to the quantum number.
        phi_b: The quantum number (at the aft space) to which the constant is added.

    """
    repeat(
        count=phi_b.len,
        iteration=lambda index: PHASE(
            theta=qft_const_adder_phase(
                index, value, phi_b.len  # type:ignore[arg-type]
            ),
            target=phi_b[index],
        ),
    )


@qfunc(external=True)
def cc_modular_add(n: CInt, a: CInt, phi_b: QArray[QBit], c1: QBit, c2: QBit) -> None:
    """
    [Qmod Classiq-library function]

    Adds a constant `a` to a quantum number `phi_b` modulo the constant `n`, controlled by 2 qubits.
    The quantum number `phi_b` and the constant `a` are assumed to be in the QFT space.

    Args:
        n: The modulo number.
        a: The constant to add to the quantum number.
        phi_b: The quantum number to which the constant is added.
        c1: a control qubit.
        c2: a control qubit.

    """
    ctrl: QArray[QBit] = QArray("ctrl")
    aux = QBit("aux")

    within_apply(
        lambda: (  # type:ignore[arg-type]
            allocate(1, aux),
            bind([c1, c2], ctrl),  # type:ignore[func-returns-value]
        ),
        lambda: (  # type:ignore[arg-type]
            control(  # type:ignore[func-returns-value]
                ctrl, lambda: qft_space_add_const(a, phi_b)
            ),
            invert(  # type:ignore[func-returns-value]
                lambda: qft_space_add_const(n, phi_b)
            ),
            _check_msb(1, phi_b, aux),
            control(  # type:ignore[func-returns-value]
                aux, lambda: qft_space_add_const(n, phi_b)
            ),
            within_apply(
                lambda: invert(  # type:ignore[func-returns-value]
                    lambda: control(ctrl, lambda: qft_space_add_const(a, phi_b))
                ),
                lambda: _check_msb(0, phi_b, aux),
            ),
        ),
    )


@qfunc(external=True)
def c_modular_multiply(
    n: CInt, a: CInt, b: QArray[QBit], x: QArray[QBit], ctrl: QBit
) -> None:
    """
    [Qmod Classiq-library function]

    Performs out-of-place multiplication of a quantum number `x` by a classical number `a` modulo classical number `n`,
    controlled by a quantum bit `ctrl` and adds the result to a quantum array `b`. Applies $b += xa \\mod n$ if `ctrl=1`, and the identity otherwise.

    Args:
        n: The modulo number. Should be non-negative.
        a: The classical factor. Should be non-negative.
        b: The quantum number added to the multiplication result. Stores the result of the multiplication.
        x: The quantum factor.
        ctrl: The control bit.
    """
    within_apply(
        lambda: qft(b),
        lambda: repeat(
            count=x.len,
            iteration=lambda index: cc_modular_add(
                n, (a * (2**index)) % n, b, x[index], ctrl
            ),
        ),
    )


@qfunc(external=True)
def multiswap(x: QArray[QBit], y: QArray[QBit]) -> None:
    """
    [Qmod Classiq-library function]

    Swaps the qubit states between two arrays.
    Qubits of respective indices are swapped, and additional qubits in the longer array are left unchanged.

    Args:
        x: The first array
        y: The second array

    """
    repeat(
        count=min(x.len, y.len),
        iteration=lambda index: SWAP(x[index], y[index]),
    )


@qfunc(external=True)
def inplace_c_modular_multiply(n: CInt, a: CInt, x: QArray[QBit], ctrl: QBit) -> None:
    """
    [Qmod Classiq-library function]

    Performs multiplication of a quantum number `x` by a classical number `a` modulo classical number `n`,
    controlled by a quantum bit `ctrl`. Applies $x=xa \\mod n$ if `ctrl=1`, and the identity otherwise.

    Args:
        n: The modulo number. Should be non-negative.
        a: The classical factor. Should be non-negative.
        x: The quantum factor.
        ctrl: The control bit.
    """
    b: QArray[QBit] = QArray("b")

    within_apply(
        lambda: allocate(x.len + 1, b),
        lambda: (  # type:ignore[arg-type]
            c_modular_multiply(n, a, b, x, ctrl),
            control(  # type:ignore[func-returns-value]
                ctrl, lambda: multiswap(x, b)
            ),
            invert(  # type:ignore[func-returns-value]
                lambda: c_modular_multiply(n, mod_inverse(a, n), b, x, ctrl)
            ),
        ),
    )


@qfunc(external=True)
def modular_exp(n: CInt, a: CInt, x: QArray[QBit], power: QArray[QBit]) -> None:
    """
    [Qmod Classiq-library function]

    Raises a classical integer `a` to the power of a quantum number `power` modulo classical integer `n`
    times a quantum number `x`. Performs $x=(a^{power} \\mod n)*x$ in-place.
    (and specifically if at the input $x=1$, at the output $x=a^{power} \\mod n$).

    Args:
        n: The modulus number. Should be non-negative.
        a: The base of the exponentiation. Should be non-negative.
        x: A quantum number that multiplies the modular exponentiation and holds the output. It should be at least the size of $\\lceil \\log(n) \rceil$.
        power: The power of the exponentiation.
    """
    repeat(
        count=power.len,
        iteration=lambda index: inplace_c_modular_multiply(
            n, (a ** (2**index)) % n, x, power[index]
        ),
    )
