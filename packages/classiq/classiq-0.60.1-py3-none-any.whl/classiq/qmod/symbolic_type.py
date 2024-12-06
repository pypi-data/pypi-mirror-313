from typing import Union

from classiq.qmod.symbolic_expr import SymbolicExpr

SymbolicTypes = Union[SymbolicExpr, int, float, bool, tuple["SymbolicTypes", ...]]
