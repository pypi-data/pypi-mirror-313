from classiq.interface.model.native_function_definition import NativeFunctionDefinition

from ...quantum_function import GenerativeQFunc
from .amplitude_estimation import *
from .arithmetic import *
from .benchmarking import *
from .chemistry import *
from .discrete_sine_cosine_transform import *
from .discrete_sine_cosine_transform import _qct_d_operator, _qct_pi_operator
from .exponentiation import *
from .finance import *
from .grover import *
from .hea import *
from .linear_pauli_rotation import *
from .linear_pauli_rotation import _single_pauli
from .modular_exponentiation import *
from .modular_exponentiation import _check_msb, _ctrl_x
from .operators import *
from .qaoa_penalty import *
from .qft_functions import *
from .qpe import *
from .qsvm import *
from .qsvt import *
from .standard_gates import *
from .state_preparation import *
from .state_preparation import _prepare_uniform_trimmed_state_step
from .swap_test import *
from .utility_functions import *
from .variational import *

CORE_LIB_DECLS = [
    func.func_decl
    for func in (
        molecule_ucc,
        molecule_hva,
        molecule_hartree_fock,
        fock_hamiltonian_ucc,
        fock_hamiltonian_hva,
        fock_hamiltonian_hartree_fock,
        log_normal_finance,
        gaussian_finance,
        pauli_feature_map,
        bloch_sphere_feature_map,
        H,
        X,
        Y,
        Z,
        I,
        S,
        T,
        SDG,
        TDG,
        PHASE,
        RX,
        RY,
        RZ,
        R,
        RXX,
        RYY,
        RZZ,
        CH,
        CX,
        CY,
        CZ,
        CRX,
        CRY,
        CRZ,
        CPHASE,
        SWAP,
        IDENTITY,
        prepare_state,
        prepare_amplitudes,
        unitary,
        add,
        modular_add,
        integer_xor,
        modular_add_constant,
        real_xor_constant,
        U,
        CCX,
        allocate,
        free,
        randomized_benchmarking,
        inplace_prepare_state,
        inplace_prepare_amplitudes,
        single_pauli_exponent,
        suzuki_trotter,
        qdrift,
        exponentiation_with_depth_constraint,
    )
]

OPEN_LIBRARY_UNPROCESSED_FUNCTIONS = [
    qpe_flexible,
    qpe,
    _single_pauli,
    linear_pauli_rotations,
    amplitude_estimation,
    phase_oracle,
    reflect_about_zero,
    grover_diffuser,
    grover_operator,
    grover_search,
    hadamard_transform,
    apply_to_all,
    qft_no_swap,
    qft_space_add_const,
    cc_modular_add,
    c_modular_multiply,
    multiswap,
    inplace_c_modular_multiply,
    modular_exp,
    qsvt_step,
    qsvt,
    projector_controlled_phase,
    qsvt_inversion,
    allocate_num,
    qaoa_mixer_layer,
    qaoa_cost_layer,
    qaoa_layer,
    qaoa_init,
    qaoa_penalty,
    full_hea,
    swap_test,
    prepare_uniform_trimmed_state,
    prepare_uniform_interval_state,
    prepare_ghz_state,
    prepare_exponential_state,
    prepare_bell_state,
    inplace_prepare_int,
    prepare_int,
    switch,
    qct_qst_type1,
    qct_qst_type2,
    qct_type2,
    qst_type2,
    modular_increment,
    qft,
    _ctrl_x,
    _prepare_uniform_trimmed_state_step,
    _qct_d_operator,
    _qct_pi_operator,
    _check_msb,
    encode_in_angle,
    encode_on_bloch,
]

OPEN_LIBRARY_FUNCTIONS: list[NativeFunctionDefinition] = []


def load_open_library_implementations() -> None:
    OPEN_LIBRARY_FUNCTIONS.extend(
        [func.get_implementation() for func in OPEN_LIBRARY_UNPROCESSED_FUNCTIONS]
    )


OPEN_LIBRARY_GENERATIVE_FUNCTIONS: list[GenerativeQFunc] = []

OPEN_LIB_DECLS = [
    func.func_decl
    for func in OPEN_LIBRARY_GENERATIVE_FUNCTIONS + OPEN_LIBRARY_UNPROCESSED_FUNCTIONS
]

STD_QMOD_OPERATORS = [func.func_decl for func in (apply, permute)]

BUILTIN_FUNCTION_DECLARATIONS = {
    func_decl.name: func_decl
    for func_decl in STD_QMOD_OPERATORS + OPEN_LIB_DECLS + CORE_LIB_DECLS
}

__all__ = [
    "permute",
    "apply",
    "molecule_ucc",
    "molecule_hva",
    "molecule_hartree_fock",
    "fock_hamiltonian_ucc",
    "fock_hamiltonian_hva",
    "fock_hamiltonian_hartree_fock",
    "log_normal_finance",
    "gaussian_finance",
    "pauli_feature_map",
    "bloch_sphere_feature_map",
    "H",
    "X",
    "Y",
    "Z",
    "I",
    "S",
    "T",
    "SDG",
    "TDG",
    "PHASE",
    "RX",
    "RY",
    "RZ",
    "R",
    "RXX",
    "RYY",
    "RZZ",
    "CH",
    "CX",
    "CY",
    "CZ",
    "CRX",
    "CRY",
    "CRZ",
    "CPHASE",
    "SWAP",
    "IDENTITY",
    "prepare_state",
    "prepare_amplitudes",
    "unitary",
    "add",
    "modular_add",
    "integer_xor",
    "modular_add_constant",
    "real_xor_constant",
    "U",
    "CCX",
    "allocate",
    "free",
    "randomized_benchmarking",
    "inplace_prepare_state",
    "inplace_prepare_amplitudes",
    "single_pauli_exponent",
    "suzuki_trotter",
    "qdrift",
    "exponentiation_with_depth_constraint",
    "qpe_flexible",
    "qpe",
    "_single_pauli",
    "linear_pauli_rotations",
    "amplitude_estimation",
    "phase_oracle",
    "reflect_about_zero",
    "grover_diffuser",
    "grover_operator",
    "grover_search",
    "hadamard_transform",
    "apply_to_all",
    "qft_no_swap",
    "qft_space_add_const",
    "cc_modular_add",
    "c_modular_multiply",
    "multiswap",
    "inplace_c_modular_multiply",
    "modular_exp",
    "qsvt_step",
    "qsvt",
    "projector_controlled_phase",
    "qsvt_inversion",
    "allocate_num",
    "qaoa_mixer_layer",
    "qaoa_cost_layer",
    "qaoa_layer",
    "qaoa_init",
    "qaoa_penalty",
    "full_hea",
    "swap_test",
    "prepare_uniform_trimmed_state",
    "prepare_uniform_interval_state",
    "prepare_ghz_state",
    "prepare_exponential_state",
    "prepare_bell_state",
    "inplace_prepare_int",
    "prepare_int",
    "switch",
    "qct_qst_type1",
    "qct_qst_type2",
    "qct_type2",
    "qst_type2",
    "modular_increment",
    "qft",
    "encode_in_angle",
    "encode_on_bloch",
]
