from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from classiq.interface.executor.execution_request import JobCost
from classiq.interface.jobs import JobStatus


class ExecutionJobDetailsV1(BaseModel, extra="ignore"):
    id: str

    name: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None

    provider: Optional[str] = None
    backend_name: Optional[str] = None

    status: JobStatus

    num_shots: Optional[int] = None
    program_id: Optional[str] = None

    error: Optional[str] = None

    cost: Optional[JobCost] = Field(default=None)


class ExecutionJobsQueryResultsV1(BaseModel, extra="ignore"):
    results: list[ExecutionJobDetailsV1]
