from collections.abc import Hashable
from enum import (
    Enum,
)
from typing import (
    Any,
)

from pydantic import (
    BaseModel,
    ConfigDict,
)


class RelationshipType(Enum):
    OWNERSHIP_BY_FILE_OVERLAP_RELATIONSHIP: str = "ownership-by-file-overlap"
    EVIDENT_BY_RELATIONSHIP: str = "evident-by"
    CONTAINS_RELATIONSHIP: str = "contains"
    DEPENDENCY_OF_RELATIONSHIP: str = "dependency-of"
    DESCRIBED_BY_RELATIONSHIP: str = "described-by"


class Relationship(BaseModel):
    from_: Hashable
    to_: Hashable
    type: RelationshipType
    data: Any
    model_config = ConfigDict(frozen=True)
