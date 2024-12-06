from dataclasses import dataclass, fields, is_dataclass

from classiq.interface.generator.types.struct_declaration import StructDeclaration

from classiq.qmod.builtins.enums import LadderOperator, Pauli
from classiq.qmod.cparam import CArray, CBool, CInt, CReal
from classiq.qmod.python_classical_type import PythonClassicalType


@dataclass
class PauliTerm:
    """
    A term in a Hamiltonian, represented as a product of Pauli operators.

    Attributes:
        pauli (CArray[Pauli]): The list of the chosen Pauli operators in the term, corresponds to a product of them.
        coefficient (CReal): The coefficient of the term (floating number).
    """

    pauli: CArray[Pauli]
    coefficient: CReal


@dataclass
class Position:
    x: CReal
    y: CReal
    z: CReal


@dataclass
class ChemistryAtom:
    element: CInt
    position: Position


@dataclass
class Molecule:
    atoms: CArray[ChemistryAtom]
    spin: CInt
    charge: CInt


@dataclass
class MoleculeProblem:
    mapping: CInt
    z2_symmetries: CBool
    molecule: Molecule
    freeze_core: CBool
    remove_orbitals: CArray[CInt]


@dataclass
class LadderOp:
    op: LadderOperator
    index: CInt


@dataclass
class LadderTerm:
    coefficient: CReal
    ops: CArray[LadderOp]


@dataclass
class FockHamiltonianProblem:
    mapping: CInt
    z2_symmetries: CBool
    terms: CArray[LadderTerm]
    num_particles: CArray[CInt]


@dataclass
class CombinatorialOptimizationSolution:
    probability: CReal
    cost: CReal
    solution: CArray[CInt]
    count: CInt


@dataclass
class GaussianModel:
    num_qubits: CInt
    normal_max_value: CReal
    default_probabilities: CArray[CReal]
    rhos: CArray[CReal]
    loss: CArray[CInt]
    min_loss: CInt


@dataclass
class LogNormalModel:
    num_qubits: CInt
    mu: CReal
    sigma: CReal


@dataclass
class FinanceFunction:
    f: CInt
    threshold: CReal
    larger: CBool
    polynomial_degree: CInt
    use_chebyshev_polynomial_approximation: CBool
    tail_probability: CReal


@dataclass
class QsvmResult:
    test_score: CReal
    predicted_labels: CArray[CReal]


@dataclass
class QSVMFeatureMapPauli:
    feature_dimension: CInt
    reps: CInt
    entanglement: CInt
    alpha: CReal
    paulis: CArray[CArray[Pauli]]


BUILTIN_STRUCT_DECLARATIONS = {
    struct_decl.__name__: StructDeclaration(
        name=struct_decl.__name__,
        variables={
            field.name: PythonClassicalType().convert(field.type)
            for field in fields(struct_decl)
        },
    )
    for struct_decl in vars().values()
    if is_dataclass(struct_decl)
}


__all__ = [
    "PauliTerm",
    "MoleculeProblem",
    "Molecule",
    "ChemistryAtom",
    "Position",
    "FockHamiltonianProblem",
    "LadderTerm",
    "LadderOp",
    "CombinatorialOptimizationSolution",
    "GaussianModel",
    "LogNormalModel",
    "FinanceFunction",
    "QsvmResult",
    "QSVMFeatureMapPauli",
]
