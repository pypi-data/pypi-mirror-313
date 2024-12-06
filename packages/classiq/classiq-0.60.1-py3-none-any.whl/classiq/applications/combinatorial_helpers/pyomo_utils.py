import math
import re
from enum import Enum
from typing import Any, Optional, TypeVar, Union

import pydantic
import pyomo.core.expr.numeric_expr as pyo_expr
import pyomo.environ as pyo
import sympy
from pyomo.core import ConcreteModel, Constraint, Objective, Var, maximize
from pyomo.core.base import _GeneralVarData
from pyomo.core.base.component import ComponentData
from pyomo.core.base.constraint import _GeneralConstraintData
from pyomo.core.base.indexed_component import IndexedComponent
from pyomo.core.base.objective import ScalarObjective
from pyomo.core.expr.sympy_tools import (
    Pyomo2SympyVisitor,
    PyomoSympyBimap,
    Sympy2PyomoVisitor,
)

from classiq.interface.exceptions import ClassiqValueError
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.classical_type import Integer
from classiq.interface.generator.types.struct_declaration import StructDeclaration

from classiq.qmod.qmod_variable import QBit, QNum, QStruct, QVar
from classiq.qmod.symbolic_expr import SymbolicExpr

ListVars = list[_GeneralVarData]
SUPPORTED_TYPES = [
    pyo.Binary,
    pyo.Integers,
    pyo.NegativeIntegers,
    pyo.NonNegativeIntegers,
    pyo.NonPositiveIntegers,
    pyo.PositiveIntegers,
]


class ObjectiveType(Enum):
    Min = "Min"
    Max = "Max"


class CombinatorialOptimizationStructDeclaration(StructDeclaration):
    variable_lower_bound: int = pydantic.Field(default=0)
    variable_upper_bound: int = pydantic.Field(default=1)
    constraints: list[Expression] = pydantic.Field(
        default_factory=list, description="List of constraint expressions"
    )
    objective_type: ObjectiveType = pydantic.Field(
        description="Specify whether the optimization problem is Min or Max"
    )
    objective_function: Expression = pydantic.Field(
        description="The expression to optimize, according to the objective type"
    )


def contains(var_data: _GeneralVarData, vars_data: ListVars) -> bool:
    # HACK: standard "__containts__ (in)" method doesn't work, because pyomo overrode the __eq__ method (IMO)
    return any(var_data is var_data_temp for var_data_temp in vars_data)


def remove(var_data: _GeneralVarData, vars_data: ListVars) -> ListVars:
    # HACK: standard "list method remove" method doesn't work, because pyomo overrode the __eq__ method (IMO)
    assert contains(var_data, vars_data), "var not in list"
    vars_data = vars_data.copy()
    for idx, var_data_temp in enumerate(vars_data):
        if var_data_temp is var_data:
            del vars_data[idx]
            break
    return vars_data


def index(var_data: _GeneralVarData, vars_data: ListVars) -> int:
    # HACK: standard "index method" doesn't work.
    assert contains(var_data, vars_data), "var not in list"
    idxs = [
        idx for idx, var_data_temp in enumerate(vars_data) if var_data is var_data_temp
    ]
    return idxs[0]


T = TypeVar("T")


def extract(model: ConcreteModel, type_: type[T]) -> list[T]:
    if type_ == _GeneralVarData:
        type_ = Var

    elif type_ == _GeneralConstraintData:
        type_ = Constraint

    components = model.component_objects(type_)
    return [
        component[component_idx]
        for component in components
        for component_idx in component
    ]


def delete_component(model: ConcreteModel, component: ComponentData) -> None:
    parent_ref = component._component

    if parent_ref is None:
        return

    parent_component = parent_ref()

    if component is parent_component:
        model.del_component(component)
    else:
        _delete_element_by_value(parent_component, component)

        if not parent_component:
            model.del_component(parent_component)


def _delete_element_by_value(dict_: dict, value: Any) -> None:
    iter_dict = {**dict_}
    for k, v in iter_dict.items():
        if v is value and k in dict_:
            del dict_[k]


def get_name(component: Union[IndexedComponent, ComponentData]) -> str:
    if isinstance(component, IndexedComponent):
        return component._name  # constraint.name returns "'{name}'"
    else:
        return component.name


class FixedSympy2PyomoVisitor(Sympy2PyomoVisitor):
    def beforeChild(  # noqa: N802
        self, node: Optional[sympy.Expr], child: sympy.Expr, child_idx: Optional[int]
    ) -> tuple[bool, Union[int, float, None]]:
        if not child._args:
            item = self.object_map.getPyomoSymbol(child, None)
            if item is None:
                if isinstance(child, sympy.Integer):  # addition to base implementation
                    item = int(child.evalf())
                else:
                    item = float(child.evalf())
            return False, item
        return True, None


def sympy2pyomo_expression(
    expr: sympy.core.Basic, object_map: PyomoSympyBimap
) -> pyo_expr.ExpressionBase:
    return FixedSympy2PyomoVisitor(object_map).walk_expression(expr)


