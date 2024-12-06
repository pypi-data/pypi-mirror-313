import ast
import functools
from dataclasses import is_dataclass
from enum import EnumMeta
from inspect import isclass
from typing import Any, Callable, Optional, get_origin

from classiq.interface.exceptions import ClassiqError
from classiq.interface.executor.execution_preferences import ExecutionPreferences
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.generator.model.constraints import Constraints
from classiq.interface.generator.model.preferences.preferences import Preferences
from classiq.interface.generator.types.compilation_metadata import CompilationMetadata
from classiq.interface.model.model import Model
from classiq.interface.model.native_function_definition import (
    NativeFunctionDefinition,
)
from classiq.interface.model.quantum_function_declaration import (
    NamedParamsQuantumFunctionDeclaration,
)

from classiq.qmod.classical_function import CFunc
from classiq.qmod.declaration_inferrer import infer_func_decl
from classiq.qmod.qmod_constant import QConstant
from classiq.qmod.qmod_parameter import CArray, CParam
from classiq.qmod.qmod_variable import QVar
from classiq.qmod.quantum_callable import QCallable, QCallableList
from classiq.qmod.quantum_expandable import QExpandable, QTerminalCallable
from classiq.qmod.utilities import mangle_keyword


class BaseQFunc(QExpandable):
    def __init__(
        self,
        py_callable: Callable,
        compilation_metadata: Optional[CompilationMetadata] = None,
    ) -> None:
        super().__init__(py_callable)
        self.compilation_metadata = compilation_metadata

    @property
    def func_decl(self) -> NamedParamsQuantumFunctionDeclaration:
        raise NotImplementedError

    @property
    def _has_inputs(self) -> bool:
        return any(
            port.direction == PortDeclarationDirection.Input
            for port in self.func_decl.port_declarations
        )

    def update_compilation_metadata(self, **kwargs: Any) -> None:
        if kwargs["should_synthesize_separately"] and self._has_inputs:
            raise ClassiqError("Can't synthesize separately a function with inputs")
        self.compilation_metadata = self._compilation_metadata.model_copy(update=kwargs)

    @property
    def _compilation_metadata(self) -> CompilationMetadata:
        if self.compilation_metadata is None:
            return CompilationMetadata()
        return self.compilation_metadata


class QFunc(BaseQFunc):
    FRAME_DEPTH = 2

    def __init__(
        self,
        py_callable: Callable,
        compilation_metadata: Optional[CompilationMetadata] = None,
    ) -> None:
        _validate_no_gen_params(py_callable.__annotations__)
        super().__init__(py_callable, compilation_metadata)
        functools.update_wrapper(self, py_callable)
        self.compilation_metadata: Optional[CompilationMetadata] = None

    @property
    def func_decl(self) -> NamedParamsQuantumFunctionDeclaration:
        return self._qmodule.native_defs.get(
            self._py_callable.__name__,
            infer_func_decl(self._py_callable, qmodule=self._qmodule),
        )

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        super().__call__(*args, **kwargs)
        self.expand()

    def create_model(
        self,
        constraints: Optional[Constraints] = None,
        execution_preferences: Optional[ExecutionPreferences] = None,
        preferences: Optional[Preferences] = None,
        classical_execution_function: Optional[CFunc] = None,
    ) -> Model:
        self._qmodule.enum_decls = dict()
        self._qmodule.type_decls = dict()
        self._qmodule.qstruct_decls = dict()
        self._qmodule.native_defs = dict()
        self._qmodule.constants = dict()
        self._qmodule.functions_compilation_metadata = dict()
        QConstant.set_current_model(self._qmodule)
        self.expand()
        model_extra_settings: list[tuple[str, Any]] = [
            ("constraints", constraints),
            ("execution_preferences", execution_preferences),
            ("preferences", preferences),
        ]
        if classical_execution_function is not None:
            self._add_constants_from_classical_code(classical_execution_function)
            model_extra_settings.append(
                ("classical_execution_code", classical_execution_function.code)
            )
        return Model(
            constants=list(self._qmodule.constants.values()),
            functions=list(self._qmodule.native_defs.values()),
            enums=list(self._qmodule.enum_decls.values()),
            types=list(self._qmodule.type_decls.values()),
            qstructs=list(self._qmodule.qstruct_decls.values()),
            functions_compilation_metadata=self._qmodule.functions_compilation_metadata,
            **{key: value for key, value in model_extra_settings if value},
        )

    def expand(self) -> None:
        if self.func_decl.name in self._qmodule.native_defs:
            return
        super().expand()
        self._qmodule.native_defs[self.func_decl.name] = NativeFunctionDefinition(
            **{**self.func_decl.model_dump(), **{"body": self.body}}
        )
        if self.compilation_metadata is not None:
            self._qmodule.functions_compilation_metadata[self.func_decl.name] = (
                self.compilation_metadata
            )

    def _add_constants_from_classical_code(
        self, classical_execution_function: CFunc
    ) -> None:
        # FIXME: https://classiq.atlassian.net/browse/CAD-18050
        # We use this visitor to add the constants that were used in the classical
        # execution code to the model. In the future, if we will have a better notion
        # of "QModule" and a "QConstant" will be a part of it then we may be able to
        # remove the handling of the QConstants from this visitor, but I think we will
        # need similar logic to allow using python variables in the classical execution
        # code
        class IdentifierVisitor(ast.NodeVisitor):
            def visit_Name(self, node: ast.Name) -> None:
                if (
                    node.id in classical_execution_function._caller_constants
                    and isinstance(
                        classical_execution_function._caller_constants[node.id],
                        QConstant,
                    )
                ):
                    classical_execution_function._caller_constants[
                        node.id
                    ].add_to_model()

        IdentifierVisitor().visit(ast.parse(classical_execution_function.code))


