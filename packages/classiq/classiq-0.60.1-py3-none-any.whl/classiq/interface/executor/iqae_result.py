from pydantic import BaseModel, Field

from classiq.interface.executor.result import ExecutionDetails
from classiq.interface.generator.functions.classical_type import QmodPyObject
from classiq.interface.helpers.versioned_model import VersionedModel


class IQAEIterationData(BaseModel):
    grover_iterations: int
    sample_results: ExecutionDetails


class IQAEResult(VersionedModel, QmodPyObject):
    estimation: float
    confidence_interval: list[float] = Field(min_length=2, max_length=2)
    iterations_data: list[IQAEIterationData]
    warnings: list[str]
