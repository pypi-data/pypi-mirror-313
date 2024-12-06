from typing import (
    NotRequired,
    TypedDict,
)

from fluid_sbom.internal.package_information.api_interface import (
    make_get,
)


class PubSpec(TypedDict):
    author: NotRequired[str]


class PubPackageVersion(TypedDict):
    archive_sha256: str
    archive_url: str
    published: str
    pubspec: PubSpec
    version: str


class PubPackage(TypedDict):
    latest: PubPackageVersion
    name: str
    versions: list[PubPackageVersion]


def get_pub_package(package_name: str) -> PubPackage | None:
    url = f"https://pub.dev/api/packages/{package_name}"
    package_info = make_get(url, timeout=30, headers={"Accept": "gzip"})
    return package_info
