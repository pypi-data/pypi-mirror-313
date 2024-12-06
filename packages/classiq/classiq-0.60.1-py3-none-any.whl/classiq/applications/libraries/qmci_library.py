from typing import cast

from classiq.interface.model.native_function_definition import NativeFunctionDefinition

from classiq.qmod.builtins.functions import Z, amplitude_estimation
from classiq.qmod.qfunc import qfunc
from classiq.qmod.qmod_variable import QArray, QBit, QNum
from classiq.qmod.quantum_callable import QCallable


@qfunc
def qmci(
    space_transform: QCallable[QArray[QBit], QBit],
    phase: QNum,
    packed_vars: QArray[QBit],
) -> None:
    amplitude_estimation(
        lambda reg: Z(reg[reg.len - 1]),
        lambda reg: space_transform(reg[0 : reg.len - 1], reg[reg.len - 1]),
        phase,
        packed_vars,
    )


QMCI_LIBRARY = [
    cast(
        NativeFunctionDefinition,
        qmci.create_model().function_dict["qmci"],
    ),
]
