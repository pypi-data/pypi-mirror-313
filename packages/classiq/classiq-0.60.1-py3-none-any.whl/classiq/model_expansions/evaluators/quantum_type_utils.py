from typing import Optional

from classiq.interface.exceptions import (
    ClassiqExpansionError,
    ClassiqInternalExpansionError,
)
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.concrete_types import ConcreteQuantumType
from classiq.interface.generator.functions.type_name import (
    TypeName,
)
from classiq.interface.model.bind_operation import BindOperation
from classiq.interface.model.quantum_type import (
    QuantumBit,
    QuantumBitvector,
    QuantumNumeric,
    QuantumType,
)

from classiq.model_expansions.scope import QuantumSymbol, Scope


def copy_type_information(
    from_type: QuantumType,
    to_type: QuantumType,
    to_param_name: str,
) -> None:
    if isinstance(to_type, QuantumBit):
        set_size(to_type, from_type.size_in_bits, to_param_name)
    elif isinstance(to_type, QuantumNumeric):
        set_is_signed(to_type, getattr(from_type, "sign_value", None), to_param_name)
        set_fraction_digits(
            to_type,
            getattr(from_type, "fraction_digits_value", None),
            to_param_name,
        )
        set_size(to_type, from_type.size_in_bits, to_param_name)
    elif isinstance(to_type, QuantumBitvector):
        if isinstance(from_type, QuantumBitvector) and type(  # noqa: E721
            from_type.element_type
        ) == type(to_type.element_type):
            copy_type_information(
                from_type.element_type, to_type.element_type, to_param_name
            )
        set_size(to_type, from_type.size_in_bits, to_param_name)
    elif isinstance(to_type, TypeName):
        if isinstance(from_type, TypeName) and from_type.name == to_type.name:
            for field in from_type.fields:
                copy_type_information(
                    from_type.fields[field], to_type.fields[field], to_param_name
                )
        set_size(to_type, from_type.size_in_bits, to_param_name)
    else:
        raise ClassiqInternalExpansionError


def set_size(quantum_type: QuantumType, size: int, param_name: str) -> None:
    if size <= 0:
        raise ClassiqExpansionError(
            f"Size for {param_name!r} was deduced to be non-positive: {size!r}"
        )

    if quantum_type.has_size_in_bits and quantum_type.size_in_bits != size:
        raise ClassiqExpansionError(
            f"Size mismatch for port {param_name!r} between declared size {quantum_type.size_in_bits} and assigned size {size}"
        )

    if isinstance(quantum_type, QuantumNumeric):
        quantum_type.size = Expression(expr=str(size))
        if not quantum_type.has_sign or not quantum_type.has_fraction_digits:
            set_is_signed(quantum_type, False, param_name)
            set_fraction_digits(quantum_type, 0, param_name)
    elif isinstance(quantum_type, QuantumBitvector):
        if quantum_type.has_length:
            if size % quantum_type.length_value != 0:
                raise ClassiqExpansionError(
                    f"Size mismatch for port {param_name!r}. Cannot fit {size} "
                    f"qubits into an array of {quantum_type.length_value} elements."
                )
            set_size(
                quantum_type.element_type,
                size // quantum_type.length_value,
                param_name,
            )
        set_length_by_size(quantum_type, size, param_name)
    elif isinstance(quantum_type, TypeName):
        fields_without_size = [
            field_type
            for field_type in quantum_type.fields.values()
            if not field_type.has_size_in_bits
        ]
        if len(fields_without_size) > 1:
            raise ClassiqInternalExpansionError(
                f"QuantumStruct should have at most one field without "
                f"predetermined size. Found {fields_without_size}."
            )
        if len(fields_without_size) == 1:
            predetermined_size_part = sum(
                field_type.size_in_bits if field_type.has_size_in_bits else 0
                for field_type in quantum_type.fields.values()
            )
            set_size(fields_without_size[0], size - predetermined_size_part, param_name)


