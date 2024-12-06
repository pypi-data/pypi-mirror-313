from typing import TYPE_CHECKING, Optional, Union

from classiq.interface.exceptions import ClassiqInternalExpansionError
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.model.bind_operation import BindOperation
from classiq.interface.model.control import Control
from classiq.interface.model.handle_binding import HandleBinding
from classiq.interface.model.inplace_binary_operation import (
    BinaryOperation,
    InplaceBinaryOperation,
)
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_call import QuantumFunctionCall
from classiq.interface.model.quantum_function_declaration import (
    NamedParamsQuantumFunctionDeclaration,
)
from classiq.interface.model.quantum_statement import QuantumStatement
from classiq.interface.model.quantum_type import QuantumBitvector, QuantumNumeric
from classiq.interface.model.variable_declaration_statement import (
    VariableDeclarationStatement,
)
from classiq.interface.model.within_apply_operation import WithinApply

from classiq.model_expansions.closure import FunctionClosure
from classiq.model_expansions.evaluators.parameter_types import (
    evaluate_types_in_quantum_symbols,
)
from classiq.model_expansions.evaluators.quantum_type_utils import (
    validate_inplace_binary_op_vars,
)
from classiq.model_expansions.quantum_operations.call_emitter import CallEmitter
from classiq.model_expansions.scope import QuantumSymbol, Scope
from classiq.qmod.builtins.functions import (
    CX,
    allocate,
    apply_to_all,
    integer_xor,
    modular_add,
    modular_add_constant,
    real_xor_constant,
)


def _binary_function_declaration(
    op: BinaryOperation, constant: bool
) -> NamedParamsQuantumFunctionDeclaration:
    return {
        False: {
            BinaryOperation.Addition: modular_add.func_decl,
            BinaryOperation.Xor: integer_xor.func_decl,
        },
        True: {
            BinaryOperation.Addition: modular_add_constant.func_decl,
            BinaryOperation.Xor: real_xor_constant.func_decl,
        },
    }[constant][op]


class InplaceBinaryOperationEmitter(CallEmitter[InplaceBinaryOperation]):
    def emit(self, op: InplaceBinaryOperation, /) -> None:
        if isinstance(op.value, Expression):
            self._emit_constant_operation(op)
            return

        value_var = self._interpreter.evaluate(op.value).as_type(QuantumSymbol)
        target_var = self._interpreter.evaluate(op.target).as_type(QuantumSymbol)
        value_var, target_var = evaluate_types_in_quantum_symbols(
            [value_var, target_var], self._current_scope
        )
        validate_inplace_binary_op_vars(value_var, target_var, op.operation.value)
        if TYPE_CHECKING:
            assert isinstance(value_var.quantum_type, QuantumNumeric)
            assert isinstance(target_var.quantum_type, QuantumNumeric)

        frac_digits_diff = (
            value_var.quantum_type.fraction_digits_value
            - target_var.quantum_type.fraction_digits_value
        )
        if (
            frac_digits_diff == value_var.quantum_type.size_in_bits
            or -frac_digits_diff == target_var.quantum_type.size_in_bits
        ):
            return

        value_var = QuantumSymbol(
            handle=HandleBinding(name="value"), quantum_type=value_var.quantum_type
        )
        target_var = QuantumSymbol(
            handle=HandleBinding(name="target"),
            quantum_type=target_var.quantum_type,
        )
        internal_func_decl = _binary_function_declaration(op.operation, constant=False)
        if op.operation == BinaryOperation.Xor:
            body = _build_inplace_xor_operation(
                value_var=value_var,
                target_var=target_var,
            )
        else:
            body = _build_inplace_binary_operation(
                value_var=value_var,
                target_var=target_var,
                internal_function_declaration=internal_func_decl,
            )
        inplace_binary_op_function = FunctionClosure.create(
            name=op.operation.value,
            positional_arg_declarations=[
                PortDeclaration(
                    name=value_var.handle.name,
                    quantum_type=value_var.quantum_type,
                    direction=PortDeclarationDirection.Inout,
                ),
                PortDeclaration(
                    name=target_var.handle.name,
                    quantum_type=target_var.quantum_type,
                    direction=PortDeclarationDirection.Inout,
                ),
            ],
            body=body,
            scope=Scope(parent=self._current_scope),
        )
        self._emit_quantum_function_call(
            inplace_binary_op_function, [op.value, op.target]
        )

    def _emit_constant_operation(self, op: InplaceBinaryOperation) -> None:
        if TYPE_CHECKING:
            assert isinstance(op.value, Expression)
        value = self._evaluate_expression(op.value)
        self._interpreter.emit(
            _internal_inplace_binary_operation_function_call(
                _binary_function_declaration(op.operation, constant=True),
                value,
                op.target,
            )
        )


