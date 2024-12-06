import itertools

from classiq.interface.generator.function_param_library import FunctionParamLibrary
from classiq.interface.generator.function_param_list_without_self_reference import (
    function_param_library_without_self_reference,
)
from classiq.interface.generator.qpe import PhaseEstimation

function_param_library: FunctionParamLibrary = FunctionParamLibrary(
    param_list=itertools.chain(
        function_param_library_without_self_reference.param_list,
        {PhaseEstimation},
    )
)
