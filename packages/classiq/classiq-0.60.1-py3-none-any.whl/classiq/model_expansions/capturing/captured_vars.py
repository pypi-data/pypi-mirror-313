import dataclasses
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from classiq.interface.enum_utils import StrEnum
from classiq.interface.exceptions import (
    ClassiqExpansionError,
    ClassiqInternalExpansionError,
)
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.model.handle_binding import HandleBinding, NestedHandleBinding
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_call import ArgValue
from classiq.interface.model.quantum_type import QuantumType

from classiq.model_expansions.capturing.mangling_utils import (
    demangle_handle,
    mangle_captured_var_name,
)
from classiq.model_expansions.scope import QuantumSymbol
from classiq.model_expansions.transformers.var_splitter import SymbolPart, SymbolParts

if TYPE_CHECKING:
    from classiq.model_expansions.closure import FunctionClosure


class PortDirection(StrEnum):
    Input = "input"
    Inout = "inout"
    Output = "output"
    Outin = "outin"

    def negate(self) -> "PortDirection":
        if self == PortDirection.Input:
            return PortDirection.Output
        if self == PortDirection.Output:
            return PortDirection.Input
        return self

    @staticmethod
    def load(direction: PortDeclarationDirection) -> "PortDirection":
        if direction == PortDeclarationDirection.Input:
            return PortDirection.Input
        if direction == PortDeclarationDirection.Output:
            return PortDirection.Output
        if direction == PortDeclarationDirection.Inout:
            return PortDirection.Inout
        raise ClassiqInternalExpansionError

    def dump(self) -> PortDeclarationDirection:
        if self == PortDirection.Input:
            return PortDeclarationDirection.Input
        if self == PortDirection.Output:
            return PortDeclarationDirection.Output
        if self == PortDirection.Inout:
            return PortDeclarationDirection.Inout
        raise ClassiqInternalExpansionError


@dataclass(frozen=True)
class _CapturedHandle:
    handle: HandleBinding
    quantum_type: QuantumType
    defining_function: "FunctionClosure"
    direction: PortDirection
    is_propagated: bool

    @property
    def mangled_name(self) -> str:
        return mangle_captured_var_name(self.handle.identifier, self.defining_function)

    @property
    def port(self) -> PortDeclaration:
        return PortDeclaration(
            name=self.mangled_name,
            quantum_type=self.quantum_type,
            direction=self.direction.dump(),
        )

    def is_same_var(self, other: "_CapturedHandle") -> bool:
        return self.handle.name == other.handle.name and _same_closure(
            self.defining_function, other.defining_function
        )

    def change_direction(self, new_direction: PortDirection) -> "_CapturedHandle":
        return dataclasses.replace(self, direction=new_direction)

    def set_propagated(self) -> "_CapturedHandle":
        return dataclasses.replace(self, is_propagated=True)

    def update_propagation(
        self, other_captured_handle: "_CapturedHandle"
    ) -> "_CapturedHandle":
        if self.is_propagated and not other_captured_handle.is_propagated:
            return dataclasses.replace(self, is_propagated=False)
        return self


