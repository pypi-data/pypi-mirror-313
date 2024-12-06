import logging
from copy import (
    deepcopy,
)
from typing import (
    TypedDict,
    cast,
)

from pydantic import (
    ValidationError,
)

from fluid_sbom.artifact.relationship import (
    Relationship,
    RelationshipType,
)
from fluid_sbom.file.location import (
    Location,
)
from fluid_sbom.file.location_read_closer import (
    LocationReadCloser,
)
from fluid_sbom.file.resolver import (
    Resolver,
)
from fluid_sbom.internal.collection.toml import (
    parse_toml_with_tree_sitter,
)
from fluid_sbom.internal.collection.types import (
    IndexedDict,
    IndexedList,
)
from fluid_sbom.model.core import (
    Language,
    Package,
    PackageType,
)
from fluid_sbom.pkg.cataloger.generic.parser import (
    Environment,
)
from fluid_sbom.pkg.cataloger.rust.package import (
    package_url,
)
from fluid_sbom.pkg.rust import (
    RustCargoLockEntry,
)

LOGGER = logging.getLogger(__name__)


class CargoLockEntry(TypedDict):
    name: str
    version: str
    source: str | None
    checksum: str | None
    dependencies: list[str]


class CargoLock(TypedDict):
    package: IndexedList[CargoLockEntry]


def _create_package(pkg: IndexedDict[str, str], location: Location) -> Package | None:
    name: str | None = pkg.get("name")
    version: str | None = pkg.get("version")

    if not name or not version:
        return None

    source: str | None = pkg.get("source")
    dependencies: IndexedList[str] | None = cast(IndexedList[str] | None, pkg.get("dependencies"))
    checksum: str | None = pkg.get("checksum")

    current_location = deepcopy(location)
    if current_location.coordinates and hasattr(pkg, "position"):
        current_location.coordinates.line = pkg.position.start.line

    try:
        return Package(
            name=name,
            version=version,
            locations=[current_location],
            language=Language.RUST,
            licenses=[],
            p_url=package_url(name, version),
            type=PackageType.RustPkg,
            metadata=RustCargoLockEntry(
                name=name,
                version=version,
                source=source,
                dependencies=list(dependencies or []),
                checksum=checksum,
            ),
        )
    except ValidationError as ex:
        LOGGER.warning(
            "Malformed package. Required fields are missing or data types are incorrect.",
            extra={
                "extra": {
                    "exception": ex.errors(include_url=False),  # type: ignore
                    "location": current_location.path(),
                },
            },
        )
        return None


def _create_relationships(packages: list[Package]) -> list[Relationship]:
    relationships = []
    for pkg in packages:
        if isinstance(pkg.metadata, RustCargoLockEntry):
            for dep_name in pkg.metadata.dependencies:
                if dep := next((x for x in packages if x.name == dep_name), None):
                    relationships.append(
                        Relationship(
                            from_=pkg,
                            to_=dep,
                            type=RelationshipType.DEPENDENCY_OF_RELATIONSHIP,
                            data=None,
                        ),
                    )
    return relationships


def parse_cargo_lock(
    _: Resolver | None,
    __: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    packages: list[Package] = []

    if not reader.location.coordinates:
        return packages, []

    _content = reader.read_closer.read()
    toml: IndexedDict[str, IndexedList[IndexedDict[str, str]] | None] = parse_toml_with_tree_sitter(
        _content,
    )
    if not toml:
        return [], []

    toml_pkgs: IndexedList[IndexedDict[str, str]] | None = toml.get("package")
    for pkg in toml_pkgs or []:
        if package := _create_package(pkg, reader.location):
            packages.append(package)

    relationships = _create_relationships(packages)

    return packages, relationships
