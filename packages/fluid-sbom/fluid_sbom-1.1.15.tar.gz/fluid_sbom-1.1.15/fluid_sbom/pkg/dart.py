from pydantic import (
    BaseModel,
)


class DartPubspecLickEntry(BaseModel):
    name: str
    version: str
    hosted_url: str
    vcs_url: str
