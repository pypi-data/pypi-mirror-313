import pydantic


class ResourceEstimatorParams(pydantic.BaseModel):
    circuit_id: str
    error_budget: float
    physical_error_rate: float