def _build_inplace_binary_operation(
    value_var: QuantumSymbol,
    target_var: QuantumSymbol,
    internal_function_declaration: NamedParamsQuantumFunctionDeclaration,
) -> list[QuantumStatement]:
    if TYPE_CHECKING:
        assert isinstance(value_var.quantum_type, QuantumNumeric)
        assert isinstance(target_var.quantum_type, QuantumNumeric)

    frac_digits_diff = (
        value_var.quantum_type.fraction_digits_value
        - target_var.quantum_type.fraction_digits_value
    )

    target_overlap_var, target_var_decls, target_bind_ops = (
        _trim_superfluous_fraction_digits("target", target_var, -frac_digits_diff)
    )
    value_overlap_var, value_trim_var_decls, value_bind_ops = (
        _trim_superfluous_fraction_digits("value", value_var, frac_digits_diff)
    )
    size_diff = (
        value_overlap_var.quantum_type.size_in_bits
        - target_overlap_var.quantum_type.size_in_bits
    )
    (
        value_padded_var,
        value_pad_var_decls,
        value_pad_pre_bind_ops,
        value_pad_init_ops,
        value_post_bind_ops,
    ) = _pad_with_sign_bit("value", value_overlap_var, size_diff)

    op_call = _internal_inplace_binary_operation_function_call(
        internal_function_declaration,
        value_padded_var.handle,
        target_overlap_var.handle,
    )

    return [
        *target_var_decls,
        *value_trim_var_decls,
        *value_pad_var_decls,
        WithinApply(
            compute=[
                *target_bind_ops,
                *value_bind_ops,
                *value_pad_pre_bind_ops,
                *value_pad_init_ops,
                *value_post_bind_ops,
            ],
            action=[
                op_call,
            ],
        ),
    ]


def _build_inplace_xor_operation(
    value_var: QuantumSymbol, target_var: QuantumSymbol
) -> list[QuantumStatement]:
    if TYPE_CHECKING:
        assert isinstance(value_var.quantum_type, QuantumNumeric)
        assert isinstance(target_var.quantum_type, QuantumNumeric)

    frac_digits_diff = (
        value_var.quantum_type.fraction_digits_value
        - target_var.quantum_type.fraction_digits_value
    )

    target_overlap_var, target_var_decls, target_bind_ops = (
        _trim_superfluous_fraction_digits("target", target_var, -frac_digits_diff)
    )
    value_overlap_var, value_trim_var_decls, value_bind_ops = (
        _trim_superfluous_fraction_digits("value", value_var, frac_digits_diff)
    )
    target_left_var, value_left_var, sign_var_decls, sign_bind_ops, sign_xor = (
        _split_and_xor_sign(target_overlap_var, value_overlap_var)
    )

    action: list[QuantumStatement] = []
    if target_left_var is not None and value_left_var is not None:
        action.append(
            _internal_inplace_binary_operation_function_call(
                integer_xor.func_decl,
                value_left_var.handle,
                target_left_var.handle,
            )
        )
    action.extend(sign_xor)

    return [
        *target_var_decls,
        *value_trim_var_decls,
        *sign_var_decls,
        WithinApply(
            compute=[
                *target_bind_ops,
                *value_bind_ops,
                *sign_bind_ops,
            ],
            action=action,
        ),
    ]


def _internal_inplace_binary_operation_function_call(
    internal_function_declaration: NamedParamsQuantumFunctionDeclaration,
    value: Union[HandleBinding, Expression],
    target_var: HandleBinding,
) -> QuantumFunctionCall:
    internal_function_call = QuantumFunctionCall(
        function=internal_function_declaration.name,
        positional_args=[value, target_var],
    )
    internal_function_call.set_func_decl(internal_function_declaration)
    return internal_function_call


