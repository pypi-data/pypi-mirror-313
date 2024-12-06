from copy import (
    deepcopy,
)
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
    IndexedList,
)
from fluid_sbom.model.core import (
    Language,
    Package,
    PackageType,
)
from fluid_sbom.pkg.cataloger.cpp.package import (
    package_url,
)
from fluid_sbom.pkg.cataloger.generic.parser import (
    Environment,
)


def format_conan_lock_dep(dep_info: str, location: Location, is_dev: bool = False) -> Package:
    product, version = dep_info.split("/")
    version = version.split("#")[0]
    return Package(
        name=product,
        version=version,
        type=PackageType.ConanPkg,
        locations=[location],
        p_url=package_url(product, version),
        metadata=None,
        language=Language.CPP,
        licenses=[],
        is_dev=is_dev,
    )


def parse_conan_lock(
    _: Resolver | None,
    __: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    packages = []
    conan_file = cast(
        IndexedDict[str, IndexedList[str]],
        parse_json_with_tree_sitter(reader.read_closer.read()),
    )
    for index, dep_line in enumerate(conan_file["requires"]):
        location = deepcopy(reader.location)
        if location.coordinates:
            location.coordinates.line = (
                conan_file["requires"]
                .get_position(
                    index,
                )
                .start.line
            )
        packages.append(
            format_conan_lock_dep(dep_line, location),
        )
    for index, dep_line in enumerate(
        conan_file["build_requires"],
    ):
        location = deepcopy(reader.location)
        if location.coordinates:
            location.coordinates.line = conan_file["build_requires"].get_position(index).start.line
        packages.append(
            format_conan_lock_dep(dep_line, location, True),
        )
    return packages, []
