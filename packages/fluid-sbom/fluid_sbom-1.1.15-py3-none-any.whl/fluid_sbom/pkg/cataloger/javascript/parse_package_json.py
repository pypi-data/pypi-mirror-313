import logging
from copy import (
    deepcopy,
)
from typing import (
    cast,
)

from pydantic import (
    ValidationError,
)

from fluid_sbom.artifact.relationship import (
    Relationship,
)
from fluid_sbom.file.dependency_type import (
    DependencyType,
)
from fluid_sbom.file.location_read_closer import (
    LocationReadCloser,
)
from fluid_sbom.file.resolver import (
    Resolver,
)
from fluid_sbom.internal.collection.json import (
    parse_json_with_tree_sitter,
)
from fluid_sbom.internal.collection.types import (
    IndexedDict,
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
    NpmPackage,
)
from fluid_sbom.utils.exceptions import (
    UnexpectedNodeError,
)

LOGGER = logging.getLogger(__name__)


def _create_package(
    package_json: IndexedDict,
    reader: LocationReadCloser,
    package_name: str,
    specifier: str,
    is_dev: bool,
) -> Package | None:
    current_location = deepcopy(reader.location)
    if current_location.coordinates:
        dependencies_key = "devDependencies" if is_dev else "dependencies"
        current_location.coordinates.line = (
            package_json[dependencies_key].get_key_position(package_name).start.line
        )
        current_location.dependency_type = DependencyType.DIRECT
    try:
        return Package(
            name=package_name,
            version=specifier,
            type=PackageType.NpmPkg,
            language=Language.JAVASCRIPT,
            licenses=[],
            locations=[current_location],
            p_url=package_url(package_name, specifier),
            metadata=NpmPackage(
                name=package_name,
                version=specifier,
                is_dev=is_dev,
            ),
            is_dev=is_dev,
        )
    except ValidationError as ex:
        LOGGER.warning(
            "Malformed package. Required fields are missing or data types are incorrect.",
            extra={
                "extra": {
                    "exception": ex.errors(include_url=False),
                    "location": current_location.path(),
                },
            },
        )
        return None


def parse_package_json(
    _: Resolver | None,
    __: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    try:
        package_json: IndexedDict = cast(
            IndexedDict,
            parse_json_with_tree_sitter(reader.read_closer.read()),
        )
    except (UnexpectedNodeError, ValueError):
        return [], []

    packages = []

    for package_name, specifier in package_json.get("dependencies", {}).items():
        if not package_name or not specifier:
            continue

        package = _create_package(package_json, reader, package_name, specifier, is_dev=False)
        if package:
            packages.append(package)

    for package_name, specifier in package_json.get("devDependencies", {}).items():
        if not package_name or not specifier:
            continue

        package = _create_package(package_json, reader, package_name, specifier, is_dev=True)
        if package:
            packages.append(package)

    return packages, []
