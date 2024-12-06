from classiq.interface.generator.functions.builtins.internal_operators import (
    INVERT_OPERATOR_NAME,
)
from classiq.interface.model.invert import Invert

from classiq.model_expansions.closure import Closure
from classiq.model_expansions.quantum_operations.call_emitter import CallEmitter
from classiq.model_expansions.scope import Scope


class InvertEmitter(CallEmitter[Invert]):
    def emit(self, invert: Invert, /) -> None:
        is_generative = invert.is_generative()
        if is_generative:
            context = self._register_generative_context(invert, INVERT_OPERATOR_NAME)
            invert = invert.model_copy(update={"body": context.statements("body")})

        if not is_generative and self._should_wrap(invert.body):
            self._emit_wrapped(invert)
            return

        self._emit_as_operation(invert)

    def _emit_as_operation(self, invert: Invert) -> None:
        invert_operation = Closure(
            name=INVERT_OPERATOR_NAME,
            blocks={"body": invert.body},
            scope=Scope(parent=self._current_scope),
        )
        context = self._expand_operation(invert_operation)
        self.emit_statement(
            Invert(body=context.statements("body"), source_ref=invert.source_ref)
        )

    def _emit_wrapped(self, invert: Invert) -> None:
        wrapping_function = self._create_expanded_wrapping_function(
            INVERT_OPERATOR_NAME, invert.body
        )
        self.emit_statement(
            Invert(body=[wrapping_function], source_ref=invert.source_ref)
        )
