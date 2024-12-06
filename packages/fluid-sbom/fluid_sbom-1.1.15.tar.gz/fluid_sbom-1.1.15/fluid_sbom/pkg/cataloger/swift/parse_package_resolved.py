import logging
from copy import (
    deepcopy,
)
from typing import (
    cast,
)

from fluid_sbom.artifact.relationship import (
    Relationship,
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
    Package,
)
from fluid_sbom.pkg.cataloger.generic.parser import (
    Environment,
)
from fluid_sbom.pkg.cataloger.swift.package import (
    new_swift_package_manager_package,
)

LOGGER = logging.getLogger(__name__)


def parse_package_resolved(
    _: Resolver | None,
    __: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    try:
        package_resolved: IndexedDict = cast(
            IndexedDict,
            parse_json_with_tree_sitter(reader.read_closer.read()),
        )
    except ValueError:
        return [], []

    packages: list[Package] = []
    relationships: list[Relationship] = []
    package_resolved_pins = package_resolved.get("pins")

    if package_resolved_pins:
        for pin in package_resolved_pins:
            state = pin.get("state", {})
            name = pin.get("identity")
            version = state.get("version")

            if not name or not version:
                continue

            new_location = deepcopy(reader.location)
            if new_location.coordinates:
                new_location.coordinates.line = pin.position.start.line

            if pkg := new_swift_package_manager_package(
                name=name,
                version=version,
                source_url=pin.get("location"),
                revision=state.get("revision"),
                location=new_location,
            ):
                packages.append(pkg)

    return packages, relationships
