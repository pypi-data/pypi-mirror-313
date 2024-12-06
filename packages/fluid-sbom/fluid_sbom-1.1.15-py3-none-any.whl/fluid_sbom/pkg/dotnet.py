from pydantic import (
    BaseModel,
)


class DotnetDepsEntry(BaseModel):
    name: str
    version: str
    path: str
    sha512: str
    hash_path: str


class DotnetPortableExecutableEntry(BaseModel):
    assembly_version: str | None = None
    legal_copyright: str | None = None
    company_name: str | None = None
    product_name: str | None = None
    product_version: str | None = None
    comments: str | None = None
    internal_name: str | None = None
