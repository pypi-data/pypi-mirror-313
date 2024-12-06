import logging
import re
from copy import (
    deepcopy,
)
from typing import (
    NotRequired,
    TypedDict,
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
from fluid_sbom.model.core import (
    Language,
    Package,
    PackageType,
)
from fluid_sbom.pkg.cataloger.generic.parser import (
    Environment,
)
from fluid_sbom.pkg.cataloger.javascript.package import (
    package_url,
)
from fluid_sbom.pkg.npm import (
    YarnLockEntry,
)

LOGGER = logging.getLogger(__name__)


def _resolve_pair(line: str) -> tuple[str, str]:
    line = line.strip()
    if ": " in line:
        key, value = line.split(": ")
        return key.strip(), value.strip()

    key, value = line.split(" ", maxsplit=1)
    return key.strip(), value.strip()


def _count_indentation(line: str) -> int:
    # Stripping the leading spaces and comparing the length difference
    return len(line) - len(line.lstrip(" "))


def _is_list_item(
    current_package: str | None,
    current_key: str | None,
    current_indentation: int | None,
    line: str,
) -> bool:
    return bool(
        current_package
        and current_key
        and current_indentation
        and _count_indentation(line) > current_indentation,
    )


class YarnPackage(TypedDict):
    checksum: str
    dependencies: NotRequired[list[tuple[str, str]]]
    integrity: NotRequired[str]
    line: int
    resolution: NotRequired[str]
    resolved: NotRequired[str]
    version: str


def _parse_yarn_file(yarn_lock_content: str) -> dict[str, YarnPackage]:
    yarn_lock_lines = yarn_lock_content.strip().split("\n")

    # Dictionary to store the parsed yarn lock data
    parsed_yarn_lock = {}

    # Temporary variables for current package and dependencies
    current_package: str | None = None
    current_indentation = None
    current_key = None

    # Iterate through each line and parse the content
    for index, line in enumerate(yarn_lock_lines, 1):
        if not line:
            current_indentation = None
            continue
        if line.startswith("#"):
            continue
        if not line.startswith(" "):
            line = line.strip()
            if match_ := re.match(r'^"?((?:@\w[\w\-\.]*/)?\w[\w\-\.]*)@', line):
                current_package = match_.groups()[0]
                parsed_yarn_lock[current_package] = {"line": index}
            else:
                current_package = None
        elif current_package and ":" in line and line.strip().endswith(":"):
            current_indentation = _count_indentation(line)
            current_key = line.strip().split(":")[0]
            parsed_yarn_lock[current_package][current_key] = []  # type: ignore
        elif _is_list_item(
            current_package,
            current_key,
            current_indentation,
            line,
        ):
            parsed_yarn_lock[current_package][  # type: ignore
                current_key  # type: ignore
            ].append(_resolve_pair(line))
        elif current_package:
            current_indentation = None
            key, value = _resolve_pair(line)
            parsed_yarn_lock[current_package][key] = value.strip('"')  # type: ignore
    return parsed_yarn_lock  # type: ignore


def _get_name(pkg_name: str, item: YarnPackage) -> str:
    resolution = item.get("resolution")
    if resolution is None:
        return pkg_name

    is_scoped_package = resolution.startswith("@")
    if is_scoped_package:
        return f"@{resolution.split('@')[1]}"
    return resolution.split("@")[0]


def _extract_packages(parsed_yarn_lock: dict, reader: LocationReadCloser) -> list[Package]:
    packages = []
    for pkg_name, item in parsed_yarn_lock.items():
        name = _get_name(pkg_name, item)
        version = item.get("version")

        if not name or not version:
            continue

        current_location = deepcopy(reader.location)
        if current_location.coordinates:
            current_location.coordinates.line = item["line"]
        try:
            packages.append(
                Package(
                    name=name,
                    version=version,
                    locations=[current_location],
                    language=Language.JAVASCRIPT,
                    licenses=[],
                    type=PackageType.NpmPkg,
                    p_url=package_url(name, version),
                    metadata=YarnLockEntry(
                        resolved=item.get("resolved"),
                        integrity=item.get("integrity"),
                    ),
                ),
            )
        except ValidationError as ex:
            LOGGER.warning(
                "Malformed package. Required fields are missing or data types are incorrect.",
                extra={
                    "extra": {
                        "exception": ex.errors(include_url=False),
                        "location": current_location.path(),
                    },
                },
            )
            continue

    return packages


def _extract_relationships(parsed_yarn_lock: dict, packages: list[Package]) -> list[Relationship]:
    relationships = []
    for pkg_name, item in parsed_yarn_lock.items():
        current_pkg = next(
            (package for package in packages if package.name == _get_name(pkg_name, item)),
            None,
        )

        if current_pkg is None:
            continue

        if "dependencies" in item:
            for dep_name, _ in item["dependencies"]:
                dep_name = dep_name.strip('"')
                # TO-DO: check if the version matches
                if dep := next(
                    (package for package in packages if package.name == dep_name),
                    None,
                ):
                    relationships.append(
                        Relationship(
                            from_=dep,
                            to_=current_pkg,
                            type=RelationshipType.DEPENDENCY_OF_RELATIONSHIP,
                            data=None,
                        ),
                    )
    return relationships


def parse_yarn_lock(
    _resolver: Resolver | None,
    _environment: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    parsed_yarn_lock = _parse_yarn_file(reader.read_closer.read())
    packages = _extract_packages(parsed_yarn_lock, reader)
    relationships = _extract_relationships(parsed_yarn_lock, packages)
    return packages, relationships
