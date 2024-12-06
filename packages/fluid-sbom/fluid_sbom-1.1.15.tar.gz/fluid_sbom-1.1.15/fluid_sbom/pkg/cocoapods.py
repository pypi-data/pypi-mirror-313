from pydantic import (
    BaseModel,
    ConfigDict,
)


class CocoaPodfileLockEntry(BaseModel):
    checksum: str
    model_config = ConfigDict(frozen=True)
