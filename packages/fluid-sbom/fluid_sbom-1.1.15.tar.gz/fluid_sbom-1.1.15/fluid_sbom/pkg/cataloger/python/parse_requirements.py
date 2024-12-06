import logging
from collections.abc import Generator
from contextlib import (
    suppress,
)
from copy import (
    deepcopy,
)

import requirements
from pydantic import (
    ValidationError,
)
from requirements.requirement import (
    Requirement,
)
from univers.versions import (
    InvalidVersion,
    PypiVersion,
)

from fluid_sbom.artifact.relationship import (
    Relationship,
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
from fluid_sbom.pkg.cataloger.python.package import (
    package_url,
)
from fluid_sbom.pkg.python import (
    PythonRequirementsEntry,
)

LOGGER = logging.getLogger(__name__)


def get_dep_version_range(dep_specs: list[tuple[str, str]]) -> str:
    version_obj = PypiVersion(dep_specs[0][1])
    for _, version in dep_specs[1:]:
        version_obj = max(PypiVersion(version), version_obj)

    return version_obj.string


def get_parsed_dependency(line: str) -> tuple[str, str, Requirement] | None:
    with suppress(Exception):
        parsed_dep = list(requirements.parse(line))[0]

        if not parsed_dep.specs:
            return None
        try:
            version = get_dep_version_range(parsed_dep.specs)
        except InvalidVersion:
            return None
        return str(parsed_dep.name), version, parsed_dep
    return None


def split_lines_requirements(
    content: str,
) -> Generator[tuple[int, str], None, None]:
    last_line = ""
    line_number = 1
    for index, line in enumerate(content.splitlines(), 1):
        if not last_line:
            line_number = index
        line = trim_requirements_txt_line(line)
        if last_line != "":
            line = last_line + line
            last_line = ""
        if line.endswith("\\"):
            last_line += line.rstrip("\\")
            continue
        if not line:
            continue

        if any(
            (
                line.startswith("-e"),
                line.startswith("-r"),
                line.startswith("--requirements"),
            ),
        ):
            continue

        yield line_number, line


def parse_requirements_txt(
    _resolver: Resolver | None,
    _env: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    packages: list[Package] = []

    line_number = 1

    try:
        content = reader.read_closer.read()
    except UnicodeDecodeError:
        return packages, []

    for line_number, line in split_lines_requirements(content):
        parsed_dep = get_parsed_dependency(line)

        # Avoid parsing big txt files that have nothing to do with pip
        if not parsed_dep:
            continue

        product, version, req = parsed_dep

        if not product or not version:
            continue

        p_url = package_url(product, version, None)
        current_location = deepcopy(reader.location)
        if current_location.coordinates:
            current_location.coordinates.line = line_number

        try:
            packages.append(
                Package(
                    name=product,
                    version=version,
                    found_by=None,
                    locations=[current_location],
                    language=Language.PYTHON,
                    p_url=p_url,
                    metadata=PythonRequirementsEntry(
                        name=str(req.name),
                        extras=req.extras,
                        version_constraint=",".join(f"{s[0]} {s[1]}" for s in req.specs)
                        if req.specs
                        else "",
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
                        "location": current_location.path(),
                    },
                },
            )
            continue

    return packages, []


def remove_trailing_comment(line: str) -> str:
    parts = line.split("#", 1)
    if len(parts) < 2:
        # there aren't any comments
        return line
    return parts[0]


def parse_url(line: str) -> str:
    parts = line.split("@")

    if len(parts) > 1:
        desired_index = -1

        for index, part in enumerate(parts):
            part = "".join([char for char in part if char.isalnum()])

            if part.startswith("git"):
                desired_index = index
                break

        if desired_index != -1:
            return "@".join(parts[desired_index:]).strip()

    return ""


def trim_requirements_txt_line(line: str) -> str:
    line = line.strip()

    return remove_trailing_comment(line)
