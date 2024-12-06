import logging
from collections.abc import ItemsView

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
from fluid_sbom.internal.collection.toml import (
    parse_toml_with_tree_sitter,
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

LOGGER = logging.getLogger(__name__)


def _get_location(location: Location, sourceline: int) -> Location:
    if location.coordinates:
        c_upd = {"line": sourceline}
        l_upd = {"coordinates": location.coordinates.model_copy(update=c_upd)}
        return location.model_copy(update=l_upd)
    return location


def _get_version(value: IndexedDict | str) -> str | None:
    if isinstance(value, str):
        return value
    version: str | None = value.get("version")
    return version


def _get_packages(
    reader: LocationReadCloser,
    dependencies: IndexedDict | None,
) -> list[Package]:
    if dependencies is None:
        return []

    packages: list[Package] = []

    items: ItemsView[str, IndexedDict | str] = dependencies.items()

    for name, value in items:
        version = _get_version(value)
        if not name or not version:
            continue

        location = _get_location(
            reader.location,
            dependencies.get_key_position(name).start.line,
        )

        try:
            packages.append(
                Package(
                    name=name,
                    version=version,
                    locations=[location],
                    language=Language.PYTHON,
                    licenses=[],
                    p_url=package_url(
                        name=name,
                        version=version,
                        package=None,
                    ),
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


def parse_pyproject_toml(
    _: Resolver | None,
    __: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    content = parse_toml_with_tree_sitter(reader.read_closer.read())

    if not content:
        return [], []

    tool: IndexedDict | None = content.get("tool")
    poetry: IndexedDict | None = tool.get("poetry") if tool else None
    deps: IndexedDict | None = poetry.get("dependencies") if poetry else None
    packages = _get_packages(reader, deps)
    return packages, []
