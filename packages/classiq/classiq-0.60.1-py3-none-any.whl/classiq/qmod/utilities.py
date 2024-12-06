import dataclasses
import inspect
import itertools
import keyword
import sys
from enum import Enum as PythonEnum
from types import FrameType
from typing import Any, Literal, Optional, get_args, get_origin, overload

from classiq.interface.source_reference import SourceReference

DEFAULT_DECIMAL_PRECISION = 4


def mangle_keyword(name: str) -> str:
    if keyword.iskeyword(name):
        name = f"{name}_"
    return name


@overload
def unmangle_keyword(name: str) -> str:
    pass


@overload
def unmangle_keyword(name: None) -> None:
    pass


def unmangle_keyword(name: Optional[str]) -> Optional[str]:
    if name is None:
        return None
    if name[-1] == "_" and keyword.iskeyword(name[:-1]):
        name = name[:-1]
    return name


def version_portable_get_args(py_type: type) -> tuple:
    if get_origin(py_type) is None:
        return tuple()
    if sys.version_info[0:2] < (3, 10):
        type_args = get_args(py_type)  # The result of __class_getitem__
    else:
        type_args = get_args(py_type)[0]
    if not isinstance(type_args, tuple):
        return (type_args,)
    return tuple(
        (
            version_portable_get_args(type_arg)[0]
            if get_origin(type_arg) == Literal
            else type_arg
        )
        for type_arg in type_args
    )


def get_source_ref(frame: FrameType) -> SourceReference:
    filename = inspect.getfile(frame)
    lineno = frame.f_lineno
    if sys.version_info[0:2] < (3, 11) or frame.f_lasti < 0:
        source_ref = SourceReference(
            file_name=filename,
            start_line=lineno - 1,
            start_column=-1,
            end_line=-1,
            end_column=-1,
        )
    else:
        positions_gen = frame.f_code.co_positions()
        positions = next(itertools.islice(positions_gen, frame.f_lasti // 2, None))
        source_ref = SourceReference(
            file_name=filename,
            start_line=(positions[0] or 0) - 1,
            start_column=(positions[2] or 0) - 1,
            end_line=(positions[1] or 0) - 1,
            end_column=(positions[3] or 0) - 1,
        )
    return source_ref


def qmod_val_to_expr_str(val: Any) -> str:
    if dataclasses.is_dataclass(type(val)):
        kwargs_str = ", ".join(
            [
                f"{field.name}={qmod_val_to_expr_str(vars(val)[field.name])}"
                for field in dataclasses.fields(val)
            ]
        )
        return f"struct_literal({type(val).__name__}, {kwargs_str})"

    if isinstance(val, list):
        elements_str = ", ".join([qmod_val_to_expr_str(elem) for elem in val])
        return f"[{elements_str}]"

    if isinstance(val, PythonEnum):
        return f"{type(val).__name__}.{val.name}"

    return str(val)
