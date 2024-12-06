from classiq.interface.generator.functions.type_name import TypeName
from classiq.interface.generator.visitor import Visitor

from classiq.qmod.model_state_container import QMODULE


class QStructAnnotator(Visitor):
    def __init__(self) -> None:
        self._visited: set[TypeName] = set()

    def visit_TypeName(self, type_name: TypeName) -> None:
        decl = QMODULE.qstruct_decls.get(type_name.name)
        if decl is None or type_name.has_fields or (type_name in self._visited):
            return
        self._visited.add(type_name)
        new_fields = {
            field_name: field_type.model_copy()
            for field_name, field_type in decl.fields.items()
        }
        # We first visit the new fields and then set to deal with recursive
        # qstructs
        self.visit(new_fields)
        type_name.set_fields(new_fields)