def convert_pyomo_to_global_presentation(
    pyo_model: pyo.ConcreteModel,
) -> pyo.ConcreteModel:
    problem_struct = pyomo2qmod("nativePyoModel", pyo_model)

    pyomo_model = pyo.ConcreteModel()

    var_names = list(problem_struct.variables.keys())
    pyomo_model.var_set = pyo.Var(
        var_names,
        domain=pyo.NonNegativeIntegers,
        bounds=(
            problem_struct.variable_lower_bound,
            problem_struct.variable_upper_bound,
        ),
    )
    obj_map = PyomoSympyBimap()
    var_dict = {
        var_name: obj_map.getSympySymbol(pyomo_model.var_set[var_name])
        for var_name in var_names
    }

    def expr2pyomo(expr: Expression) -> pyo_expr.ExpressionBase:
        sp_expr = sympy.sympify(expr.expr, locals=var_dict)
        if isinstance(sp_expr, sympy.core.relational.Equality):
            return sympy2pyomo_expression(
                sp_expr.args[0], obj_map
            ) == sympy2pyomo_expression(sp_expr.args[1], obj_map)

        # Note that strict greater/less than are not supported by Pyomo
        return sympy2pyomo_expression(sp_expr, obj_map)

    pyomo_model.constraints = pyo.Constraint(
        pyo.RangeSet(0, len(problem_struct.constraints) - 1),
        rule=lambda model, i: expr2pyomo(problem_struct.constraints[i]),
    )
    pyomo_model.objective = pyo.Objective(
        expr=expr2pyomo(problem_struct.objective_function),
        sense=(
            pyo.maximize
            if problem_struct.objective_type == ObjectiveType.Max
            else pyo.minimize
        ),
    )

    return pyomo_model


def pyomo2qmod(
    struct_name: str, pyo_model: ConcreteModel
) -> CombinatorialOptimizationStructDeclaration:
    symbols_map = PyomoSympyBimap()

    variables: list[sympy.Symbol] = []

    bounds_set = False
    lower_bound = None
    upper_bound = None

    for var_dict in pyo_model.component_objects(Var):
        for key in var_dict:
            var = Pyomo2SympyVisitor(symbols_map).walk_expression(var_dict[key])
            var.name = var.name.replace(",", "_")
            variables.append(var)
            if bounds_set:
                if lower_bound != var_dict[key].lb:
                    raise ClassiqValueError(
                        "All problem variables must agree on lower bound"
                    )
                if upper_bound != var_dict[key].ub:
                    raise ClassiqValueError(
                        "All problem variables must agree on upper bound"
                    )
            else:
                lower_bound = var_dict[key].lb
                upper_bound = var_dict[key].ub
                bounds_set = True

    constraint_exprs: list[sympy.Expr] = []

    constraint_exprs.extend(
        Pyomo2SympyVisitor(symbols_map).walk_expression(constraint_dict[key].expr)
        for constraint_dict in pyo_model.component_objects(Constraint)
        for key in constraint_dict
    )

    pyo_objective: ScalarObjective = next(pyo_model.component_objects(Objective))
    objective_type_str = "Max" if pyo_objective.sense == maximize else "Min"
    objective_expr: sympy.Expr = Pyomo2SympyVisitor(symbols_map).walk_expression(
        pyo_objective
    )

    return CombinatorialOptimizationStructDeclaration(
        name=struct_name,
        variables={str(variable): Integer() for variable in variables},
        variable_lower_bound=lower_bound,
        variable_upper_bound=upper_bound,
        constraints=[
            Expression(expr=str(constraint_expr))
            for constraint_expr in constraint_exprs
        ],
        objective_type=objective_type_str,
        objective_function=Expression(expr=str(objective_expr)),
    )


def pyomo_to_qmod_qstruct(
    struct_name: str, vars: list[_GeneralVarData]
) -> type[QStruct]:
    qmod_struct = type(struct_name, (QStruct,), {})
    var_names = {get_field_name(var): var for var in vars}
    qmod_struct.__annotations__ = {
        var_name: _get_qmod_field_type(var_name, var_data)
        for var_name, var_data in var_names.items()
    }
    return qmod_struct


def _get_qmod_field_type(var_name: str, var_data: _GeneralVarData) -> type[QVar]:
    if var_data.domain not in SUPPORTED_TYPES:
        raise ClassiqValueError(
            f"Type {str(var_data.domain)!r} of variable {var_name!r} is not supported"
        )

    if var_data.domain == pyo.Binary:
        return QBit

    bounds = var_data.bounds
    if bounds is None:
        raise ClassiqValueError(f"Variable {var_name!r} has no bounds")
    lb, ub = bounds
    if not isinstance(lb, int) or not isinstance(ub, int):
        raise ClassiqValueError(
            f"Non-integer bounds for variable {var_name!r} are not supported"
        )
    if lb > 0:
        ub -= lb
    qnum: Any = QNum  # mypy shenanigans
    return qnum[math.ceil(math.log2(ub - lb)), False, 0]


def evaluate_objective(
    var_mapping: dict, sympy_expr: sympy.Expr, struct_obj: Any
) -> Any:
    sympy_assignment = {
        sympy_var: getattr(struct_obj, field_name)
        for sympy_var, field_name in var_mapping.items()
    }

    # classical objective evaluation
    if not isinstance(struct_obj, QStruct):
        return float(sympy_expr.evalf(subs=sympy_assignment))

    # quantum objective evaluation
    expr_str = str(sympy_expr).replace("'", "")
    for var_name, var_value in sympy_assignment.items():
        var_name = str(var_name).replace("'", "")
        expr_str = re.sub(rf"\b{var_name}\b", str(var_value), expr_str)
    return SymbolicExpr(expr=expr_str, is_quantum=True)


def get_field_name(var: _GeneralVarData) -> str:
    return var.local_name.replace("[", "_").replace("]", "")
