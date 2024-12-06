from typing import Optional

import pydantic

from classiq.interface.helpers.hashable_pydantic_base_model import (
    HashablePydanticBaseModel,
)
from classiq.interface.source_reference import SourceReference


class ASTNode(HashablePydanticBaseModel):
    source_ref: Optional[SourceReference] = pydantic.Field(default=None)


class HashableASTNode(ASTNode, HashablePydanticBaseModel):
    pass
