from typing import Annotated, Union

from pydantic import Field

from classiq.interface.generator.functions.classical_type import (
    Bool,
    ClassicalArray,
    ClassicalList,
    Estimation,
    Histogram,
    Integer,
    IQAERes,
    Real,
    StructMetaType,
    VQEResult,
)
from classiq.interface.generator.functions.type_name import Enum, TypeName
from classiq.interface.generator.types.qstruct_declaration import QStructDeclaration
from classiq.interface.model.quantum_type import (
    QuantumBit,
    QuantumBitvector,
    QuantumNumeric,
    RegisterQuantumType,
)

ConcreteClassicalType = Annotated[
    Union[
        Integer,
        Real,
        Bool,
        ClassicalList,
        StructMetaType,
        TypeName,
        ClassicalArray,
        VQEResult,
        Histogram,
        Estimation,
        IQAERes,
    ],
    Field(discriminator="kind"),
]
ClassicalList.model_rebuild()
ClassicalArray.model_rebuild()

NativePythonClassicalTypes = (int, float, bool, list)
PythonClassicalPydanticTypes = (Enum,)

ConcreteQuantumType = Annotated[
    Union[QuantumBit, QuantumBitvector, QuantumNumeric, TypeName],
    Field(discriminator="kind", default_factory=QuantumBitvector),
]
QuantumBitvector.model_rebuild()
TypeName.model_rebuild()
QStructDeclaration.model_rebuild()
RegisterQuantumType.model_rebuild()
