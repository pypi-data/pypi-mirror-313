import logging

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
from fluid_sbom.internal.collection import (
    toml,
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
from fluid_sbom.pkg.cataloger.python.package import (
    package_url,
)
from fluid_sbom.pkg.python import (
    PythonRequirementsEntry,
)

LOGGER = logging.getLogger(__name__)


def _get_location(location: Location, sourceline: int) -> Location:
    if location.coordinates:
        c_upd = {"line": sourceline}
        l_upd = {"coordinates": location.coordinates.model_copy(update=c_upd)}
        return location.model_copy(update=l_upd)
    return location


def parse_poetry_lock(
    _resolver: Resolver | None,
    _env: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    _content = reader.read_closer.read()

    toml_content: IndexedDict = toml.parse_toml_with_tree_sitter(_content)

    if not toml_content:
        return [], []

    packages = _parse_packages(toml_content, reader)
    relationships = _parse_relationships(toml_content, packages)

    return packages, relationships


def _parse_packages(toml_content: IndexedDict, reader: LocationReadCloser) -> list[Package]:
    packages = []

    for package in toml_content.get("package", []):
        name: str | None = package.get("name")
        version: str | None = package.get("version")

        if not name or not version:
            continue

        p_url = package_url(name, version, package)

        location = (
            _get_location(reader.location, package.position.start.line)
            if isinstance(package, IndexedDict)
            else reader.location
        )

        try:
            packages.append(
                Package(
                    name=name,
                    version=version,
                    found_by=None,
                    locations=[location],
                    language=Language.PYTHON,
                    p_url=p_url,
                    metadata=PythonRequirementsEntry(
                        name=name,
                        extras=[],
                        markers=p_url,
                    ),
                    licenses=[],
                    type=PackageType.PythonPkg,
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

    return packages


def _parse_relationships(
    toml_content: IndexedDict,
    packages: list[Package],
) -> list[Relationship]:
    relationships = []

    for package in toml_content.get("package", []):
        _pkg = next((pkg for pkg in packages if pkg.name == package["name"]), None)
        dependencies = list(package.get("dependencies", {}).keys())

        if _pkg and dependencies:
            for dep in dependencies:
                dep_pkg = next((pkg for pkg in packages if pkg.name == dep), None)
                if dep_pkg:
                    relationships.append(
                        Relationship(
                            from_=dep_pkg,
                            to_=_pkg,
                            type=RelationshipType.DEPENDENCY_OF_RELATIONSHIP,
                            data=None,
                        ),
                    )

    return relationships
