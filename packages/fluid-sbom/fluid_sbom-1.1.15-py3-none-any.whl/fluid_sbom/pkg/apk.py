from pydantic import (
    BaseModel,
)

from fluid_sbom.utils.file import (
    Digest,
)


class ApkFileRecord(BaseModel):
    path: str
    owner_uid: str | None = None
    owner_gid: str | None = None
    permissions: str | None = None
    digest: Digest | None = None


class ApkDBEntry(BaseModel):
    package: str
    origin_package: str | None
    maintainer: str | None
    version: str
    architecture: str | None
    url: str | None
    description: str | None
    size: str
    installed_size: str | None
    dependencies: list[str]
    provides: list[str]
    checksum: str | None
    git_commit: str | None
    files: list[ApkFileRecord]
