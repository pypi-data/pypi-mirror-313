from typing import Optional

from pydantic import BaseModel, Field

from classiq.interface.chemistry.operator import PauliOperator
from classiq.interface.executor.quantum_code import Arguments
from classiq.interface.helpers.custom_encoders import CUSTOM_ENCODERS


class EstimateInput(BaseModel, json_encoders=CUSTOM_ENCODERS):
    hamiltonian: PauliOperator
    parameters: list[Arguments]


class PrimitivesInput(BaseModel, json_encoders=CUSTOM_ENCODERS):
    sample: Optional[list[Arguments]] = Field(default=None)
    estimate: Optional[EstimateInput] = Field(default=None)