def _trim_superfluous_fraction_digits(
    kind: str, var: QuantumSymbol, frac_digits_diff: int
) -> tuple[QuantumSymbol, list[VariableDeclarationStatement], list[BindOperation]]:
    if frac_digits_diff <= 0:
        return var, [], []

    quantum_type = var.quantum_type
    if TYPE_CHECKING:
        assert isinstance(quantum_type, QuantumNumeric)

    trimmed_fraction_digits_var = QuantumSymbol(
        handle=HandleBinding(name=f"trimmed_{kind}_fraction_digits"),
        quantum_type=QuantumBitvector(
            length=Expression(expr=str(frac_digits_diff)),
        ),
    )
    overlap_var = QuantumSymbol(
        handle=HandleBinding(name=f"{kind}_overlap"),
        quantum_type=QuantumNumeric(
            size=Expression(expr=str(quantum_type.size_in_bits - frac_digits_diff)),
            is_signed=quantum_type.is_signed,
            fraction_digits=Expression(expr="0"),
        ),
    )
    bind_targets = trimmed_fraction_digits_var, overlap_var

    split_var_declarations = [
        VariableDeclarationStatement(
            name=var.handle.name,
            quantum_type=var.quantum_type,
        )
        for var in bind_targets
    ]
    bind_op = BindOperation(
        in_handles=[var.handle],
        out_handles=[var.handle for var in bind_targets],
    )

    return overlap_var, split_var_declarations, [bind_op]


def _pad_with_sign_bit(kind: str, var: QuantumSymbol, size_diff: int) -> tuple[
    QuantumSymbol,
    list[VariableDeclarationStatement],
    list[QuantumStatement],
    list[QuantumFunctionCall],
    list[BindOperation],
]:
    quantum_type = var.quantum_type
    if TYPE_CHECKING:
        assert isinstance(quantum_type, QuantumNumeric)

    if not quantum_type.sign_value or size_diff >= 0:
        return var, [], [], [], []

    padding_var, padding_allocation = _allocate_padding(kind, size_diff)
    padded_var = QuantumSymbol(
        handle=HandleBinding(name=f"padded_{kind}"),
        quantum_type=QuantumNumeric(
            size=Expression(expr=str(quantum_type.size_in_bits - size_diff)),
            is_signed=Expression(expr="False"),
            fraction_digits=Expression(expr="0"),
        ),
    )
    var_decls = [
        VariableDeclarationStatement(
            name=var.handle.name,
            quantum_type=var.quantum_type,
        )
        for var in (padding_var, padded_var)
    ]

    if quantum_type.size_in_bits == 1:  # qnum<1, SIGNED, ?>
        padding_init_ops = _init_padding(var, padding_var, size_diff)
        padding_rebind = BindOperation(
            in_handles=[var.handle, padding_var.handle],
            out_handles=[padded_var.handle],
        )
        return (
            padded_var,
            var_decls,
            [padding_allocation],
            padding_init_ops,
            [padding_rebind],
        )

    significand_var, sign_var, sign_split_bind = _split_var(kind, var, 1)
    padding_init_ops = _init_padding(sign_var, padding_var, size_diff)

    padding_rebind = BindOperation(
        in_handles=[significand_var.handle, sign_var.handle, padding_var.handle],
        out_handles=[padded_var.handle],
    )

    var_decls += [
        VariableDeclarationStatement(
            name=var.handle.name,
            quantum_type=var.quantum_type,
        )
        for var in (significand_var, sign_var)
    ]

    return (
        padded_var,
        var_decls,
        [sign_split_bind, padding_allocation],
        padding_init_ops,
        [padding_rebind],
    )


def _init_padding(
    sign_var: QuantumSymbol, padding_var: QuantumSymbol, size_diff: int
) -> list[QuantumFunctionCall]:
    padding_init_ops = [
        QuantumFunctionCall(
            function=CX.func_decl.name,
            positional_args=[sign_var.handle, padding_var[idx].handle],
        )
        for idx in range(-size_diff)
    ]
    for cx_call in padding_init_ops:
        cx_call.set_func_decl(CX.func_decl)
    return padding_init_ops


