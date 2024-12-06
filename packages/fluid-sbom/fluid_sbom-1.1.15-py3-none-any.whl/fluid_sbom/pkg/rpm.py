from pydantic import (
    BaseModel,
)

from fluid_sbom.utils.file import (
    Digest,
)


class RpmFileRecord(BaseModel):
    path: str
    mode: int
    size: int
    digest: Digest
    username: str
    group_name: str | None
    flags: str


class RpmDBEntry(BaseModel):
    id_: str
    name: str
    version: str
    epoch: int | None
    arch: str
    release: str
    source_rpm: str
    size: int
    vendor: str
    modularitylabel: str
    files: list[RpmFileRecord]
