from typing import Literal, Union

from classiq.interface.enum_utils import StrEnum


class AnalyzerProviderVendor(StrEnum):
    IBM_QUANTUM = "IBM Quantum"
    AZURE_QUANTUM = "Azure Quantum"
    AMAZON_BRAKET = "Amazon Braket"


class ProviderVendor(StrEnum):
    CLASSIQ = "Classiq"
    IBM_QUANTUM = "IBM Quantum"
    AZURE_QUANTUM = "Azure Quantum"
    AMAZON_BRAKET = "Amazon Braket"
    IONQ = "IonQ"
    GOOGLE = "Google"
    ALICE_AND_BOB = "Alice & Bob"
    OQC = "OQC"
    INTEL = "Intel"
    AQT = "AQT"
    IQCC = "IQCC"


class ProviderTypeVendor:
    CLASSIQ = Literal[ProviderVendor.CLASSIQ]
    IBM_QUANTUM = Literal[ProviderVendor.IBM_QUANTUM]
    AZURE_QUANTUM = Literal[ProviderVendor.AZURE_QUANTUM]
    AMAZON_BRAKET = Literal[ProviderVendor.AMAZON_BRAKET]
    IONQ = Literal[ProviderVendor.IONQ]
    GOOGLE = Literal[ProviderVendor.GOOGLE]
    ALICE_BOB = Literal[ProviderVendor.ALICE_AND_BOB]
    OQC = Literal[ProviderVendor.OQC]
    INTEL = Literal[ProviderVendor.INTEL]
    AQT = Literal[ProviderVendor.AQT]
    IQCC = Literal[ProviderVendor.IQCC]


class ClassiqSimulatorBackendNames(StrEnum):
    """

    The simulator backends available in the Classiq provider.

    """

    SIMULATOR = "simulator"
    SIMULATOR_STATEVECTOR = "simulator_statevector"
    SIMULATOR_DENSITY_MATRIX = "simulator_density_matrix"
    SIMULATOR_MATRIX_PRODUCT_STATE = "simulator_matrix_product_state"


class IonqBackendNames(StrEnum):
    """
    IonQ backend names which Classiq Supports running on.
    """

    SIMULATOR = "simulator"
    HARMONY = "qpu.harmony"
    ARIA_1 = "qpu.aria-1"
    ARIA_2 = "qpu.aria-2"
    FORTE_1 = "qpu.forte-1"


class AzureQuantumBackendNames(StrEnum):
    """
    AzureQuantum backend names which Classiq Supports running on.
    """

    IONQ_ARIA_1 = "ionq.qpu.aria-1"
    IONQ_ARIA_2 = "ionq.qpu.aria-2"
    IONQ_QPU = "ionq.qpu"
    IONQ_QPU_FORTE = "ionq.qpu.forte-1"
    IONQ_SIMULATOR = "ionq.simulator"
    MICROSOFT_ESTIMATOR = "microsoft.estimator"
    MICROSOFT_FULLSTATE_SIMULATOR = "microsoft.simulator.fullstate"
    RIGETTI_SIMULATOR = "rigetti.sim.qvm"
    RIGETTI_ANKAA2 = "rigetti.qpu.ankaa-2"
    RIGETTI_ANKAA9 = "rigetti.qpu.ankaa-9q-1"
    QCI_MACHINE1 = "qci.machine1"
    QCI_NOISY_SIMULATOR = "qci.simulator.noisy"
    QCI_SIMULATOR = "qci.simulator"
    QUANTINUUM_API_VALIDATOR1_1 = "quantinuum.sim.h1-1sc"
    QUANTINUUM_API_VALIDATOR1_2 = "quantinuum.sim.h1-2sc"
    QUANTINUUM_API_VALIDATOR2_1 = "quantinuum.sim.h2-1sc"
    QUANTINUUM_QPU1_1 = "quantinuum.qpu.h1-1"
    QUANTINUUM_QPU1_2 = "quantinuum.qpu.h1-2"
    QUANTINUUM_SIMULATOR1_1 = "quantinuum.sim.h1-1e"
    QUANTINUUM_SIMULATOR1_2 = "quantinuum.sim.h1-2e"
    QUANTINUUM_QPU2 = "quantinuum.qpu.h2-1"
    QUANTINUUM_SIMULATOR2 = "quantinuum.sim.h2-1e"


class AmazonBraketBackendNames(StrEnum):
    """
    Amazon Braket backend names which Classiq Supports running on.
    """

    AMAZON_BRAKET_SV1 = "SV1"
    AMAZON_BRAKET_TN1 = "TN1"
    AMAZON_BRAKET_DM1 = "dm1"
    AMAZON_BRAKET_ASPEN_11 = "Aspen-11"
    AMAZON_BRAKET_M_1 = "Aspen-M-1"
    AMAZON_BRAKET_IONQ = "IonQ Device"
    AMAZON_BRAKET_LUCY = "Lucy"


