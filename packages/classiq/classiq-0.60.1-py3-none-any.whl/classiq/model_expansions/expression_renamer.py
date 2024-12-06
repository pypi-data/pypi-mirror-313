import ast
from collections.abc import Sequence

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.expressions.expression_constants import (
    RESERVED_EXPRESSIONS,
)
from classiq.interface.generator.visitor import Transformer
from classiq.interface.model.quantum_function_call import QuantumFunctionCall
from classiq.interface.model.quantum_function_declaration import (
    ClassicalParameterDeclaration,
    PositionalArg,
)

from classiq.model_expansions.visitors.variable_references import VarRefTransformer


class ExpressionRenamer(Transformer):

    def __init__(self, var_mapping: dict[str, str]) -> None:
        self.var_ref_transformer = VarRefTransformer(var_mapping)

    @property
    def var_mapping(self) -> dict[str, str]:
        return self.var_ref_transformer.var_mapping

    def visit_QuantumFunctionCall(
        self, node: QuantumFunctionCall
    ) -> QuantumFunctionCall:
        update_dict = dict(
            positional_args=[self.visit(arg) for arg in node.positional_args],
        )
        return node.model_copy(update=update_dict)

    def visit_Expression(self, expression: Expression) -> Expression:
        parsed_expr = ast.parse(expression.expr)
        renamed_expr = self.var_ref_transformer.visit(parsed_expr)
        return Expression(expr=ast.unparse(renamed_expr))

    def rename_string(self, name: str) -> str:
        return self.var_mapping.get(name, name)

    def rename_expression_dict(
        self, expr_dict: dict[str, Expression]
    ) -> dict[str, Expression]:
        return {
            self.rename_string(key): self.visit(val) for key, val in expr_dict.items()
        }

    @classmethod
    def from_positional_arg_declarations(
        cls, positional_arg_declarations: Sequence[PositionalArg], suffix: str
    ) -> "ExpressionRenamer":
        var_mapping: dict[str, str] = dict()
        for arg in positional_arg_declarations:
            if not isinstance(arg, ClassicalParameterDeclaration):
                continue
            if arg.name in RESERVED_EXPRESSIONS:
                continue
            new_name = arg.name + suffix
            var_mapping[arg.name] = new_name

        return cls(var_mapping)

    def rename_positional_arg_declarations(
        self, positional_arg_declarations: Sequence[PositionalArg]
    ) -> Sequence[PositionalArg]:
        return tuple(
            (
                arg.rename(self.var_mapping[arg.name])
                if isinstance(arg, ClassicalParameterDeclaration)
                and arg.name in self.var_mapping
                else arg
            )
            for arg in positional_arg_declarations
        )
