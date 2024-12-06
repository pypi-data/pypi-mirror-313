from abc import ABC, abstractmethod
from enum import IntEnum
from typing import ClassVar, Generic, Optional, TypeVar

from classiq.interface.generator.expressions.handle_identifier import HandleIdentifier
from classiq.interface.generator.functions.classical_type import QmodPyObject
from classiq.interface.generator.types.enum_declaration import EnumDeclaration
from classiq.interface.generator.types.qstruct_declaration import QStructDeclaration
from classiq.interface.generator.types.struct_declaration import StructDeclaration

from classiq.qmod.builtins.enums import BUILTIN_ENUM_DECLARATIONS
from classiq.qmod.builtins.structs import BUILTIN_STRUCT_DECLARATIONS
from classiq.qmod.model_state_container import QMODULE

DeclarationType = TypeVar(
    "DeclarationType", EnumDeclaration, StructDeclaration, QStructDeclaration
)


class TypeTable(Generic[DeclarationType], ABC):
    def __init__(self, user_types: list[DeclarationType]) -> None:
        self._all_types: dict[str, DeclarationType] = self.builtins.copy()
        for t in user_types:
            assert t.name not in self._all_types  # FIXME: issue user error (CAD-7856)
            self._all_types[t.name] = t

    @property
    @abstractmethod
    def builtins(self) -> dict[str, DeclarationType]:
        pass

    def __getitem__(self, key: str) -> DeclarationType:
        return self._all_types[key]

    def __setitem__(self, key: str, value: DeclarationType) -> None:
        self._all_types[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self._all_types

    def all_types(self) -> dict[str, DeclarationType]:
        return self._all_types


class EnumTable(TypeTable[EnumDeclaration]):
    def __init__(self, user_types: list[EnumDeclaration]) -> None:
        super().__init__(user_types)

    @property
    def builtins(self) -> dict[str, EnumDeclaration]:
        return BUILTIN_ENUM_DECLARATIONS

    @property
    def enums(self) -> dict[str, IntEnum]:
        return {
            enum_decl.name: enum_decl.create_enum()
            for enum_decl in self.all_types().values()
        }


class StructTable(TypeTable[StructDeclaration]):
    @property
    def builtins(self) -> dict[str, StructDeclaration]:
        return BUILTIN_STRUCT_DECLARATIONS


class QStructTable(TypeTable[QStructDeclaration]):
    @property
    def builtins(self) -> dict[str, QStructDeclaration]:
        return {}


class SymbolTable:
    enum_table: ClassVar[EnumTable] = EnumTable([])
    type_table: ClassVar[StructTable] = StructTable([])
    qstruct_table: ClassVar[QStructTable] = QStructTable([])

    @classmethod
    def init_user_enums(cls, user_enums: list[EnumDeclaration]) -> None:
        cls.enum_table = EnumTable(user_enums)

    @classmethod
    def init_user_types(cls, user_types: list[StructDeclaration]) -> None:
        cls.type_table = StructTable(user_types)

    @classmethod
    def init_user_qstructs(cls, user_qstructs: list[QStructDeclaration]) -> None:
        cls.qstruct_table = QStructTable(user_qstructs)
        QMODULE.qstruct_decls = {
            qstruct_decl.name: qstruct_decl for qstruct_decl in user_qstructs
        }


class HandleTable:
    _handle_map: dict[HandleIdentifier, QmodPyObject] = {}

    @classmethod
    def get_handle_object(cls, hid: HandleIdentifier) -> Optional[QmodPyObject]:
        return cls._handle_map.get(hid)

    @classmethod
    def set_handle_object(cls, qmod_object: QmodPyObject) -> HandleIdentifier:
        hid = HandleIdentifier(id(qmod_object))
        cls._handle_map[hid] = qmod_object
        return hid
