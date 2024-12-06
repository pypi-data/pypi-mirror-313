from classiq.interface.model.handle_binding import HandleBinding
from classiq.interface.model.variable_declaration_statement import (
    VariableDeclarationStatement,
)

from classiq.model_expansions.evaluators.parameter_types import (
    evaluate_type_in_quantum_symbol,
)
from classiq.model_expansions.quantum_operations.emitter import Emitter
from classiq.model_expansions.scope import Evaluated, QuantumSymbol


class VariableDeclarationStatementEmitter(Emitter[VariableDeclarationStatement]):
    def emit(self, variable_declaration: VariableDeclarationStatement, /) -> None:
        var_decl = variable_declaration.model_copy()
        var_decl.quantum_type = variable_declaration.quantum_type.model_copy()
        self._current_scope[variable_declaration.name] = Evaluated(
            value=QuantumSymbol(
                handle=HandleBinding(name=var_decl.name),
                quantum_type=evaluate_type_in_quantum_symbol(
                    var_decl.quantum_type,
                    self._current_scope,
                    var_decl.name,
                ),
            ),
            defining_function=self._builder.current_function,
        )
        self.emit_statement(var_decl)
