from typing import Union

from sympy import Expr
from sympy.logic.boolalg import Boolean

from classiq.interface.generator.expressions.handle_identifier import HandleIdentifier
from classiq.interface.generator.expressions.qmod_sized_proxy import QmodSizedProxy
from classiq.interface.generator.expressions.qmod_struct_instance import (
    QmodStructInstance,
)
from classiq.interface.generator.expressions.type_proxy import TypeProxy

RuntimeConstant = Union[
    int,
    float,
    list,
    bool,
    QmodStructInstance,
    QmodSizedProxy,
    TypeProxy,
    HandleIdentifier,
]
RuntimeExpression = Union[Expr, Boolean]
ExpressionValue = Union[RuntimeConstant, RuntimeExpression]
