import logging
import re
from copy import (
    deepcopy,
)
from typing import (
    Any,
    cast,
)

from pydantic import (
    ValidationError,
)

from fluid_sbom.artifact.relationship import (
    Relationship,
    RelationshipType,
)
from fluid_sbom.file.dependency_type import (
    DependencyType,
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
from fluid_sbom.internal.collection.types import (
    IndexedDict,
)
from fluid_sbom.internal.collection.yaml import (
    parse_yaml_with_tree_sitter,
)
from fluid_sbom.model.core import (
    Language,
    Package,
    PackageType,
)
from fluid_sbom.pkg.cataloger.generic.parser import (
    Environment,
)
from fluid_sbom.pkg.cataloger.javascript.package import (
    package_url,
)
from fluid_sbom.pkg.npm import (
    PnpmEntry,
)
from fluid_sbom.utils.file import (
    Digest,
)

LOGGER = logging.getLogger(__name__)


def extract_package_name_from_key_dependency(item: str) -> str | None:
    # Regex pattern to extract the package name
    pattern = r"^@?[\w-]+/[\w-]+$"
    match = re.match(pattern, item)
    if match:
        return match.group(0)
    return None


def extract_version_from_value_dependency(item: str) -> str | None:
    # Regex pattern to extract the version number before any parentheses
    pattern = r"^(\d+\.\d+\.\d+)"
    match = re.match(pattern, item)
    if match:
        return match.group(1)
    return None


def _get_package(
    packages: list[Package],
    dep_name: str | None,
    dep_version: str | None,
) -> Package | None:
    return next(
        (x for x in packages if x.name == dep_name and x.version == dep_version),
        None,
    )


def _generate_relations_relationship(
    package_yaml: IndexedDict[str, IndexedDict[str, Any]],
    packages: list[Package],
) -> list[Relationship]:
    relationships: list[Relationship] = []
    for package_key, package_value in package_yaml["packages"].items():
        if match_ := re.search(r"/(@?[^@]+)@(\d+\.\d+\.\d+)", package_key):
            package_name = match_.groups()[0]
            package_version = match_.groups()[1]
            current_package = _get_package(
                packages,
                dep_name=package_name,
                dep_version=package_version,
            )
            dependencies: IndexedDict[str, str]
            if dependencies := package_value.get("dependencies"):
                for dep_name, dep_version in dependencies.items():
                    dep_name = extract_package_name_from_key_dependency(
                        dep_name,
                    )
                    dep_version = extract_version_from_value_dependency(
                        dep_version,
                    )
                    if dep := _get_package(
                        packages,
                        dep_name,
                        dep_version,
                    ):
                        relationships.append(
                            Relationship(
                                from_=dep,
                                to_=current_package,
                                type=(RelationshipType.DEPENDENCY_OF_RELATIONSHIP),
                                data=None,
                            ),
                        )
    return relationships


def _get_package_metadata(
    package_value: dict[str, bool | dict[str, str]],
) -> PnpmEntry:
    is_dev_value = package_value.get("dev")

    resolution_value = package_value.get("resolution")
    integrity_value = (
        resolution_value.get("integrity") if isinstance(resolution_value, dict) else None
    )

    return PnpmEntry(
        is_dev=is_dev_value if isinstance(is_dev_value, bool) else False,
        integrity=Digest(
            algorithm="sha-512",
            value=integrity_value,
        ),
    )


def manage_coordinates(
    package_yaml: IndexedDict,
    package_key: str,
    package_name: str,
    direct_dependencies: list,
    base_location: Location,
) -> Location:
    current_location = deepcopy(base_location)
    if current_location.coordinates:
        position = package_yaml["packages"].get_key_position(package_key)
        current_location.coordinates.line = position.start.line
        is_transitive = package_name not in direct_dependencies
        current_location.dependency_type = (
            DependencyType.TRANSITIVE if is_transitive else DependencyType.DIRECT
        )
    return current_location


def parse_pnpm_lock(
    _: Resolver | None,
    __: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    package_yaml: IndexedDict = cast(
        IndexedDict,
        parse_yaml_with_tree_sitter(reader.read_closer.read()),
    )

    if not package_yaml:
        return [], []

    dependencies = list(package_yaml.get("dependencies", {}))
    dev_dependencies = list(package_yaml.get("devDependencies", {}))
    direct_dependencies = [*dev_dependencies, *dependencies]

    packages: list[Package] = []
    relationships: list[Relationship] = []
    for package_key, _package_value in package_yaml["packages"].items():
        if match_ := re.search(r"/(@?[^@]+)@(\d+\.\d+\.\d+)", package_key):
            package_name = match_.groups()[0]
            package_version = match_.groups()[1]

            if not package_name or not package_version:
                continue

            current_location: Location = manage_coordinates(
                package_yaml,
                package_key,
                package_name,
                direct_dependencies,
                reader.location,
            )

            try:
                packages.append(
                    Package(
                        name=package_name,
                        version=package_version,
                        locations=[current_location],
                        language=Language.JAVASCRIPT,
                        licenses=[],
                        type=PackageType.NpmPkg,
                        p_url=package_url(package_name, package_version),
                        metadata=_get_package_metadata(_package_value),
                    ),
                )
            except ValidationError as ex:
                LOGGER.warning(
                    "Malformed package. Required fields are missing or data "
                    "types are incorrect.",
                    extra={
                        "extra": {
                            "exception": ex.errors(include_url=False),
                            "location": current_location.path(),
                        },
                    },
                )
                continue

    relationships = _generate_relations_relationship(package_yaml, packages)

    return packages, relationships
