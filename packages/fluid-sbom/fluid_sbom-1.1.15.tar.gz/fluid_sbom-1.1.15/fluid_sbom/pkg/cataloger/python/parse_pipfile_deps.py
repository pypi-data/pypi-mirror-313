import logging

from pydantic import (
    ValidationError,
)

from fluid_sbom.artifact.relationship import (
    Relationship,
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
    PythonPackage,
)

LOGGER = logging.getLogger(__name__)


def _get_location(location: Location, sourceline: int) -> Location:
    if location.coordinates:
        c_upd = {"line": sourceline}
        l_upd = {"coordinates": location.coordinates.model_copy(update=c_upd)}
        return location.model_copy(update=l_upd)
    return location


def parse_pipfile_deps(
    _resolver: Resolver | None,
    _env: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    packages = []
    file_content = reader.read_closer.read()
    toml_content = toml.parse_toml_with_tree_sitter(file_content)
    toml_packages = toml_content.get("packages", {})
    for package, version_data in toml_packages.items():
        version = (
            version_data if isinstance(version_data, str) else version_data.get("version", "*")
        ).strip("=<>~^ ")

        if not package or not version or "*" in version:
            continue

        try:
            packages.append(
                Package(
                    name=package,
                    version=version,
                    locations=[
                        (
                            _get_location(reader.location, package.position.start.line)
                            if isinstance(package, IndexedDict)
                            else reader.location
                        ),
                    ],
                    language=Language.PYTHON,
                    type=PackageType.PythonPkg,
                    metadata=PythonPackage(
                        name=package,
                        version=version,
                    ),
                    p_url=package_url(name=package, version=version, package=None),
                    licenses=[],
                ),
            )
        except ValidationError as ex:
            LOGGER.warning(
                "Malformed package. Required fields are missing or data types are incorrect.",
                extra={
                    "extra": {
                        "exception": ex.errors(include_url=False),
                        "location": reader.location.path(),
                    },
                },
            )
            continue
    return packages, []
