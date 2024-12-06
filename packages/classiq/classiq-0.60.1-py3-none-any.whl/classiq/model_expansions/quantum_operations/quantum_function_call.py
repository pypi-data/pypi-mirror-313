from typing import TYPE_CHECKING

from classiq.interface.model.quantum_function_call import QuantumFunctionCall

from classiq.model_expansions.closure import FunctionClosure
from classiq.model_expansions.quantum_operations.call_emitter import CallEmitter
from classiq.qmod.semantics.error_manager import ErrorManager

if TYPE_CHECKING:
    from classiq.model_expansions.interpreter import Interpreter


class QuantumFunctionCallEmitter(CallEmitter[QuantumFunctionCall]):
    def __init__(self, interpreter: "Interpreter") -> None:
        super().__init__(interpreter)
        self._model = self._interpreter._model

    def emit(self, call: QuantumFunctionCall, /) -> None:
        function = self._interpreter.evaluate(call.function).as_type(FunctionClosure)
        args = call.positional_args
        with ErrorManager().call(function.name), function.freeze():
            self._emit_quantum_function_call(function, args)
