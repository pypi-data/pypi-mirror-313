from typing import TYPE_CHECKING, Any, Literal, Union

import pydantic
from pydantic import ConfigDict
from sympy import IndexedBase, Symbol

from classiq.interface.ast_node import HashableASTNode
from classiq.interface.generator.expressions.expression_types import RuntimeExpression
from classiq.interface.helpers.pydantic_model_helpers import values_with_discriminator

if TYPE_CHECKING:
    from classiq.interface.generator.functions.concrete_types import (
        ConcreteClassicalType,
    )

CLASSICAL_ATTRIBUTES = {"len", "size", "is_signed", "fraction_digits"}

NamedSymbol = Union[IndexedBase, Symbol]


class ClassicalType(HashableASTNode):
    def as_symbolic(self, name: str) -> Union[NamedSymbol, list[NamedSymbol]]:
        return Symbol(name)

    model_config = ConfigDict(extra="forbid")

    def __str__(self) -> str:
        return str(type(self).__name__)


class Integer(ClassicalType):
    kind: Literal["int"]

    def as_symbolic(self, name: str) -> Symbol:
        return Symbol(name, integer=True)

    @pydantic.model_validator(mode="before")
    @classmethod
    def _set_kind(cls, values: Any) -> dict[str, Any]:
        return values_with_discriminator(values, "kind", "int")


class Real(ClassicalType):
    kind: Literal["real"]

    def as_symbolic(self, name: str) -> Symbol:
        return Symbol(name, real=True)

    @pydantic.model_validator(mode="before")
    @classmethod
    def _set_kind(cls, values: Any) -> dict[str, Any]:
        return values_with_discriminator(values, "kind", "real")


class Bool(ClassicalType):
    kind: Literal["bool"]

    @pydantic.model_validator(mode="before")
    @classmethod
    def _set_kind(cls, values: Any) -> dict[str, Any]:
        return values_with_discriminator(values, "kind", "bool")


class ClassicalList(ClassicalType):
    kind: Literal["list"]
    element_type: "ConcreteClassicalType"

    def as_symbolic(self, name: str) -> Symbol:
        return IndexedBase(name)

    @pydantic.model_validator(mode="before")
    @classmethod
    def _set_kind(cls, values: Any) -> dict[str, Any]:
        return values_with_discriminator(values, "kind", "list")


class StructMetaType(ClassicalType):
    kind: Literal["type_proxy"]

    @pydantic.model_validator(mode="before")
    @classmethod
    def _set_kind(cls, values: Any) -> dict[str, Any]:
        return values_with_discriminator(values, "kind", "type_proxy")


class ClassicalArray(ClassicalType):
    kind: Literal["array"]
    element_type: "ConcreteClassicalType"
    size: pydantic.PositiveInt

    def as_symbolic(self, name: str) -> list:
        return [self.element_type.as_symbolic(f"{name}_{i}") for i in range(self.size)]

    @pydantic.model_validator(mode="before")
    @classmethod
    def _set_kind(cls, values: Any) -> dict[str, Any]:
        return values_with_discriminator(values, "kind", "array")


class OpaqueHandle(ClassicalType):
    pass


class VQEResult(OpaqueHandle):
    kind: Literal["vqe_result"]

    @pydantic.model_validator(mode="before")
    @classmethod
    def _set_kind(cls, values: Any) -> dict[str, Any]:
        return values_with_discriminator(values, "kind", "vqe_result")


class Histogram(OpaqueHandle):
    kind: Literal["histogram"]

    @pydantic.model_validator(mode="before")
    @classmethod
    def _set_kind(cls, values: Any) -> dict[str, Any]:
        return values_with_discriminator(values, "kind", "histogram")


class Estimation(OpaqueHandle):
    kind: Literal["estimation_result"]

    @pydantic.model_validator(mode="before")
    @classmethod
    def _set_kind(cls, values: Any) -> dict[str, Any]:
        return values_with_discriminator(values, "kind", "estimation_result")


class IQAERes(OpaqueHandle):
    kind: Literal["iqae_result"]

    @pydantic.model_validator(mode="before")
    @classmethod
    def _set_kind(cls, values: Any) -> dict[str, Any]:
        return values_with_discriminator(values, "kind", "iqae_result")


def as_symbolic(symbols: dict[str, ClassicalType]) -> dict[str, RuntimeExpression]:
    return {
        param_name: param_type.as_symbolic(param_name)
        for param_name, param_type in symbols.items()
    }


class QmodPyObject:
    pass
