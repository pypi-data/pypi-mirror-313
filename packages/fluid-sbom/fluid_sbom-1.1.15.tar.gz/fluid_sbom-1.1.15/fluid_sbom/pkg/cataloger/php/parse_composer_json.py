from collections.abc import ItemsView
from typing import (
    cast,
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
from fluid_sbom.pkg.cataloger.php.package import (
    package_url,
)


def _get_location(location: Location, sourceline: int) -> Location:
    if location.coordinates:
        c_upd = {"line": sourceline}
        l_upd = {"coordinates": location.coordinates.model_copy(update=c_upd)}
        return location.model_copy(update=l_upd)
    return location


def _get_packages(
    reader: LocationReadCloser,
    dependencies: IndexedDict | None,
    is_dev: bool,
) -> list[Package]:
    if dependencies is None:
        return []

    general_location = _get_location(reader.location, dependencies.position.start.line)
    items: ItemsView[str, str] = dependencies.items()
    return [
        Package(
            name=name,
            version=version,
            locations=[general_location],
            language=Language.PHP,
            licenses=[],
            type=PackageType.PhpComposerPkg,
            p_url=package_url(name, version),
            is_dev=is_dev,
        )
        for name, version in items
    ]


def parse_composer_json(
    _: Resolver | None,
    __: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    content = cast(IndexedDict, parse_json_with_tree_sitter(reader.read_closer.read()))
    deps: IndexedDict | None = content.get("require")
    dev_deps: IndexedDict | None = content.get("require-dev")
    packages = [
        *_get_packages(reader, deps, is_dev=False),
        *_get_packages(reader, dev_deps, is_dev=True),
    ]
    return packages, []
