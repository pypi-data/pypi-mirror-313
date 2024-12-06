from pydantic import (
    BaseModel,
)


class ElixirMixLockEntry(BaseModel):
    name: str
    version: str
    pkg_hash: str
    pkg_hash_ext: str
