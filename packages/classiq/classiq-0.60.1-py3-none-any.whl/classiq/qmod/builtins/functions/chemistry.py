from typing import Literal

from classiq.qmod.builtins.structs import (
    FockHamiltonianProblem,
    MoleculeProblem,
)
from classiq.qmod.qfunc import qfunc
from classiq.qmod.qmod_parameter import CArray, CInt
from classiq.qmod.qmod_variable import QArray, QBit


@qfunc(external=True)
def molecule_ucc(
    molecule_problem: MoleculeProblem,
    excitations: CArray[CInt],
    qbv: QArray[
        QBit,
        Literal[
            "get_field(get_field(molecule_problem_to_hamiltonian(molecule_problem)[0], 'pauli'), 'len')"
        ],
    ],
) -> None:
    pass


@qfunc(external=True)
def molecule_hva(
    molecule_problem: MoleculeProblem,
    reps: CInt,
    qbv: QArray[
        QBit,
        Literal[
            "get_field(get_field(molecule_problem_to_hamiltonian(molecule_problem)[0], 'pauli'), 'len')"
        ],
    ],
) -> None:
    pass


@qfunc(external=True)
def molecule_hartree_fock(
    molecule_problem: MoleculeProblem,
    qbv: QArray[
        QBit,
        Literal[
            "get_field(get_field(molecule_problem_to_hamiltonian(molecule_problem)[0], 'pauli'), 'len')"
        ],
    ],
) -> None:
    pass


@qfunc(external=True)
def fock_hamiltonian_ucc(
    fock_hamiltonian_problem: FockHamiltonianProblem,
    excitations: CArray[CInt],
    qbv: QArray[
        QBit,
        Literal[
            "get_field(get_field(fock_hamiltonian_problem_to_hamiltonian(fock_hamiltonian_problem)[0], 'pauli'), 'len')"
        ],
    ],
) -> None:
    pass


@qfunc(external=True)
def fock_hamiltonian_hva(
    fock_hamiltonian_problem: FockHamiltonianProblem,
    reps: CInt,
    qbv: QArray[
        QBit,
        Literal[
            "get_field(get_field(fock_hamiltonian_problem_to_hamiltonian(fock_hamiltonian_problem)[0], 'pauli'), 'len')"
        ],
    ],
) -> None:
    pass


@qfunc(external=True)
def fock_hamiltonian_hartree_fock(
    fock_hamiltonian_problem: FockHamiltonianProblem,
    qbv: QArray[
        QBit,
        Literal[
            "get_field(get_field(fock_hamiltonian_problem_to_hamiltonian(fock_hamiltonian_problem)[0], 'pauli'), 'len')"
        ],
    ],
) -> None:
    pass
