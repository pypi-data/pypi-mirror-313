from collections.abc import Sequence

from classiq.interface.generator.constant import Constant

from classiq.qmod.builtins import BUILTIN_CONSTANTS
from classiq.qmod.semantics.error_manager import ErrorManager


def check_duplicate_constants(constants: Sequence[Constant]) -> None:
    known_constants = {constant.name: constant for constant in BUILTIN_CONSTANTS}
    for constant in constants:
        if constant.name in known_constants:
            with ErrorManager().node_context(constant):
                ErrorManager().add_error(f"Constant {constant.name!r} already exists")
        else:
            known_constants[constant.name] = constant
