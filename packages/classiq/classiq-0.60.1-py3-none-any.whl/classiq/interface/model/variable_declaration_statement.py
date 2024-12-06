from typing import Literal

from classiq.interface.model.quantum_statement import QuantumStatement
from classiq.interface.model.quantum_variable_declaration import (
    QuantumVariableDeclaration,
)


class VariableDeclarationStatement(QuantumStatement, QuantumVariableDeclaration):
    kind: Literal["VariableDeclarationStatement"]
