from classiq.interface.exceptions import ClassiqExpansionError
from classiq.interface.model.bind_operation import BindOperation

from classiq.model_expansions.evaluators.parameter_types import (
    evaluate_types_in_quantum_symbols,
)
from classiq.model_expansions.evaluators.quantum_type_utils import (
    set_size,
    validate_bind_targets,
)
from classiq.model_expansions.quantum_operations.emitter import Emitter
from classiq.model_expansions.scope import QuantumSymbol


class BindEmitter(Emitter[BindOperation]):
    def emit(self, bind: BindOperation, /) -> None:
        inputs: list[QuantumSymbol] = [
            self._interpreter.evaluate(arg).as_type(QuantumSymbol)
            for arg in bind.in_handles
        ]
        outputs: list[QuantumSymbol] = [
            self._interpreter.evaluate(arg).as_type(QuantumSymbol)
            for arg in bind.out_handles
        ]
        inputs = evaluate_types_in_quantum_symbols(inputs, self._current_scope)
        outputs = evaluate_types_in_quantum_symbols(outputs, self._current_scope)
        validate_bind_targets(bind, self._current_scope)
        unsized_outputs = [
            output for output in outputs if not output.quantum_type.has_size_in_bits
        ]

        if len(unsized_outputs) > 1:
            raise ClassiqExpansionError(
                f"Cannot perform the split operation {bind.in_handles[0].name} -> {{{', '.join(out_handle.name for out_handle in bind.out_handles)}}}:\n"
                f"Quantum variables {', '.join(str(out_handle.handle) for out_handle in unsized_outputs)} are used as bind outputs, but their size cannot be inferred."
            )

        input_size = sum(input.quantum_type.size_in_bits for input in inputs)
        output_size = sum(
            output.quantum_type.size_in_bits
            for output in outputs
            if output.quantum_type.has_size_in_bits
        )

        if len(unsized_outputs) == 1:
            set_size(
                unsized_outputs[0].quantum_type,
                input_size - output_size,
                str(unsized_outputs[0].handle),
            )

        else:
            if input_size != output_size:
                raise ClassiqExpansionError(
                    f"The total size for the input and output of the bind operation must be the same. The in size is {input_size} and the out size is {output_size}"
                )

        self.emit_statement(
            BindOperation(in_handles=bind.in_handles, out_handles=bind.out_handles)
        )