@dataclass
class CapturedVars:
    _captured_handles: list[_CapturedHandle] = field(default_factory=list)

    def capture_handle(
        self,
        handle: HandleBinding,
        quantum_type: QuantumType,
        defining_function: "FunctionClosure",
        direction: PortDeclarationDirection,
    ) -> None:
        self._capture_handle(
            _CapturedHandle(
                handle=handle,
                quantum_type=quantum_type,
                defining_function=defining_function,
                direction=PortDirection.load(direction),
                is_propagated=False,
            )
        )

    def _capture_handle(self, captured_handle: _CapturedHandle) -> None:
        if (
            isinstance(captured_handle.handle, NestedHandleBinding)
            and captured_handle.direction != PortDirection.Inout
        ):
            raise ClassiqInternalExpansionError("Captured nested handles must be inout")

        new_captured_handles = []
        for existing_captured_handle in self._captured_handles:
            if not existing_captured_handle.is_same_var(captured_handle):
                new_captured_handles.append(existing_captured_handle)
                continue
            captured_handle = captured_handle.update_propagation(
                existing_captured_handle
            )
            if existing_captured_handle.handle == captured_handle.handle:
                captured_handle = self._conjugate_direction(
                    existing_captured_handle, captured_handle
                )
            elif captured_handle.handle in existing_captured_handle.handle:
                if existing_captured_handle.direction in (
                    PortDirection.Input,
                    PortDirection.Outin,
                ):
                    raise ClassiqInternalExpansionError(
                        "Captured handle is already freed"
                    )
                captured_handle = existing_captured_handle
            elif existing_captured_handle.handle in captured_handle.handle:
                if captured_handle.direction in (
                    PortDirection.Output,
                    PortDirection.Outin,
                ):
                    raise ClassiqInternalExpansionError(
                        "Captured handle is already allocated"
                    )
            else:
                new_captured_handles.append(existing_captured_handle)
        new_captured_handles.append(captured_handle)
        self._captured_handles = new_captured_handles

    def _conjugate_direction(
        self,
        existing_captured_handle: _CapturedHandle,
        captured_handle: _CapturedHandle,
    ) -> _CapturedHandle:
        if existing_captured_handle.direction == PortDirection.Input:
            if captured_handle.direction == PortDirection.Output:
                return captured_handle.change_direction(PortDirection.Inout)
            if captured_handle.direction == PortDirection.Outin:
                return captured_handle.change_direction(PortDirection.Input)
            raise ClassiqInternalExpansionError("Captured handle is already freed")
        if existing_captured_handle.direction == PortDirection.Output:
            if captured_handle.direction == PortDirection.Input:
                return captured_handle.change_direction(PortDirection.Outin)
            if captured_handle.direction in (
                PortDirection.Output,
                PortDirection.Outin,
            ):
                raise ClassiqInternalExpansionError(
                    "Captured handle is already allocated"
                )
            return captured_handle.change_direction(PortDirection.Output)
        if existing_captured_handle.direction == PortDirection.Inout:
            if captured_handle.direction in (
                PortDirection.Output,
                PortDirection.Outin,
            ):
                raise ClassiqInternalExpansionError(
                    "Captured handle is already allocated"
                )
        elif captured_handle.direction in (
            PortDirection.Input,
            PortDirection.Inout,
        ):
            raise ClassiqInternalExpansionError("Captured handle is already freed")
        return captured_handle

    def update(self, other_captured_vars: "CapturedVars") -> None:
        for captured_handle in other_captured_vars._captured_handles:
            self._capture_handle(captured_handle)

    def negate(self) -> "CapturedVars":
        return CapturedVars(
            _captured_handles=[
                captured_handle.change_direction(captured_handle.direction.negate())
                for captured_handle in self._captured_handles
            ]
        )

    def filter(self, current_function: "FunctionClosure") -> "CapturedVars":
        return CapturedVars(
            _captured_handles=[
                captured_handle
                for captured_handle in self._captured_handles
                if not _same_closure(
                    captured_handle.defining_function, current_function
                )
            ]
        )

    def set_propagated(self) -> "CapturedVars":
        return CapturedVars(
            _captured_handles=[
                captured_handle.set_propagated()
                for captured_handle in self._captured_handles
            ]
        )

    def get_captured_ports(self) -> list[PortDeclaration]:
        return [captured_handle.port for captured_handle in self._captured_handles]

    def get_captured_args(
        self, current_function: "FunctionClosure"
    ) -> list[HandleBinding]:
        return [
            (
                captured_handle.handle
                if _same_closure(current_function, captured_handle.defining_function)
                else HandleBinding(name=captured_handle.mangled_name)
            )
            for captured_handle in self._captured_handles
        ]

    def get_captured_mapping(self) -> SymbolParts:
        return {
            QuantumSymbol(
                handle=captured_handle.handle,
                quantum_type=captured_handle.quantum_type,
            ): [
                SymbolPart(
                    source_handle=captured_handle.handle,
                    target_var_name=captured_handle.mangled_name,
                    target_var_type=captured_handle.quantum_type,
                )
            ]
            for captured_handle in self._captured_handles
            if not captured_handle.is_propagated
        }

    @contextmanager
    def freeze(self) -> Iterator[None]:
        previous = self._captured_handles
        yield
        self._captured_handles = previous


def _same_closure(closure_1: "FunctionClosure", closure_2: "FunctionClosure") -> bool:
    return closure_1.depth == closure_2.depth


def validate_args_are_not_propagated(
    args: Sequence[ArgValue], captured_vars: Sequence[HandleBinding]
) -> None:
    if not captured_vars:
        return
    captured_handles = {demangle_handle(handle) for handle in captured_vars}
    arg_handles = {
        demangle_handle(arg) for arg in args if isinstance(arg, HandleBinding)
    }
    if any(
        arg_handle.overlaps(captured_handle)
        for arg_handle in arg_handles
        for captured_handle in captured_handles
    ):
        captured_handles_str = {str(handle) for handle in captured_handles}
        arg_handles_str = {str(handle) for handle in arg_handles}
        vars_msg = f"Explicitly passed variables: {arg_handles_str}, captured variables: {captured_handles_str}"
        raise ClassiqExpansionError(
            f"Cannot capture variables that are explicitly passed as arguments. "
            f"{vars_msg}"
        )


def validate_captured_directions(captured_vars: CapturedVars) -> None:
    captured_inputs = [
        captured_handle.handle.name
        for captured_handle in captured_vars._captured_handles
        if captured_handle.direction == PortDirection.Input
    ]
    captured_outputs = [
        captured_handle.handle.name
        for captured_handle in captured_vars._captured_handles
        if captured_handle.direction == PortDirection.Output
    ]
    if len(captured_inputs) > 0:
        raise ClassiqExpansionError(
            f"Captured quantum variables {captured_inputs!r} cannot be used as inputs"
        )
    if len(captured_outputs) > 0:
        raise ClassiqExpansionError(
            f"Captured quantum variables {captured_outputs!r} cannot be used as outputs"
        )
