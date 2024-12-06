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
from fluid_sbom.file.location import (
    Location,
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


def _load_package_json(
    reader: LocationReadCloser,
) -> IndexedDict | None:
    try:
        return cast(IndexedDict, parse_json_with_tree_sitter(reader.read_closer.read()))
    except ValueError:
        return None


def _extract_packages(package_json: IndexedDict, location: Location) -> list[Package]:
    packages = []
    if isinstance(package_json, IndexedDict) and "dev-package-names" in package_json:
        dev_packages = package_json["dev-package-names"]
    else:
        dev_packages = []

    if "packages" in package_json:
        packages_list = package_json["packages"]
    else:
        packages_list = package_json

    for package in packages_list:
        pkg_item = new_package_from_composer(package, deepcopy(location), False)
        if pkg_item:
            pkg_item.is_dev = pkg_item.name in dev_packages
            packages.append(pkg_item)

    return packages


def _extract_relationships(packages: list[Package]) -> list[Relationship]:
    relationships = []
    for package in packages:
        package_metadata = getattr(package.metadata, "require", None)
        dependencies = list(package_metadata.keys()) if package_metadata else []
        for dep_name in dependencies:
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

    return relationships


def parse_installed_json(
    _: Resolver | None,
    __: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    package_json = _load_package_json(reader)

    if not package_json:
        return [], []

    packages = _extract_packages(package_json, reader.location)
    relationships = _extract_relationships(packages)

    return packages, relationships
