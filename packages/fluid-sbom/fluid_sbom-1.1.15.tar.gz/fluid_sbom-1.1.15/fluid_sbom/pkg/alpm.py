from datetime import (
    datetime,
)

from pydantic import (
    BaseModel,
)

from fluid_sbom.utils.file import (
    Digest,
)


class AlpmFileRecord(BaseModel):
    path: str
    type: str | None = None
    uid: str | None = None
    gid: str | None = None
    time: datetime | None = None
    size: str | None = None
    link: str | None = None
    digests: list[Digest] | None = None


class AlpmDBEntry(BaseModel):  # pylint:disable=too-many-instance-attributes
    licenses: str = ""
    base_package: str = ""
    package: str = ""
    version: str = ""
    description: str = ""
    architecture: str = ""
    size: int = 0
    packager: str = ""
    url: str = ""
    validation: str = ""
    reason: int = 0
    files: list[AlpmFileRecord] | None = None
    backup: list[AlpmFileRecord] | None = None

    def owned_files(self) -> list[str]:
        seen = set()
        result = []
        for file_record in self.files or []:
            if file_record.path and file_record.path not in seen:
                seen.add(file_record.path)
                result.append(file_record.path)
        result.sort()
        return result
