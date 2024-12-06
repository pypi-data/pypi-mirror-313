from collections.abc import Sequence
from itertools import chain
from typing import TYPE_CHECKING, Any, Union

import pydantic
from pydantic import ConfigDict, Field
from typing_extensions import Self

from classiq.interface.ast_node import ASTNode
from classiq.interface.generator.expressions.expression import Expression

HANDLE_ID_SEPARATOR = "___"


class HandleBinding(ASTNode):
    name: str = Field(default=None)
    model_config = ConfigDict(frozen=True, extra="forbid")

    def __str__(self) -> str:
        return self.name

    @property
    def qmod_expr(self) -> str:
        return self.name

    def is_bindable(self) -> bool:
        return True

    @property
    def identifier(self) -> str:
        return self.name

    def collapse(self) -> "HandleBinding":
        return self

    def prefixes(self) -> Sequence["HandleBinding"]:
        """
        Split the handle into prefixes:
        a.b[0].c --> [a, a.b, a.b[0], a.b[0].c]
        """
        return [self]

    def _tail_overlaps(self, other_handle: "HandleBinding") -> bool:
        return self.name == other_handle.name

    def overlaps(self, other_handle: "HandleBinding") -> bool:
        self_prefixes = self.collapse().prefixes()
        other_prefixes = other_handle.collapse().prefixes()
        return all(
            self_prefix._tail_overlaps(other_prefix)
            for self_prefix, other_prefix in zip(self_prefixes, other_prefixes)
        )

    def rename(self, name: str) -> Self:
        return self.model_copy(update=dict(name=name))

    def replace_prefix(
        self, prefix: "HandleBinding", replacement: "HandleBinding"
    ) -> "HandleBinding":
        if self == prefix:
            return replacement
        return self

    def __contains__(self, other_handle: "HandleBinding") -> bool:
        return self.collapse() in other_handle.collapse().prefixes()


class NestedHandleBinding(HandleBinding):
    base_handle: "ConcreteHandleBinding"

    @pydantic.model_validator(mode="before")
    @classmethod
    def _set_name(cls, values: Any) -> dict[str, Any]:
        if isinstance(values, dict):
            orig = values
            while "base_handle" in dict(values):
                values = dict(values)["base_handle"]
            orig["name"] = dict(values).get("name")
            return orig
        if isinstance(values, NestedHandleBinding):
            values.name = values.base_handle.name
            return values.model_dump()
        return values

    def is_bindable(self) -> bool:
        return False

    def prefixes(self) -> Sequence["HandleBinding"]:
        return list(chain.from_iterable([self.base_handle.prefixes(), [self]]))

    def rename(self, name: str) -> Self:
        return self.model_copy(
            update=dict(name=name, base_handle=self.base_handle.rename(name))
        )

    def replace_prefix(
        self, prefix: HandleBinding, replacement: HandleBinding
    ) -> HandleBinding:
        if self == prefix:
            return replacement
        new_base_handle = self.base_handle.replace_prefix(prefix, replacement)
        if new_base_handle is not self.base_handle:
            return self.model_copy(
                update=dict(name=new_base_handle.name, base_handle=new_base_handle)
            )
        return self


class SubscriptHandleBinding(NestedHandleBinding):
    index: Expression
    model_config = ConfigDict(frozen=True, extra="forbid")

    def __str__(self) -> str:
        return f"{self.base_handle}[{self.index}]"

    @property
    def qmod_expr(self) -> str:
        return f"{self.base_handle.qmod_expr}[{self.index}]"

    @property
    def identifier(self) -> str:
        return f"{self.base_handle.identifier}{HANDLE_ID_SEPARATOR}{self.index}"

    def collapse(self) -> HandleBinding:
        if isinstance(self.base_handle, SlicedHandleBinding):
            return SubscriptHandleBinding(
                base_handle=self.base_handle.base_handle,
                index=self._get_collapsed_index(),
            ).collapse()
        return SubscriptHandleBinding(
            base_handle=self.base_handle.collapse(),
            index=self.index,
        )

    def _get_collapsed_index(self) -> Expression:
        if TYPE_CHECKING:
            assert isinstance(self.base_handle, SlicedHandleBinding)
        if self.index.is_evaluated() and self.base_handle.start.is_evaluated():
            return Expression(
                expr=str(
                    self.base_handle.start.to_int_value() + self.index.to_int_value()
                )
            )
        return Expression(expr=f"({self.base_handle.start})+({self.index})")

    def _tail_overlaps(self, other_handle: "HandleBinding") -> bool:
        if isinstance(other_handle, SubscriptHandleBinding):
            return self.index == other_handle.index
        if (
            isinstance(other_handle, SlicedHandleBinding)
            and self.index.is_evaluated()
            and other_handle.start.is_evaluated()
            and other_handle.end.is_evaluated()
        ):
            return (
                other_handle.start.to_int_value()
                <= self.index.to_int_value()
                < other_handle.end.to_int_value()
            )
        return False


