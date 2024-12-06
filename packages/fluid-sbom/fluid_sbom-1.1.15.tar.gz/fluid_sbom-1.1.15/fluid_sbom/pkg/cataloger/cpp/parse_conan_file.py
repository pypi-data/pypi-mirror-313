import re
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


def get_conan_dep_info(dep_line: str) -> tuple[str, str]:
    product, version = re.sub(r"[\"\]\[]", "", dep_line).strip().split("@")[0].split("/")
    if "," in version:
        version = re.sub(r",(?=[<>=])", " ", version).split(",")[0]
    return product, version


def format_conan_lock_dep(
    dep_info: str,
    location: Location,
    is_dev: bool = False,
) -> Package | None:
    regex = r"^([a-zA-Z0-9\-_]+)\/([^\s@]+)"
    match = re.match(regex, dep_info)
    if match:
        name, version = cast(tuple[str, str], match.groups())
        return Package(
            name=name,
            version=version,
            type=PackageType.ConanPkg,
            locations=[location],
            p_url=package_url(name, version),
            metadata=None,
            language=Language.CPP,
            licenses=[],
            is_dev=is_dev,
        )
    return None


def parse_conan_file(
    _: Resolver | None,
    __: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    packages = []
    line_deps: bool = False
    is_dev = False
    for line_number, line in enumerate(reader.read_closer.read().splitlines(), 1):
        if re.search(r"^\[(tool|build)_requires\]$", line):
            line_deps = True
            is_dev = True
        elif not is_dev and line.startswith("[requires]"):
            line_deps = True
            is_dev = False
        elif line_deps:
            if not line or line.startswith("["):
                break
            pkg_name, pkg_version = get_conan_dep_info(line)
            location = deepcopy(reader.location)
            if location.coordinates:
                location.coordinates.line = line_number
            packages.append(
                Package(
                    name=pkg_name,
                    version=pkg_version,
                    type=PackageType.ConanPkg,
                    locations=[location],
                    p_url=package_url(pkg_name, pkg_version),
                    metadata=None,
                    language=Language.CPP,
                    licenses=[],
                    is_dev=is_dev,
                ),
            )
    return packages, []
