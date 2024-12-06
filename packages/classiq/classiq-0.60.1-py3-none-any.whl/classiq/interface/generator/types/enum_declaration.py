from collections import Counter
from enum import Enum, EnumMeta, IntEnum

import pydantic

from classiq.interface.ast_node import HashableASTNode
from classiq.interface.exceptions import ClassiqValueError


class EnumDeclaration(HashableASTNode):
    name: str

    members: dict[str, int] = pydantic.Field(
        default_factory=dict,
        description="Dictionary of member names and their values",
    )

    @pydantic.field_validator("members")
    @classmethod
    def _validate_members(cls, members: dict[str, int]) -> dict[str, int]:
        underscore_members = [
            member for member in members.keys() if member.startswith("_")
        ]
        if len(underscore_members) > 0:
            raise ClassiqValueError(
                f"Enum member names must not start with an underscore. The offending "
                f"members: {underscore_members}"
            )

        counter = Counter(members.values())
        repeating_members = [
            member for member, value in members.items() if counter[value] > 1
        ]
        if len(repeating_members) > 0:
            raise ClassiqValueError(
                f"Cannot assign the same value to more than one enum member. The "
                f"offending members: {repeating_members}"
            )

        return members

    def create_enum(self) -> IntEnum:
        return IntEnum(self.name, self.members)


def declaration_from_enum(enum_type: EnumMeta) -> EnumDeclaration:
    members: list[Enum] = list(enum_type)
    return EnumDeclaration(
        name=enum_type.__name__,
        members={
            member.name: member.value
            for member in sorted(members, key=lambda member: member.value)
        },
    )
