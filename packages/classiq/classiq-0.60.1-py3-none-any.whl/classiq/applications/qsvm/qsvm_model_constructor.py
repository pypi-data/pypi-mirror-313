from typing import Any

from classiq.interface.applications.qsvm import DataList, LabelsInt
from classiq.interface.exceptions import ClassiqValueError
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.model.handle_binding import HandleBinding
from classiq.interface.model.model import Model, SerializedModel
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_call import QuantumFunctionCall

from classiq.qmod.builtins.enums import Pauli, QSVMFeatureMapEntanglement
from classiq.qmod.utilities import qmod_val_to_expr_str

INVALID_FEATURE_MAP_FUNC_NAME_MSG = "Invalid feature_map_function_name, it can be bloch_sphere_feature_map or pauli_feature_map"

_OUTPUT_VARIABLE_NAME = "qsvm_results"


def _bloch_sphere_feature_map_function_params(
    bloch_feature_dimension: int,
) -> tuple[list[Expression], str]:
    return [
        Expression(expr=f"{bloch_feature_dimension}")
    ], f"ceiling({bloch_feature_dimension}/2)"


def _pauli_feature_map_function_params(
    paulis: list[list[Pauli]],
    entanglement: QSVMFeatureMapEntanglement,
    alpha: int,
    reps: int,
    feature_dimension: int,
) -> tuple[list[Expression], str]:
    paulis_str = (
        "["
        + ",".join(
            [
                "[" + ",".join([qmod_val_to_expr_str(p) for p in p_list]) + "]"
                for p_list in paulis
            ]
        )
        + "]"
    )
    pauli_feature_map_params = (
        f"paulis={paulis_str}, "
        f"entanglement={qmod_val_to_expr_str(entanglement)}, "
        f"alpha={alpha}, "
        f"reps={reps}, "
        f"feature_dimension={feature_dimension}"
    )
    return [
        Expression(
            expr=f"struct_literal(QSVMFeatureMapPauli, {pauli_feature_map_params})"
        )
    ], f"{feature_dimension}"


def get_qsvm_qmain_body(
    feature_map_function_name: str, **kwargs: Any
) -> list[QuantumFunctionCall]:
    if feature_map_function_name == "bloch_sphere_feature_map":
        params, size_expr = _bloch_sphere_feature_map_function_params(**kwargs)
    elif feature_map_function_name == "pauli_feature_map":
        params, size_expr = _pauli_feature_map_function_params(**kwargs)
    else:
        raise ClassiqValueError(INVALID_FEATURE_MAP_FUNC_NAME_MSG)

    return [
        QuantumFunctionCall(
            function="allocate",
            positional_args=[Expression(expr=size_expr), HandleBinding(name="qbv")],
        ),
        QuantumFunctionCall(
            function=feature_map_function_name,
            positional_args=[*params, HandleBinding(name="qbv")],
        ),
    ]


def construct_qsvm_model(
    train_data: DataList,
    train_labels: LabelsInt,
    test_data: DataList,
    test_labels: LabelsInt,
    predict_data: DataList,
    feature_map_function_name: str,
    **kwargs: Any,
) -> SerializedModel:
    qsvm_qmod = Model(
        functions=[
            NativeFunctionDefinition(
                name="main",
                positional_arg_declarations=[
                    PortDeclaration(
                        name="qbv",
                        direction=PortDeclarationDirection.Output,
                    ),
                ],
                body=get_qsvm_qmain_body(
                    feature_map_function_name=feature_map_function_name, **kwargs
                ),
            ),
        ],
        classical_execution_code=f"""
{_OUTPUT_VARIABLE_NAME} = qsvm_full_run(
    train_data={train_data},
    train_labels={train_labels},
    test_data={test_data},
    test_labels={test_labels},
    predict_data={predict_data}
)
save({{{_OUTPUT_VARIABLE_NAME!r}: {_OUTPUT_VARIABLE_NAME}}})
""".strip(),
    )

    return qsvm_qmod.get_model()
