from typing import TYPE_CHECKING, Literal

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.model.quantum_statement import QuantumOperation

if TYPE_CHECKING:
    from classiq.interface.model.statement_block import StatementBlock


class ClassicalIf(QuantumOperation):
    kind: Literal["ClassicalIf"]

    condition: Expression
    then: "StatementBlock"
    else_: "StatementBlock"
