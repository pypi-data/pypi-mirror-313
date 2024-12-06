import logging

from packageurl import (
    PackageURL,
)
from pydantic import (
    ValidationError,
)

from fluid_sbom.file.location import (
    Location,
)
from fluid_sbom.model.core import (
    Language,
    Package,
    PackageType,
)
from fluid_sbom.pkg.cocoapods import (
    CocoaPodfileLockEntry,
)
from fluid_sbom.pkg.swift import (
    SwiftPackageManagerResolvedEntry,
)

LOGGER = logging.getLogger(__name__)


def new_cocoa_pods_package(
    name: str,
    version: str,
    hash_: str,
    location: Location,
) -> Package | None:
    try:
        return Package(
            name=name,
            version=version,
            p_url=cocoapods_package_url(name, version),
            locations=[location],
            type=PackageType.CocoapodsPkg,
            language=Language.SWIFT,
            metadata=CocoaPodfileLockEntry(checksum=hash_),
            licenses=[],
        )
    except ValidationError as ex:
        LOGGER.warning(
            "Malformed package. Required fields are missing or data types are incorrect.",
            extra={
                "extra": {
                    "exception": ex.errors(include_url=False),
                    "location": location.path(),
                },
            },
        )
        return None


def new_swift_package_manager_package(
    *,
    name: str,
    version: str,
    source_url: str | None,
    revision: str | None,
    location: Location,
) -> Package | None:
    if not name or not version:
        return None

    try:
        return Package(
            name=name,
            version=version,
            p_url=swift_package_manager_package_url(name, version, source_url),
            locations=[location],
            type=PackageType.SwiftPkg,
            language=Language.SWIFT,
            metadata=SwiftPackageManagerResolvedEntry(revision=revision) if revision else None,
            licenses=[],
        )
    except ValidationError as ex:
        LOGGER.warning(
            "Malformed package. Required fields are missing or data types are incorrect.",
            extra={
                "extra": {
                    "exception": ex.errors(include_url=False),
                    "location": location.path(),
                },
            },
        )
        return None


def cocoapods_package_url(
    name: str,
    version: str,
) -> str:
    return PackageURL("cocoapods", "", name, version, None, "").to_string()


def swift_package_manager_package_url(
    name: str,
    version: str,
    source_url: str | None,
) -> str:
    return PackageURL(
        "swift",
        source_url.replace("https://", "", 1) if source_url else "",
        name,
        version,
        None,
        "",
    ).to_string()
