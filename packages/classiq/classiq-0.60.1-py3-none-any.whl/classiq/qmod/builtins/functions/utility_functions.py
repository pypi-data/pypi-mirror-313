from typing import Annotated

from classiq.qmod.builtins.functions.standard_gates import H
from classiq.qmod.builtins.operations import repeat
from classiq.qmod.qfunc import qfunc
from classiq.qmod.qmod_variable import QArray, QBit, QCallable


@qfunc(external=True)
def apply_to_all(
    gate_operand: QCallable[Annotated[QBit, "target"]], target: QArray[QBit]
) -> None:
    """
    [Qmod Classiq-library function]

    Applies the single-qubit operand `gate_operand` to each qubit in the qubit
    array `target`.

    Args:
        gate_operand: The single-qubit gate to apply to each qubit in the array.
        target: The qubit array to apply the gate to.
    """
    repeat(target.len, lambda index: gate_operand(target[index]))


@qfunc(external=True)
def hadamard_transform(target: QArray[QBit]) -> None:
    """
    [Qmod Classiq-library function]

    Applies Hadamard transform to the target qubits.

    Corresponds to the braket notation:

    $$
     H^{\\otimes n} |x\rangle = \frac{1}{\\sqrt{2^n}} \\sum_{y=0}^{2^n - 1} (-1)^{x \\cdot y} |y\rangle
    $$

    Args:
        target:  qubits to apply to Hadamard transform to.

    """
    apply_to_all(H, target)
