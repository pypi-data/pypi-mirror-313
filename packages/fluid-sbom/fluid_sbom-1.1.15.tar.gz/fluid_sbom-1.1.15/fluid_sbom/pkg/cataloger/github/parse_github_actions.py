from copy import (
    deepcopy,
)
from typing import (
    TypedDict,
    cast,
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
from fluid_sbom.internal.collection.types import (
    IndexedDict,
    IndexedList,
)
from fluid_sbom.internal.collection.yaml import (
    parse_yaml_with_tree_sitter,
)
from fluid_sbom.model.core import (
    Language,
    Package,
    PackageType,
)
from fluid_sbom.pkg.cataloger.generic.parser import (
    Environment,
)
from fluid_sbom.pkg.cataloger.github.package import (
    package_url,
)


class GitHubActions(TypedDict):
    jobs: IndexedDict[str, IndexedDict[str, IndexedList[IndexedDict[str, str]]]]


def parse_github_actions_deps(
    _: Resolver | None,
    __: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    packages: list[Package] = []
    parsed_content = cast(
        IndexedDict[
            str,
            IndexedDict[str, IndexedDict[str, IndexedDict[str, str]]],
        ]
        | None,
        parse_yaml_with_tree_sitter(reader.read_closer.read()),
    )
    if not parsed_content:
        return packages, []

    if jobs := parsed_content.get("jobs"):
        deps: list[tuple[str, int]] = [
            (
                step.get("uses"),  # type: ignore
                step.get_key_position("uses").start.line,  # type: ignore
            )
            for job in jobs.values()
            if isinstance(job, IndexedDict)
            for step in job.get("steps", [])
            if step.get("uses")  # type: ignore
        ]
        for dep, line_number in deps:
            dep_info = dep.rsplit("@", 1)
            location = deepcopy(reader.location)
            if location.coordinates:
                location.coordinates.line = line_number
            if len(dep_info) == 2:
                packages.append(
                    Package(
                        name=dep_info[0],
                        version=dep_info[1],
                        language=Language.UNKNOWN_LANGUAGE,
                        licenses=[],
                        locations=[location],
                        type=PackageType.GithubActionPkg,
                        metadata=None,
                        p_url=package_url(dep_info[0], dep_info[1]),
                    ),
                )
    return packages, []
