from classiq.interface.ast_node import ASTNode
from classiq.interface.generator.functions.concrete_types import ConcreteQuantumType


class QuantumVariableDeclaration(ASTNode):
    name: str
    quantum_type: ConcreteQuantumType
