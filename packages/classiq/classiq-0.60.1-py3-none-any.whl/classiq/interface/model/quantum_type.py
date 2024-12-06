from typing import TYPE_CHECKING, Any, Literal, Optional

import pydantic
from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Self

from classiq.interface.ast_node import HashableASTNode
from classiq.interface.exceptions import ClassiqValueError
from classiq.interface.generator.arith.register_user_input import (
    RegisterArithmeticInfo,
    RegisterUserInput,
)
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.expressions.qmod_qarray_proxy import QmodQArrayProxy
from classiq.interface.generator.expressions.qmod_qscalar_proxy import (
    QmodQBitProxy,
    QmodQNumProxy,
    QmodQScalarProxy,
)
from classiq.interface.generator.expressions.qmod_sized_proxy import QmodSizedProxy
from classiq.interface.helpers.pydantic_model_helpers import values_with_discriminator
from classiq.interface.model.handle_binding import HandleBinding

if TYPE_CHECKING:
    from classiq.interface.generator.functions.concrete_types import ConcreteQuantumType


class QuantumType(HashableASTNode):
    model_config = ConfigDict(extra="forbid")

    _size_in_bits: Optional[int] = pydantic.PrivateAttr(default=None)

    def _update_size_in_bits_from_declaration(self) -> None:
        pass

    @property
    def size_in_bits(self) -> int:
        self._update_size_in_bits_from_declaration()
        if self._size_in_bits is None:
            raise ClassiqValueError("Trying to retrieve unknown size of quantum type")
        return self._size_in_bits

    @property
    def has_size_in_bits(self) -> bool:
        self._update_size_in_bits_from_declaration()
        return self._size_in_bits is not None

    def set_size_in_bits(self, val: int) -> None:
        self._size_in_bits = val

    def get_proxy(self, handle: "HandleBinding") -> QmodSizedProxy:
        return QmodSizedProxy(handle=handle, size=self.size_in_bits)

    @property
    def qmod_type_name(self) -> str:
        raise NotImplementedError

    @property
    def type_name(self) -> str:
        raise NotImplementedError


class QuantumScalar(QuantumType):
    def get_proxy(self, handle: "HandleBinding") -> QmodQScalarProxy:
        return QmodQScalarProxy(handle, size=self.size_in_bits)


class QuantumBit(QuantumScalar):
    kind: Literal["qbit"]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._size_in_bits = 1

    @pydantic.model_validator(mode="before")
    @classmethod
    def _set_kind(cls, values: Any) -> dict[str, Any]:
        return values_with_discriminator(values, "kind", "qbit")

    @property
    def qmod_type_name(self) -> str:
        return "QBit"

    def get_proxy(self, handle: "HandleBinding") -> QmodQBitProxy:
        return QmodQBitProxy(handle)

    @property
    def type_name(self) -> str:
        return "Quantum bit"


class QuantumBitvector(QuantumType):
    element_type: "ConcreteQuantumType" = Field(
        discriminator="kind", default_factory=QuantumBit
    )
    kind: Literal["qvec"]
    length: Optional[Expression] = Field(default=None)

    @pydantic.model_validator(mode="before")
    @classmethod
    def _set_kind(cls, values: Any) -> dict[str, Any]:
        return values_with_discriminator(values, "kind", "qvec")

    def _update_size_in_bits_from_declaration(self) -> None:
        self.element_type._update_size_in_bits_from_declaration()
        if self.element_type.has_size_in_bits and self.has_length:
            assert self.length is not None
            self._size_in_bits = (
                self.element_type.size_in_bits * self.length.to_int_value()
            )

    @property
    def has_length(self) -> bool:
        return self.length is not None and self.length.is_evaluated()

    @property
    def length_value(self) -> int:
        if not self.has_length:
            raise ClassiqValueError(
                "Tried to access unevaluated length of quantum array"
            )
        assert self.length is not None
        return self.length.to_int_value()

    def get_proxy(self, handle: "HandleBinding") -> QmodQArrayProxy:
        element_size = self.element_type.size_in_bits
        assert self.size_in_bits % element_size == 0
        return QmodQArrayProxy(
            handle,
            self.element_type,
            element_size,
            self.size_in_bits // element_size,
        )

    @property
    def qmod_type_name(self) -> str:
        element_type = [self.element_type.qmod_type_name]
        length = [self.length.expr] if self.length is not None else []
        return f"QArray[{', '.join(element_type + length)}]"

    @property
    def type_name(self) -> str:
        return "Quantum array"


