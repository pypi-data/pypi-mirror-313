import logging
from copy import (
    deepcopy,
)
from typing import (
    cast,
)

from fluid_sbom.artifact.relationship import (
    Relationship,
    RelationshipType,
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
from fluid_sbom.pkg.cataloger.php.package import (
    new_package_from_composer,
)

LOGGER = logging.getLogger(__name__)


def parse_composer_lock(
    _: Resolver | None,
    __: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    try:
        package_json: IndexedDict = cast(
            IndexedDict,
            parse_json_with_tree_sitter(reader.read_closer.read()),
        )
    except ValueError:
        return [], []
    packages: list[Package] = []
    relationships: list[Relationship] = []

    for is_dev, package in [
        *[(False, x) for x in package_json.get("packages", [])],
        *[(True, x) for x in package_json.get("packages-dev", [])],
    ]:
        new_location = deepcopy(reader.location)

        if pkg := new_package_from_composer(package, new_location, is_dev):
            packages.append(pkg)

    for package in packages:
        for dep_name in package.metadata.require or []:
            package_dep = next((x for x in packages if x.name == dep_name), None)
            if package_dep:
                relationships.append(
                    Relationship(
                        from_=package,
                        to_=package_dep,
                        type=RelationshipType.DEPENDENCY_OF_RELATIONSHIP,
                        data=None,
                    ),
                )
    return packages, relationships
