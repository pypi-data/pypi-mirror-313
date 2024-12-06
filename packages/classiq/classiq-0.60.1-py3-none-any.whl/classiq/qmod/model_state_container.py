from classiq.interface.generator.constant import Constant
from classiq.interface.generator.types.compilation_metadata import CompilationMetadata
from classiq.interface.generator.types.enum_declaration import EnumDeclaration
from classiq.interface.generator.types.qstruct_declaration import QStructDeclaration
from classiq.interface.generator.types.struct_declaration import StructDeclaration
from classiq.interface.model.native_function_definition import (
    NativeFunctionDefinition,
)


class ModelStateContainer:
    enum_decls: dict[str, EnumDeclaration]
    type_decls: dict[str, StructDeclaration]
    qstruct_decls: dict[str, QStructDeclaration]
    native_defs: dict[str, NativeFunctionDefinition]
    constants: dict[str, Constant]
    functions_compilation_metadata: dict[str, CompilationMetadata]


QMODULE = ModelStateContainer()