class SlicedHandleBinding(NestedHandleBinding):
    start: Expression
    end: Expression
    model_config = ConfigDict(frozen=True, extra="forbid")

    def __str__(self) -> str:
        return f"{self.base_handle}[{self.start}:{self.end}]"

    @property
    def qmod_expr(self) -> str:
        return f"{self.base_handle.qmod_expr}[{self.start}:{self.end}]"

    @property
    def identifier(self) -> str:
        return (
            f"{self.base_handle.identifier}{HANDLE_ID_SEPARATOR}{self.start}_{self.end}"
        )

    def collapse(self) -> HandleBinding:
        if isinstance(self.base_handle, SlicedHandleBinding):
            return SlicedHandleBinding(
                base_handle=self.base_handle.base_handle,
                start=self._get_collapsed_start(),
                end=self._get_collapsed_stop(),
            ).collapse()
        return SlicedHandleBinding(
            base_handle=self.base_handle.collapse(),
            start=self.start,
            end=self.end,
        )

    def _tail_overlaps(self, other_handle: "HandleBinding") -> bool:
        if not self.start.is_evaluated() or not self.end.is_evaluated():
            return False
        start = self.start.to_int_value()
        end = self.end.to_int_value()
        if (
            isinstance(other_handle, SubscriptHandleBinding)
            and other_handle.index.is_evaluated()
        ):
            return start <= other_handle.index.to_int_value() < end
        if (
            isinstance(other_handle, SlicedHandleBinding)
            and other_handle.start.is_evaluated()
            and other_handle.end.is_evaluated()
        ):
            other_start = other_handle.start.to_int_value()
            other_end = other_handle.end.to_int_value()
            return start <= other_start < end or other_start <= start < other_end
        return False

    def _get_collapsed_start(self) -> Expression:
        if TYPE_CHECKING:
            assert isinstance(self.base_handle, SlicedHandleBinding)
        if self.start.is_evaluated() and self.base_handle.start.is_evaluated():
            return Expression(
                expr=str(
                    self.base_handle.start.to_int_value() + self.start.to_int_value()
                )
            )
        return Expression(expr=f"({self.base_handle.start})+({self.start})")

    def _get_collapsed_stop(self) -> Expression:
        if TYPE_CHECKING:
            assert isinstance(self.base_handle, SlicedHandleBinding)
        if self.end.is_evaluated() and self.base_handle.end.is_evaluated():
            return Expression(
                expr=str(self.base_handle.end.to_int_value() - self.end.to_int_value())
            )
        return Expression(expr=f"({self.base_handle.end})-({self.end})")


class FieldHandleBinding(NestedHandleBinding):
    field: str
    model_config = ConfigDict(frozen=True, extra="forbid")

    def __str__(self) -> str:
        return f"{self.base_handle}.{self.field}"

    @property
    def qmod_expr(self) -> str:
        return f"get_field({self.base_handle.qmod_expr}, '{self.field}')"

    @property
    def identifier(self) -> str:
        return f"{self.base_handle.identifier}{HANDLE_ID_SEPARATOR}{self.field}"

    def collapse(self) -> HandleBinding:
        return FieldHandleBinding(
            base_handle=self.base_handle.collapse(),
            field=self.field,
        )

    def _tail_overlaps(self, other_handle: "HandleBinding") -> bool:
        return (
            isinstance(other_handle, FieldHandleBinding)
            and self.field == other_handle.field
        )


ConcreteHandleBinding = Union[
    HandleBinding,
    SubscriptHandleBinding,
    SlicedHandleBinding,
    FieldHandleBinding,
]
SubscriptHandleBinding.model_rebuild()
SlicedHandleBinding.model_rebuild()
FieldHandleBinding.model_rebuild()
