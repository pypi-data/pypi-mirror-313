import re
from copy import (
    deepcopy,
)

from fluid_sbom.artifact.relationship import (
    Relationship,
)
from fluid_sbom.file.dependency_type import (
    DependencyType,
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
from fluid_sbom.pkg.cataloger.generic.parser import (
    Environment,
)

from .package import (
    package_url,
)

MIX_DEP: re.Pattern[str] = re.compile(
    r"\{:(?P<dep>[\w]*),\s\"~>\s(?P<version>[\d.]+)\".+",
)


def parse_mix_exs(
    _: Resolver | None,
    __: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    packages: list[Package] = []
    relationships: list[Relationship] = []
    is_line_deps = False

    for line_number, line in enumerate(
        reader.read_closer.read().splitlines(),
        1,
    ):
        line = line.strip()
        if line == "defp deps do":
            is_line_deps = True
        elif is_line_deps:
            if line == "end":
                break
            if matched := MIX_DEP.match(line):
                is_dev = ":dev" in line
                pkg_name = matched.group("dep")
                pkg_version = matched.group("version")
                location = deepcopy(reader.location)
                if location.coordinates:
                    location.coordinates.line = line_number
                    location.dependency_type = DependencyType.DIRECT

                packages.append(
                    Package(
                        name=pkg_name,
                        version=pkg_version,
                        type=PackageType.HexPkg,
                        locations=[location],
                        p_url=package_url(pkg_name, pkg_version),
                        metadata=None,
                        language=Language.ELIXIR,
                        licenses=[],
                        is_dev=is_dev,
                    ),
                )
    return packages, relationships
