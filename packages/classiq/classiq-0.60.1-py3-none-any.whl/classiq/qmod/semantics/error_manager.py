from collections.abc import Iterator
from contextlib import contextmanager
from typing import Optional

from classiq.interface.ast_node import ASTNode
from classiq.interface.exceptions import CLASSIQ_SLACK_COMMUNITY_LINK
from classiq.interface.source_reference import SourceReferencedError


class ErrorManager:
    def __new__(cls) -> "ErrorManager":
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "_instantiated"):
            return
        self._instantiated = True
        self._errors: list[SourceReferencedError] = []
        self._current_nodes_stack: list[ASTNode] = []
        self._call_stack: list[str] = []
        self._ignore_errors: bool = False

    @contextmanager
    def ignore_errors_context(self) -> Iterator[None]:
        previous = self._ignore_errors
        self._ignore_errors = True
        try:
            yield
        finally:
            self._ignore_errors = previous

    @property
    def annotated_errors(self) -> list[str]:
        return [str(error) for error in self._errors]

    def add_error(self, error: str) -> None:
        if not self._ignore_errors:
            self._errors.append(
                SourceReferencedError(
                    error=error.replace(CLASSIQ_SLACK_COMMUNITY_LINK, ""),
                    source_ref=(
                        self._current_nodes_stack[-1].source_ref
                        if self._current_nodes_stack
                        else None
                    ),
                    function=self.current_function,
                )
            )

    def get_errors(self) -> list[SourceReferencedError]:
        return self._errors

    def clear(self) -> None:
        self._current_nodes_stack = []
        self._errors = []

    def has_errors(self) -> bool:
        return len(self._errors) > 0

    def report_errors(self, error_type: type[Exception]) -> None:
        if self.has_errors():
            errors = self.annotated_errors
            self.clear()
            raise error_type("\n\t" + "\n\t".join(errors))

    @property
    def current_function(self) -> Optional[str]:
        return self._call_stack[-1] if self._call_stack else None

    @contextmanager
    def node_context(self, node: ASTNode) -> Iterator[None]:
        self._current_nodes_stack.append(node)
        yield
        self._current_nodes_stack.pop()

    @contextmanager
    def call(self, func_name: str) -> Iterator[None]:
        self._call_stack.append(func_name)
        yield
        self._call_stack.pop()


def append_error(node: ASTNode, message: str) -> None:
    instance = ErrorManager()
    with instance.node_context(node):
        instance.add_error(message)
