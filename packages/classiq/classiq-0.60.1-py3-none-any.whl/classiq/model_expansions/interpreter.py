import copy
from collections.abc import Iterator, Sequence
from contextlib import contextmanager, nullcontext
from functools import singledispatchmethod
from typing import Any, Optional, cast

import numpy as np
from numpy.random import permutation
from pydantic import ValidationError

from classiq.interface.exceptions import (
    ClassiqError,
    ClassiqExpansionError,
    ClassiqInternalExpansionError,
)
from classiq.interface.generator.constant import Constant
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.types.compilation_metadata import CompilationMetadata
from classiq.interface.model.bind_operation import BindOperation
from classiq.interface.model.classical_if import ClassicalIf
from classiq.interface.model.control import Control
from classiq.interface.model.handle_binding import (
    FieldHandleBinding,
    HandleBinding,
    SlicedHandleBinding,
    SubscriptHandleBinding,
)
from classiq.interface.model.inplace_binary_operation import InplaceBinaryOperation
from classiq.interface.model.invert import Invert
from classiq.interface.model.model import Model
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.phase_operation import PhaseOperation
from classiq.interface.model.power import Power
from classiq.interface.model.quantum_expressions.quantum_expression import (
    QuantumAssignmentOperation,
)
from classiq.interface.model.quantum_function_call import (
    OperandIdentifier,
    QuantumFunctionCall,
)
from classiq.interface.model.quantum_function_declaration import (
    NamedParamsQuantumFunctionDeclaration,
    QuantumFunctionDeclaration,
)
from classiq.interface.model.quantum_lambda_function import QuantumLambdaFunction
from classiq.interface.model.quantum_statement import QuantumStatement
from classiq.interface.model.repeat import Repeat
from classiq.interface.model.variable_declaration_statement import (
    VariableDeclarationStatement,
)
from classiq.interface.model.within_apply_operation import WithinApply

from classiq.model_expansions.closure import (
    Closure,
    FunctionClosure,
    GenerativeClosure,
    GenerativeFunctionClosure,
)
from classiq.model_expansions.debug_flag import debug_mode
from classiq.model_expansions.evaluators.classical_expression import (
    evaluate_classical_expression,
)
from classiq.model_expansions.expression_renamer import ExpressionRenamer
from classiq.model_expansions.function_builder import (
    FunctionContext,
    OperationBuilder,
    OperationContext,
)
from classiq.model_expansions.generative_functions import emit_generative_statements
from classiq.model_expansions.quantum_operations import (
    BindEmitter,
    ClassicalIfEmitter,
    ControlEmitter,
    InplaceBinaryOperationEmitter,
    InvertEmitter,
    PowerEmitter,
    QuantumAssignmentOperationEmitter,
    QuantumFunctionCallEmitter,
    RepeatEmitter,
    VariableDeclarationStatementEmitter,
    WithinApplyEmitter,
)
from classiq.model_expansions.quantum_operations.phase import PhaseEmitter
from classiq.model_expansions.scope import Evaluated, QuantumSymbol, Scope
from classiq.model_expansions.scope_initialization import (
    add_constants_to_scope,
    add_entry_point_params_to_scope,
    get_main_renamer,
    init_top_level_scope,
)
from classiq.model_expansions.utils.counted_name_allocator import CountedNameAllocator
from classiq.qmod.builtins.functions import permute
from classiq.qmod.quantum_function import GenerativeQFunc
from classiq.qmod.semantics.error_manager import ErrorManager