def _allocate_padding(
    kind: str, size_diff: int
) -> tuple[QuantumSymbol, QuantumFunctionCall]:
    padding_var = QuantumSymbol(
        handle=HandleBinding(name=f"{kind}_sign_padding"),
        quantum_type=QuantumBitvector(
            length=Expression(expr=str(-size_diff)),
        ),
    )
    padding_allocation = QuantumFunctionCall(
        function=allocate.func_decl.name,
        positional_args=[Expression(expr=str(-size_diff)), padding_var.handle],
    )
    padding_allocation.set_func_decl(allocate.func_decl)
    return padding_var, padding_allocation


def _split_var(
    kind: str, var: QuantumSymbol, right_size: int
) -> tuple[QuantumSymbol, QuantumSymbol, BindOperation]:
    left_var = QuantumSymbol(
        handle=HandleBinding(name=f"{kind}_left"),
        quantum_type=QuantumNumeric(
            size=Expression(expr=str(var.quantum_type.size_in_bits - right_size)),
            is_signed=Expression(expr="False"),
            fraction_digits=Expression(expr="0"),
        ),
    )
    right_var = QuantumSymbol(
        handle=HandleBinding(name=f"{kind}_right"),
        quantum_type=QuantumNumeric(
            size=Expression(expr=str(right_size)),
            is_signed=Expression(expr="False"),
            fraction_digits=Expression(expr="0"),
        ),
    )
    split_bind = BindOperation(
        in_handles=[var.handle],
        out_handles=[left_var.handle, right_var.handle],
    )
    return left_var, right_var, split_bind


def _split_and_xor_sign(target_var: QuantumSymbol, value_var: QuantumSymbol) -> tuple[
    Optional[QuantumSymbol],
    Optional[QuantumSymbol],
    list[VariableDeclarationStatement],
    list[BindOperation],
    list[Control],
]:
    if TYPE_CHECKING:
        assert isinstance(value_var.quantum_type, QuantumNumeric)
        assert isinstance(target_var.quantum_type, QuantumNumeric)
    size_diff = (
        value_var.quantum_type.size_in_bits - target_var.quantum_type.size_in_bits
    )
    if not value_var.quantum_type.sign_value or size_diff >= 0:
        return target_var, value_var, [], [], []

    if value_var.quantum_type.size_in_bits == 1:
        return None, None, [], [], [_xor_sign(target_var, value_var)]

    value_rest_var, value_sign_var, value_split_bind = _split_var("value", value_var, 1)
    target_left_var, target_right_var, target_split_bind = _split_var(
        "target", target_var, -size_diff + 1
    )
    var_decls = [
        VariableDeclarationStatement(
            name=var.handle.name,
            quantum_type=var.quantum_type,
        )
        for var in (value_rest_var, value_sign_var, target_left_var, target_right_var)
    ]
    bind_ops = [value_split_bind, target_split_bind]
    sign_xor = _xor_sign(target_right_var, value_sign_var)
    return target_left_var, value_rest_var, var_decls, bind_ops, [sign_xor]


def _xor_sign(target_var: QuantumSymbol, value_var: QuantumSymbol) -> Control:
    quantum_type = value_var.quantum_type
    if TYPE_CHECKING:
        assert isinstance(quantum_type, QuantumNumeric)
    if quantum_type.size_in_bits != 1 or quantum_type.fraction_digits_value not in (
        0,
        1,
    ):
        raise ClassiqInternalExpansionError

    inner_xor = QuantumFunctionCall(
        function=apply_to_all.func_decl.name,
        positional_args=["X", target_var.handle],
    )
    inner_xor.set_func_decl(apply_to_all.func_decl)

    if quantum_type.sign_value:
        if quantum_type.fraction_digits_value == 1:
            ctrl_value = -0.5
        else:
            ctrl_value = -1
    else:
        if quantum_type.fraction_digits_value == 1:
            ctrl_value = 0.5
        else:
            ctrl_value = 1

    return Control(
        expression=Expression(expr=f"{value_var.handle} == {ctrl_value}"),
        body=[inner_xor],
    )
