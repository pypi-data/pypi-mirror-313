from typing import (
    NotRequired,
    TypedDict,
)

from retry_requests import (  # type: ignore
    retry,
)

from fluid_sbom.internal.cache import (
    dual_cache,
)


class NPMPackageAuthor(TypedDict):
    email: str
    name: str


class NPMPackageDist(TypedDict):
    integrity: str
    tarball: str


class NPMPackageLicense(TypedDict):
    type: str
    url: str


class NPMPackageVersion(TypedDict):
    dist: NPMPackageDist
    name: str


class NPMPackageTimeUnpublished(TypedDict):
    time: str
    versions: list[str]


NPMPackage = TypedDict(
    "NPMPackage",
    {
        "author": NotRequired[str | NPMPackageAuthor],
        "dist-tags": NotRequired[dict[str, str]],
        "license": str | NPMPackageLicense,
        "name": str,
        "time": dict[str, str],
        "versions": dict[str, NPMPackageVersion],
    },
)


@dual_cache
def get_npm_package(package_name: str) -> NPMPackage | None:
    response = retry().get(
        f"https://registry.npmjs.org/{package_name}",
        timeout=30,
    )
    if response.status_code != 200:
        return None

    package: NPMPackage = response.json()
    if "unpublished" in package["time"]:
        return None
    return package