class Interpreter:
    def __init__(
        self,
        model: Model,
        generative_functions: Optional[list[GenerativeQFunc]] = None,
        is_frontend: bool = False,
    ) -> None:
        self._is_frontend = is_frontend
        self._model = model
        self._current_scope = Scope()
        self._top_level_scope = self._current_scope
        self._builder = OperationBuilder(self._top_level_scope)
        self._expanded_functions: dict[str, NativeFunctionDefinition] = {}

        self._main_renamer: ExpressionRenamer = get_main_renamer(self._model.functions)

        if generative_functions is None:
            generative_functions = []
        self._generative_functions = generative_functions
        init_top_level_scope(model, generative_functions, self._current_scope)
        self._expanded_functions_compilation_metadata: dict[
            str, CompilationMetadata
        ] = dict()
        self._counted_name_allocator = CountedNameAllocator()
        self._error_manager: ErrorManager = ErrorManager()

    @contextmanager
    def _scope_guard(self, scope: Scope) -> Iterator[None]:
        """This manager restores both `scope` and `self._current_scope` to their previous values."""
        scope_data = copy.copy(scope.data)
        prev_context_scope_data = copy.copy(self._current_scope.data)

        prev_context_scope = self._current_scope
        self._current_scope = scope
        yield
        prev_context_scope.data = prev_context_scope_data
        self._current_scope = prev_context_scope

        scope.data = scope_data

    def _expand_main_func(self) -> None:
        main_closure = FunctionClosure.create(
            name=self._model.main_func.name,
            positional_arg_declarations=self._model.main_func.positional_arg_declarations,
            body=self._model.main_func.body,
            scope=Scope(parent=self._current_scope),
            expr_renamer=self._main_renamer,
            _depth=0,
        )

        add_entry_point_params_to_scope(
            main_closure.positional_arg_declarations, main_closure
        )
        context = self._expand_operation(main_closure)
        self._expanded_functions[main_closure.closure_id] = (
            self._builder.create_definition(cast(FunctionContext, context))
        )

    def expand(self) -> Model:
        try:
            with self._error_manager.call("main"):
                self._expand_main_func()
        except Exception as e:
            if isinstance(e, ClassiqInternalExpansionError) or debug_mode.get():
                raise e
            if not isinstance(e, (ClassiqError, ValidationError)):
                raise ClassiqInternalExpansionError(str(e)) from None
            prefix = ""
            if not isinstance(e, ClassiqExpansionError):
                prefix = f"{type(e).__name__}: "
            self._error_manager.add_error(f"{prefix}{e}")
        finally:
            self._error_manager.report_errors(ClassiqExpansionError)

        return Model(
            constraints=self._model.constraints,
            preferences=self._model.preferences,
            classical_execution_code=self._model.classical_execution_code,
            execution_preferences=self._model.execution_preferences,
            functions=list(self._expanded_functions.values()),
            constants=self._model.constants,
            enums=self._model.enums,
            types=self._model.types,
            qstructs=self._model.qstructs,
            debug_info=self._model.debug_info,
            functions_compilation_metadata=self._expanded_functions_compilation_metadata,
        )

    @singledispatchmethod
    def evaluate(self, expression: Any) -> Evaluated:
        raise NotImplementedError(f"Cannot evaluate {expression!r}")

    @evaluate.register
    def evaluate_classical_expression(self, expression: Expression) -> Evaluated:
        return evaluate_classical_expression(expression, self._current_scope)

    @evaluate.register
    def evaluate_identifier(self, identifier: str) -> Evaluated:
        return self._current_scope[identifier]

    @evaluate.register
    def evaluate_lambda(self, function: QuantumLambdaFunction) -> Evaluated:
        renamed_params = [
            param.rename(function.pos_rename_params[idx])
            for idx, param in enumerate(function.func_decl.positional_arg_declarations)
        ]
        func_decl = NamedParamsQuantumFunctionDeclaration(
            name=function.func_decl.name or "<lambda>",
            positional_arg_declarations=renamed_params,
        )

        closure_class: type[FunctionClosure]
        extra_args: dict[str, Any]
        if function.is_generative():
            closure_class = GenerativeFunctionClosure
            extra_args = {
                "generative_blocks": {
                    "body": GenerativeQFunc(function.py_callable, func_decl),
                }
            }
        else:
            closure_class = FunctionClosure
            extra_args = {}

        return Evaluated(
            value=closure_class.create(
                name=func_decl.name,
                positional_arg_declarations=func_decl.positional_arg_declarations,
                body=function.body,
                scope=Scope(parent=self._current_scope),
                is_lambda=True,
                **extra_args,
            ),
            defining_function=self._builder.current_function,
        )

    @evaluate.register
    def evaluate_handle_binding(self, handle_binding: HandleBinding) -> Evaluated:
        return self.evaluate(handle_binding.name)

    @evaluate.register
    def evaluate_sliced_handle_binding(
        self, sliced_handle_binding: SlicedHandleBinding
    ) -> Evaluated:
        quantum_variable = self.evaluate(sliced_handle_binding.base_handle).as_type(
            QuantumSymbol
        )
        start = self.evaluate(sliced_handle_binding.start).as_type(int)
        end = self.evaluate(sliced_handle_binding.end).as_type(int)
        return Evaluated(value=quantum_variable[start:end])

    @evaluate.register
    def evaluate_list(self, value: list) -> Evaluated:
        return Evaluated(value=[self.evaluate(arg).value for arg in value])

    @evaluate.register
    def evaluate_subscript_handle(self, subscript: SubscriptHandleBinding) -> Evaluated:
        base_value = self.evaluate(subscript.base_handle)
        index_value = self.evaluate(subscript.index).as_type(int)
        return Evaluated(value=base_value.value[index_value])

    @evaluate.register
    def evaluate_subscript_operand(self, subscript: OperandIdentifier) -> Evaluated:
        base_value = self.evaluate(subscript.name)
        index_value = self.evaluate(subscript.index).as_type(int)
        return Evaluated(value=base_value.value[index_value])

    @evaluate.register
    def evaluate_field_access(self, field_access: FieldHandleBinding) -> Evaluated:
        base_value = self.evaluate(field_access.base_handle)
        return Evaluated(value=base_value.value.fields[field_access.field])

    @singledispatchmethod
    def emit(self, statement: QuantumStatement) -> None:
        raise NotImplementedError(f"Cannot emit {statement!r}")

    @emit.register
    def emit_quantum_function_call(self, call: QuantumFunctionCall) -> None:
        QuantumFunctionCallEmitter(self).emit(call)

    @emit.register
    def emit_bind(self, bind: BindOperation) -> None:
        BindEmitter(self).emit(bind)

    @emit.register
    def emit_quantum_assignment_operation(self, op: QuantumAssignmentOperation) -> None:
        QuantumAssignmentOperationEmitter(self).emit(op)

    @emit.register
    def emit_inplace_binary_operation(self, operation: InplaceBinaryOperation) -> None:
        InplaceBinaryOperationEmitter(self).emit(operation)

    @emit.register
    def emit_variable_declaration(
        self, variable_declaration: VariableDeclarationStatement
    ) -> None:
        VariableDeclarationStatementEmitter(self).emit(variable_declaration)

    @emit.register
    def emit_classical_if(self, classical_if: ClassicalIf) -> None:
        ClassicalIfEmitter(self).emit(classical_if)

    @emit.register
    def emit_within_apply(self, within_apply: WithinApply) -> None:
        WithinApplyEmitter(self).emit(within_apply)

    @emit.register
    def emit_invert(self, invert: Invert) -> None:
        InvertEmitter(self).emit(invert)

    @emit.register
    def emit_repeat(self, repeat: Repeat) -> None:
        RepeatEmitter(self).emit(repeat)

    @emit.register
    def emit_control(self, control: Control) -> None:
        ControlEmitter(self).emit(control)

    @emit.register
    def emit_power(self, power: Power) -> None:
        PowerEmitter(self).emit(power)

    @emit.register
    def emit_phase(self, phase: PhaseOperation) -> None:
        PhaseEmitter(self).emit(phase)

    def _expand_block(self, block: Sequence[QuantumStatement], block_name: str) -> None:
        with self._builder.block_context(block_name):
            for statement in block:
                self.emit_statement(statement)

    def emit_statement(self, statement: QuantumStatement) -> None:
        source_ref = statement.source_ref
        error_context = (
            self._error_manager.node_context(statement)
            if source_ref is not None
            else nullcontext()
        )
        with error_context, self._builder.source_ref_context(source_ref):
            self.emit(statement)

    def _expand_operation(self, operation: Closure) -> OperationContext:
        with self._builder.operation_context(operation) as context:
            if isinstance(operation, FunctionClosure) and (
                self._expanded_functions.get(operation.closure_id) is not None
            ):
                pass
            elif isinstance(operation, FunctionClosure) and operation.name == "permute":
                # special expansion since permute is generative
                with self._scope_guard(operation.scope):
                    self._expand_permute()
            elif isinstance(operation, GenerativeClosure):
                with self._scope_guard(operation.scope):
                    args = [
                        self.evaluate(param.name)
                        for param in operation.positional_arg_declarations
                    ]
                    emit_generative_statements(self, operation, args)
            else:
                for block, block_body in operation.blocks.items():
                    with self._scope_guard(operation.scope):
                        self._expand_block(block_body, block)

        return context

    def _expand_permute(self) -> None:
        functions = self.evaluate("functions").as_type(list)
        functions_permutation = permutation(np.array(range(len(functions))))
        calls: list[QuantumFunctionCall] = []
        for function_index in functions_permutation:
            permute_call = QuantumFunctionCall(
                function=OperandIdentifier(
                    name="functions", index=Expression(expr=f"{function_index}")
                )
            )
            permute_call.set_func_decl(permute.func_decl)
            calls.append(permute_call)
        self._expand_block(calls, "body")

    def _get_function_declarations(self) -> Sequence[QuantumFunctionDeclaration]:
        return (
            self._model.functions
            + [gen_func.func_decl for gen_func in self._generative_functions]
            + list(self._expanded_functions.values())
        )

    def add_constant(self, constant: Constant) -> None:
        add_constants_to_scope([constant], self._top_level_scope)