# The IBM devices were taken from:
#   from qiskit.providers.fake_provider import FakeProvider
#   provider = FakeProvider()
#   backends_list = provider.backends()
#   # Using _normalize_backend_name from `ibm_hardware_graphs.py`
#   the_devices = [_normalize_backend_name(str(backend)) for backend in backends_list]
class IBMQHardwareNames(StrEnum):
    """
    IBM backend names which Classiq Supports running on.
    """

    ALMADEN = "Almaden"
    ARMONK = "Armonk"
    ATHENS = "Athens"
    BELEM = "Belem"
    BOEBLINGEN = "Boeblingen"
    BOGOTA = "Bogota"
    BROOKLYN = "Brooklyn"
    BURLINGTON = "Burlington"
    CAIRO = "Cairo"
    CAMBRIDGE = "Cambridge"
    # CAMBRIDGEALTERNATIVEBASIS = "CambridgeAlternativeBasis"
    CASABLANCA = "Casablanca"
    ESSEX = "Essex"
    GUADALUPE = "Guadalupe"
    HANOI = "Hanoi"
    JAKARTA = "Jakarta"
    JOHANNESBURG = "Johannesburg"
    KOLKATA = "Kolkata"
    LAGOS = "Lagos"
    LIMA = "Lima"
    LONDON = "London"
    MANHATTAN = "Manhattan"
    MANILA = "Manila"
    MELBOURNE = "Melbourne"
    MONTREAL = "Montreal"
    MUMBAI = "Mumbai"
    NAIROBI = "Nairobi"
    OPENPULSE2Q = "OpenPulse_2Q"
    OPENPULSE3Q = "OpenPulse_3Q"
    OURENSE = "Ourense"
    PARIS = "Paris"
    POUGHKEEPSIE = "Poughkeepsie"
    QASM_SIMULATOR = "qasm_simulator"
    QUITO = "Quito"
    ROCHESTER = "Rochester"
    ROME = "Rome"
    RUESCHLIKON = "Rueschlikon"
    SANTIAGO = "Santiago"
    SINGAPORE = "Singapore"
    SYDNEY = "Sydney"
    TENERIFE = "Tenerife"
    TOKYO = "Tokyo"
    TORONTO = "Toronto"
    VALENCIA = "Valencia"
    VIGO = "Vigo"
    WASHINGTON = "Washington"
    YORKTOWN = "Yorktown"


class ClassiqNvidiaBackendNames(StrEnum):
    """
    Classiq's Nvidia simulator backend names.
    """

    SIMULATOR = "nvidia_state_vector_simulator"


class IntelBackendNames(StrEnum):
    SIMULATOR = "intel_qsdk_simulator"


AllClassiqBackendNames = Union[ClassiqSimulatorBackendNames, ClassiqNvidiaBackendNames]


class GoogleNvidiaBackendNames(StrEnum):
    """
    Google backend names which Classiq Supports running on.
    """

    CUQUANTUM = "cuquantum"


class AliceBobBackendNames(StrEnum):
    """
    Alice & Bob backend names which Classiq Supports running on.
    """

    PERFECT_QUBITS = "PERFECT_QUBITS"
    LOGICAL_TARGET = "LOGICAL_TARGET"
    LOGICAL_EARLY = "LOGICAL_EARLY"
    TRANSMONS = "TRANSMONS"


class OQCBackendNames(StrEnum):
    """
    OQC backend names which Classiq Supports running on.
    """

    LUCY = "Lucy"


EXACT_SIMULATORS = {
    IonqBackendNames.SIMULATOR,
    AzureQuantumBackendNames.IONQ_SIMULATOR,
    AzureQuantumBackendNames.MICROSOFT_FULLSTATE_SIMULATOR,
    AmazonBraketBackendNames.AMAZON_BRAKET_SV1,
    AmazonBraketBackendNames.AMAZON_BRAKET_TN1,
    AmazonBraketBackendNames.AMAZON_BRAKET_DM1,
    *ClassiqSimulatorBackendNames,
    *IntelBackendNames,
    *ClassiqNvidiaBackendNames,
}

AllIBMQBackendNames = IBMQHardwareNames

AllBackendsNameByVendor = Union[
    AllIBMQBackendNames,
    AzureQuantumBackendNames,
    AmazonBraketBackendNames,
    IonqBackendNames,
    IntelBackendNames,
    ClassiqNvidiaBackendNames,
    AliceBobBackendNames,
    OQCBackendNames,
]

AllBackendsNameEnums = [
    IBMQHardwareNames,
    AzureQuantumBackendNames,
    AmazonBraketBackendNames,
    IonqBackendNames,
    AliceBobBackendNames,
    IntelBackendNames,
    ClassiqNvidiaBackendNames,
    OQCBackendNames,
]