class QuantumNumeric(QuantumScalar):
    kind: Literal["qnum"]

    size: Optional[Expression] = pydantic.Field(default=None)
    is_signed: Optional[Expression] = pydantic.Field(default=None)
    fraction_digits: Optional[Expression] = pydantic.Field(default=None)

    @pydantic.model_validator(mode="before")
    @classmethod
    def _set_kind(cls, values: Any) -> dict[str, Any]:
        return values_with_discriminator(values, "kind", "qnum")

    @pydantic.model_validator(mode="after")
    def _validate_fields(self) -> Self:
        has_sign = self.is_signed is not None
        has_fraction_digits = self.fraction_digits is not None
        if has_sign and not has_fraction_digits or not has_sign and has_fraction_digits:
            raise ClassiqValueError(
                "Assign neither or both of is_signed and fraction_digits"
            )
        return self

    @property
    def has_sign(self) -> bool:
        return self.is_signed is not None

    @property
    def sign_value(self) -> bool:
        return False if self.is_signed is None else self.is_signed.to_bool_value()

    @property
    def has_fraction_digits(self) -> bool:
        return self.fraction_digits is not None

    @property
    def fraction_digits_value(self) -> int:
        return (
            0 if self.fraction_digits is None else self.fraction_digits.to_int_value()
        )

    def _update_size_in_bits_from_declaration(self) -> None:
        if self.size is not None and self.size.is_evaluated():
            self._size_in_bits = self.size.to_int_value()

    def get_proxy(self, handle: "HandleBinding") -> QmodQNumProxy:
        return QmodQNumProxy(
            handle,
            size=self.size_in_bits,
            fraction_digits=self.fraction_digits_value,
            is_signed=self.sign_value,
        )

    @property
    def qmod_type_name(self) -> str:
        if (
            self.size is not None
            and self.is_signed is not None
            and self.fraction_digits is not None
        ):
            return f"QNum[{self.size.expr}, {self.is_signed.expr}, {self.fraction_digits.expr}]"
        return "QNum"

    @property
    def type_name(self) -> str:
        return "Quantum numeric"


class RegisterQuantumType(BaseModel):
    quantum_types: "ConcreteQuantumType"
    size: int = Field(default=1)

    @property
    def qmod_type_name(self) -> str:
        try:
            return self.quantum_types.qmod_type_name.split("[")[0]
        except AttributeError:
            return "default"


RegisterQuantumTypeDict = dict[str, RegisterQuantumType]


def register_info_to_quantum_type(reg_info: RegisterArithmeticInfo) -> QuantumNumeric:
    result = QuantumNumeric()
    result.set_size_in_bits(reg_info.size)
    result.is_signed = Expression(expr=str(reg_info.is_signed))
    result.fraction_digits = Expression(expr=str(reg_info.fraction_places))
    return result


UNRESOLVED_SIZE = 1000


def quantum_var_to_register(name: str, qtype: QuantumType) -> RegisterUserInput:
    if isinstance(qtype, QuantumNumeric):
        signed = qtype.sign_value
        fraction_places = qtype.fraction_digits_value
    else:
        signed = False
        fraction_places = 0
    return RegisterUserInput(
        name=name,
        size=qtype.size_in_bits if qtype.has_size_in_bits else UNRESOLVED_SIZE,
        is_signed=signed,
        fraction_places=fraction_places,
    )


def quantum_type_to_register_quantum_type(
    qtype: QuantumType, size: int
) -> RegisterQuantumType:
    return RegisterQuantumType(
        quantum_types=qtype,
        size=size,
    )
