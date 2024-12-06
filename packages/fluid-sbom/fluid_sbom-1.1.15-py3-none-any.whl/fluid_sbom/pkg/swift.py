from pydantic import (
    BaseModel,
    ConfigDict,
)


class SwiftPackageManagerResolvedEntry(BaseModel):
    revision: str
    model_config = ConfigDict(frozen=True)
