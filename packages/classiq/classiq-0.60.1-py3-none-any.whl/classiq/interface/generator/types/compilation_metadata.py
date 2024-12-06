from pydantic import BaseModel, Field


class CompilationMetadata(BaseModel):
    should_synthesize_separately: bool = Field(default=False)
