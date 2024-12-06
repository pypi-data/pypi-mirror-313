from collections.abc import Sequence

from classiq.interface.model.classical_if import ClassicalIf
from classiq.interface.model.quantum_function_call import QuantumFunctionCall
from classiq.interface.model.quantum_statement import QuantumStatement

from classiq.model_expansions.closure import FunctionClosure
from classiq.model_expansions.quantum_operations.call_emitter import CallEmitter
from classiq.model_expansions.scope import Scope


def _is_all_identity_calls(body: Sequence[QuantumStatement]) -> bool:
    return all(
        isinstance(stmt, QuantumFunctionCall) and stmt.func_name.lower() == "identity"
        for stmt in body
    )


class ClassicalIfEmitter(CallEmitter[ClassicalIf]):
    def emit(self, classical_if: ClassicalIf, /) -> None:
        condition = self._interpreter.evaluate(classical_if.condition).as_type(bool)
        op_name = "then" if condition else "else"
        is_generative = classical_if.is_generative()

        body: Sequence[QuantumStatement]
        if is_generative:
            if not classical_if.has_generative_block(op_name):
                return
            context = self._register_generative_context(classical_if, op_name, op_name)
            context.blocks["body"] = context.blocks[op_name]
            context.blocks.pop(op_name)
            body = context.statements("body")
        else:
            body = classical_if.then if condition else classical_if.else_

        if _is_all_identity_calls(body):
            return

        if is_generative or not self._should_wrap(body):
            for stmt in body:
                if is_generative:
                    self._interpreter._builder.emit_statement(stmt)
                else:
                    self._interpreter.emit_statement(stmt)
            return

        then_else_func = FunctionClosure.create(
            name=op_name,
            body=body,
            scope=Scope(parent=self._current_scope),
            is_lambda=True,
        )
        self._emit_quantum_function_call(then_else_func, list())
