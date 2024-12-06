from classiq.interface.generator.function_param_library import FunctionParamLibrary
from classiq.interface.generator.oracles import ArithmeticOracle, CustomOracle

oracle_function_param_library: FunctionParamLibrary = FunctionParamLibrary(
    param_list=[ArithmeticOracle, CustomOracle]
)
