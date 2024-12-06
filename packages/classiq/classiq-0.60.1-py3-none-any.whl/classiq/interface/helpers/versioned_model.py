import pydantic

from classiq.interface._version import VERSION


class VersionedModel(pydantic.BaseModel):
    version: str = pydantic.Field(default=VERSION)
