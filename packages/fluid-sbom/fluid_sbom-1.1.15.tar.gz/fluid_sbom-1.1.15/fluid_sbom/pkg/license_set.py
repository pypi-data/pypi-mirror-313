from pydantic import (
    BaseModel,
)


class LicenseSet(BaseModel):
    set: dict[str, str]