class ExternalQFunc(QTerminalCallable):
    _decl: NamedParamsQuantumFunctionDeclaration

    def __init__(self, py_callable: Callable) -> None:
        self._py_callable = py_callable
        decl = infer_func_decl(py_callable)

        py_callable.__annotations__.pop("return", None)
        if py_callable.__annotations__.keys() != {
            mangle_keyword(arg.name) for arg in decl.positional_arg_declarations
        }:
            raise ClassiqError(
                f"Parameter type hints for {py_callable.__name__!r} do not match imported declaration"
            )
        super().__init__(decl)
        functools.update_wrapper(self, py_callable)

    @property
    def func_decl(self) -> NamedParamsQuantumFunctionDeclaration:
        return self._decl

    def get_implementation(self) -> NativeFunctionDefinition:
        model = QFunc(self._py_callable).create_model()
        return [
            func for func in model.functions if func.name == self._py_callable.__name__
        ][0]


class GenerativeQFunc(BaseQFunc):
    def __init__(
        self,
        py_callable: Callable,
        func_decl: Optional[NamedParamsQuantumFunctionDeclaration] = None,
        compilation_metadata: Optional[CompilationMetadata] = None,
    ) -> None:
        super().__init__(py_callable, compilation_metadata)
        self._func_decl = func_decl

    @property
    def func_decl(self) -> NamedParamsQuantumFunctionDeclaration:
        if self._func_decl is None:
            self._func_decl = infer_func_decl(self._py_callable, self._qmodule)
        return self._func_decl


ILLEGAL_PARAM_ERROR = "Unsupported type hint '{annotation}' for argument '{name}'."


class IllegalParamsError(ClassiqError):
    _HINT = (
        "\nNote - QMOD functions can declare classical parameters using the type hints "
        "'CInt', 'CReal', 'CBool', and 'CArray'."
    )

    def __init__(self, message: str) -> None:
        super().__init__(message + self._HINT)


def _validate_no_gen_params(annotations: dict[str, Any]) -> None:
    _illegal_params = {
        name: annotation
        for name, annotation in annotations.items()
        if not (
            name == "return"
            or isclass(annotation)
            and issubclass(annotation, CParam)
            or isclass(annotation)
            and is_dataclass(annotation)
            or isclass(annotation)
            and isinstance(annotation, EnumMeta)
            or get_origin(annotation) is CArray
            or (get_origin(annotation) or annotation) is QCallable
            or (get_origin(annotation) or annotation) is QCallableList
            or QVar.from_type_hint(annotation) is not None
        )
    }
    if _illegal_params:
        raise IllegalParamsError(
            "\n".join(
                ILLEGAL_PARAM_ERROR.format(name=name, annotation=annotation)
                for name, annotation in _illegal_params.items()
            )
        )
