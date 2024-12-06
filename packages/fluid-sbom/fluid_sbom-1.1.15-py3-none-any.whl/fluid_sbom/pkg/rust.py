from pydantic import (
    BaseModel,
)


class RustCargoLockEntry(BaseModel):
    name: str
    version: str
    source: str | None
    checksum: str | None
    dependencies: list[str]
