from typing import TYPE_CHECKING, Optional, Union, cast

from classiq.interface.exceptions import ClassiqError
from classiq.interface.executor.execution_preferences import ExecutionPreferences
from classiq.interface.generator.model.constraints import Constraints
from classiq.interface.generator.model.preferences.preferences import Preferences
from classiq.interface.helpers.pydantic_model_helpers import nameables_to_dict
from classiq.interface.model.model import MAIN_FUNCTION_NAME, Model, SerializedModel
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.quantum_function_call import QuantumFunctionCall

from classiq.model_expansions.interpreter import Interpreter
from classiq.qmod.builtins.functions import BUILTIN_FUNCTION_DECLARATIONS
from classiq.qmod.classical_function import CFunc
from classiq.qmod.generative import (
    is_generative_expansion_enabled,
    set_frontend_interpreter,
)
from classiq.qmod.model_state_container import QMODULE
from classiq.qmod.qfunc import DEC_QFUNCS, GEN_QFUNCS
from classiq.qmod.quantum_expandable import _prepare_args
from classiq.qmod.quantum_function import GenerativeQFunc, QFunc
from classiq.qmod.semantics.static_semantics_visitor import resolve_function_calls
from classiq.qmod.write_qmod import write_qmod

GEN_MAIN_NAME = "_gen_main"


def create_model(
    entry_point: Union[QFunc, GenerativeQFunc],
    constraints: Optional[Constraints] = None,
    execution_preferences: Optional[ExecutionPreferences] = None,
    preferences: Optional[Preferences] = None,
    classical_execution_function: Optional[CFunc] = None,
    out_file: Optional[str] = None,
) -> SerializedModel:
    """
    Create a serialized model from a given Qmod entry function and additional parameters.

    Args:
        entry_point: The entry point function for the model, which must be a QFunc named 'main'.
        constraints: Constraints for the synthesis of the model. See Constraints (Optional).
        execution_preferences: Preferences for the execution of the model. See ExecutionPreferences (Optional).
        preferences: Preferences for the synthesis of the model. See Preferences (Optional).
        classical_execution_function: A function for the classical execution logic, which must be a CFunc (Optional).
        out_file: File path to write the Qmod model in native Qmod representation to (Optional).

    Returns:
        SerializedModel: A serialized model.

    Raises:
        ClassiqError: If the entry point function is not named 'main'.
    """

    if entry_point.func_decl.name != MAIN_FUNCTION_NAME:
        raise ClassiqError(
            f"The entry point function must be named 'main', got '{entry_point.func_decl.name}'"
        )

    user_gen_functions = {
        gen_func._py_callable.__name__ for gen_func in GEN_QFUNCS
    } - set(BUILTIN_FUNCTION_DECLARATIONS.keys())

    if len(user_gen_functions) > 0 and is_generative_expansion_enabled():
        model = _expand_generative_model(
            (
                entry_point
                if isinstance(entry_point, QFunc)
                else QFunc(entry_point._py_callable)
            ),
            constraints,
            execution_preferences,
            preferences,
        )
    else:
        if TYPE_CHECKING:
            assert isinstance(entry_point, QFunc)
        model = entry_point.create_model(
            constraints,
            execution_preferences,
            preferences,
            classical_execution_function,
        )
    result = model.get_model()

    if out_file is not None:
        write_qmod(result, out_file)

    return result


def _expand_generative_model(
    gen_main: QFunc,
    constraints: Optional[Constraints] = None,
    execution_preferences: Optional[ExecutionPreferences] = None,
    preferences: Optional[Preferences] = None,
) -> Model:
    @QFunc
    def _dummy() -> None:
        pass

    model = _dummy.create_model(
        constraints,
        execution_preferences,
        preferences,
    )
    gen_expand_model = _get_generative_functions(gen_main, preferences)
    model.functions = gen_expand_model.functions
    model.functions_compilation_metadata = (
        gen_expand_model.functions_compilation_metadata
    )
    model.types = list(QMODULE.type_decls.values())
    model.enums = list(QMODULE.enum_decls.values())
    model.qstructs = list(QMODULE.qstruct_decls.values())
    return model


def _get_generative_functions(
    gen_main: QFunc,
    preferences: Optional[Preferences],
) -> Model:
    # The Interpreter accepts a model and a list of generative functions.
    # Since the main function is generative, it can only be expanded using the
    # Interpreter.
    # To solve this deadlock, we create a wrapper model
    # `qfunc main(...) { _gen_main(...); }` and rename `main` to `_gen_main` before
    # passing them to the Interpreter.
    gen_model = _get_wrapper_main(gen_main, preferences)
    gen_functions = _get_all_model_functions_as_generative_functions()
    return _interpret_generative_model(gen_model, gen_functions)


def _get_wrapper_main(
    gen_main: QFunc,
    preferences: Optional[Preferences],
) -> Model:
    extra_args = {}
    if preferences is not None:
        extra_args["preferences"] = preferences
    functions_compilation_metadata = {
        qfunc._py_callable.__name__: qfunc.compilation_metadata
        for qfunc in DEC_QFUNCS + GEN_QFUNCS
        if qfunc.compilation_metadata is not None
    }
    return Model(
        functions=[
            NativeFunctionDefinition(
                name=MAIN_FUNCTION_NAME,
                positional_arg_declarations=gen_main.func_decl.positional_arg_declarations,
                body=[
                    QuantumFunctionCall(
                        function=GEN_MAIN_NAME,
                        positional_args=_prepare_args(
                            gen_main.func_decl,
                            gen_main._get_positional_args(),
                            {},
                        ),
                    ),
                ],
            ),
        ],
        functions_compilation_metadata=functions_compilation_metadata,
        **extra_args,
    )


def _get_all_model_functions_as_generative_functions() -> list[GenerativeQFunc]:

    gen_functions = list(GEN_QFUNCS) + [
        GenerativeQFunc(
            dec_func._py_callable, dec_func.func_decl, dec_func.compilation_metadata
        )
        for dec_func in DEC_QFUNCS
    ]
    return [
        (
            gen_func
            if gen_func.func_decl.name != MAIN_FUNCTION_NAME
            else GenerativeQFunc(
                gen_func._py_callable,
                gen_func.func_decl.model_copy(update={"name": GEN_MAIN_NAME}),
                gen_func.compilation_metadata,
            )
        )
        for gen_func in gen_functions
        if gen_func.func_decl.name not in BUILTIN_FUNCTION_DECLARATIONS
    ]


def _interpret_generative_model(
    gen_model: Model, gen_functions: list[GenerativeQFunc]
) -> Model:
    resolve_function_calls(
        gen_model,
        {gen_func.func_decl.name: gen_func.func_decl for gen_func in gen_functions},
    )
    interpreter = Interpreter(gen_model, gen_functions, is_frontend=True)
    set_frontend_interpreter(interpreter)
    expand_model = interpreter.expand()
    functions_dict = nameables_to_dict(expand_model.functions)

    # Inline _gen_main call in main
    expanded_gen_main_name = cast(
        QuantumFunctionCall, functions_dict[MAIN_FUNCTION_NAME].body[0]
    ).func_name
    functions_dict[MAIN_FUNCTION_NAME] = functions_dict[
        expanded_gen_main_name
    ].model_copy(update={"name": MAIN_FUNCTION_NAME})
    functions_dict.pop(expanded_gen_main_name)
    return expand_model.model_copy(update={"functions": list(functions_dict.values())})