def set_fraction_digits(
    quantum_numeric: QuantumNumeric, fraction_digits: Optional[int], param_name: str
) -> None:
    if fraction_digits is not None and fraction_digits < 0:
        raise ClassiqExpansionError(
            f"Number of fraction digits for {param_name!r} was deduced to be negative: "
            f"{fraction_digits!r}"
        )

    if (
        fraction_digits is not None
        and quantum_numeric.fraction_digits is not None
        and quantum_numeric.fraction_digits.is_evaluated()
        and quantum_numeric.fraction_digits_value != fraction_digits
    ):
        raise ClassiqExpansionError(
            f"Fraction digits mismatch for port {param_name!r} between declared "
            f"fraction digits {quantum_numeric.fraction_digits_value!r} and assigned fraction "
            f"digits {fraction_digits!r}"
        )

    if not (
        quantum_numeric.fraction_digits is not None
        and quantum_numeric.fraction_digits.is_evaluated()
    ):
        quantum_numeric.fraction_digits = Expression(expr=str(fraction_digits or 0))


def set_is_signed(
    quantum_numeric: QuantumNumeric, is_signed: Optional[bool], param_name: str
) -> None:
    if (
        is_signed is not None
        and quantum_numeric.is_signed is not None
        and quantum_numeric.is_signed.is_evaluated()
        and quantum_numeric.sign_value != is_signed
    ):
        raise ClassiqExpansionError(
            f"Sign mismatch for port {param_name!r} between declared sign {quantum_numeric.sign_value!r} and assigned sign {is_signed!r}"
        )

    if not (
        quantum_numeric.is_signed is not None
        and quantum_numeric.is_signed.is_evaluated()
    ):
        quantum_numeric.is_signed = Expression(expr=str(is_signed or False))


def set_element_type(
    quantum_array: QuantumBitvector, element_type: ConcreteQuantumType
) -> None:
    quantum_array.element_type = element_type


def set_length(quantum_array: QuantumBitvector, length: int) -> None:
    quantum_array.length = Expression(expr=str(length))


def set_length_by_size(
    quantum_array: QuantumBitvector, size: int, param_name: str
) -> None:
    if size <= 0:
        raise ClassiqExpansionError(
            f"Size for {param_name!r} was deduced to be non-positive: {size!r}"
        )

    if quantum_array.has_size_in_bits and quantum_array.size_in_bits != size:
        raise ClassiqExpansionError(
            f"Size mismatch for port {param_name!r} between declared size "
            f"{quantum_array.size_in_bits} ({quantum_array.length_value} elements of "
            f"size {quantum_array.element_type.size_in_bits}) and assigned size {size}."
        )

    if not quantum_array.element_type.has_size_in_bits:
        raise ClassiqExpansionError(
            f"Could not infer element size for array {param_name!r}."
        )
    element_size = quantum_array.element_type.size_in_bits

    if size % element_size != 0:
        raise ClassiqExpansionError(
            f"Size mismatch for port {param_name!r}. Cannot fit elements of type "
            f"{quantum_array.element_type.qmod_type_name} (size {element_size}) into "
            f"{size} qubits."
        )

    quantum_array.length = Expression(expr=str(size // element_size))


def validate_bind_targets(bind: BindOperation, scope: Scope) -> None:
    illegal_qnum_bind_targets = []
    for out_handle in bind.out_handles:
        out_var = scope[out_handle.name].as_type(QuantumSymbol)
        out_var_type = out_var.quantum_type
        if not isinstance(out_var_type, QuantumNumeric):
            continue
        if not out_var_type.has_size_in_bits:
            illegal_qnum_bind_targets.append(str(out_var.handle))
        elif not out_var_type.has_sign:
            assert not out_var_type.has_fraction_digits
            illegal_qnum_bind_targets.append(str(out_var.handle))
    if len(illegal_qnum_bind_targets) > 0:
        raise ClassiqExpansionError(
            f"QNum bind targets {illegal_qnum_bind_targets!r} must be declared or initialized with size, sign, and fraction digits"
        )


def validate_inplace_binary_op_vars(
    value_var: QuantumSymbol, target_var: QuantumSymbol, operation_name: str
) -> None:
    if not isinstance(value_var.quantum_type, QuantumNumeric):
        raise ClassiqExpansionError(
            f"Cannot perform `{operation_name}` operation with non numeric value {value_var.handle}"
        )
    if not isinstance(target_var.quantum_type, QuantumNumeric):
        raise ClassiqExpansionError(
            f"Cannot perform `{operation_name}` operation with non numeric target {target_var.handle}"
        )
