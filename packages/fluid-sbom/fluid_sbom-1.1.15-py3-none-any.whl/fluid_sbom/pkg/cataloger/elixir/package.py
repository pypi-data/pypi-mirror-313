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
from fluid_sbom.internal.package_information.elixir import (
    get_hex_package,
)
from fluid_sbom.model.core import (
    HealthMetadata,
    Language,
    Package,
    PackageType,
)
from fluid_sbom.pkg.elixir import (
    ElixirMixLockEntry,
)

LOGGER = logging.getLogger(__name__)


def new_package(entry: ElixirMixLockEntry, locations: Location) -> Package | None:
    name = entry.name
    version = entry.version

    if not name or not version:
        return None

    try:
        return Package(
            name=name,
            version=version,
            type=PackageType.HexPkg,
            locations=[locations],
            p_url=package_url(name, version),
            metadata=entry,
            language=Language.ELIXIR,
            licenses=[],
        )
    except ValidationError as ex:
        LOGGER.warning(
            "Malformed package. Required fields are missing or data types are incorrect.",
            extra={
                "extra": {
                    "exception": ex.errors(include_url=False),
                    "location": locations.path(),
                },
            },
        )
        return None


def package_url(name: str, version: str) -> str:
    return PackageURL(
        type="hex",
        namespace="",
        name=name,
        version=version,
        qualifiers=None,
        subpath="",
    ).to_string()


def complete_package(package: Package) -> Package:
    response = get_hex_package(package.name)
    if not response:
        return package
    package.health_metadata = HealthMetadata(
        latest_version=response["latest_stable_version"],
        latest_version_created_at=next(
            x["version"]
            for x in response["releases"]
            if x["version"] == response["latest_stable_version"]
        ),
    )
    if not package.licenses:
        package.licenses = response["meta"]["licenses"]
    if response["owners"]:
        package.health_metadata.authors = ", ".join([x["username"] for x in response["owners"]])
    return package
