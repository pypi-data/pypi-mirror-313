import logging
from copy import (
    deepcopy,
)
from typing import (
    cast,
)

from more_itertools import (
    flatten,
)
from packageurl import (
    PackageURL,
)
from pydantic import (
    ValidationError,
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
    Language,
    Package,
    PackageType,
)
from fluid_sbom.pkg.cataloger.generic.parser import (
    Environment,
)

LOGGER = logging.getLogger(__name__)


def parse_dotnet_deps_json(
    _resolver: Resolver | None,
    _env: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    package_json: IndexedDict = cast(
        IndexedDict,
        parse_json_with_tree_sitter(reader.read_closer.read()),
    )
    packages: list[Package] = []
    relationships: list[Relationship] = []

    dependencies = {}
    for package_key, package_value in flatten(
        x.items() for x in package_json.get("targets", {}).values()
    ):
        package_name, version = package_key.split("/")

        location = deepcopy(reader.location)
        if location.coordinates:
            location.coordinates.line = package_value.position.start.line
        dependencies[package_name] = package_value.get("dependencies", {})
        try:
            packages.append(
                Package(
                    name=package_name,
                    version=version,
                    locations=[location],
                    licenses=[],
                    type=PackageType.DotnetPkg,
                    language=Language.DOTNET,
                    metadata=None,
                    p_url=PackageURL(
                        type="nuget",
                        namespace="",
                        name=package_name,
                        version=version,
                        qualifiers={},
                        subpath="",
                    ).to_string(),
                ),
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
            continue
    for package_name, depens in dependencies.items():
        deps = (p for p in packages for dep_name in depens.keys() if dep_name == p.name)
        if current_package := next((x for x in packages if x.name == package_name), None):
            relationships.extend(
                Relationship(
                    from_=x,
                    to_=current_package,
                    type=RelationshipType.DEPENDENCY_OF_RELATIONSHIP,
                    data=None,
                )
                for x in deps
            )
    return packages, relationships
