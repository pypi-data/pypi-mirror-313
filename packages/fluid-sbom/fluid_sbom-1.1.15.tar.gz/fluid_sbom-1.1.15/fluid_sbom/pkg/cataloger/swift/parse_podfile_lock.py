import logging
from copy import (
    deepcopy,
)
from typing import (
    cast,
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
from fluid_sbom.internal.collection.types import (
    IndexedDict,
)
from fluid_sbom.internal.collection.yaml import (
    parse_yaml_with_tree_sitter,
)
from fluid_sbom.model.core import (
    Package,
)
from fluid_sbom.pkg.cataloger.generic.parser import (
    Environment,
)
from fluid_sbom.pkg.cataloger.swift.package import (
    new_cocoa_pods_package,
)

LOGGER = logging.getLogger(__name__)


def parse_podfile_lock(
    _: Resolver | None,
    __: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    try:
        podfile: IndexedDict = cast(
            IndexedDict,
            parse_yaml_with_tree_sitter(reader.read_closer.read()),
        )
    except ValueError:
        return [], []

    if not podfile or "PODS" not in podfile:
        return [], []

    packages, dependencies_index = process_pods(podfile, reader)
    if not packages:
        return [], []

    relationships = generate_relations(dependencies_index, packages)

    return packages, relationships


def process_pods(
    podfile: IndexedDict,
    reader: LocationReadCloser,
) -> tuple[list[Package], dict[str, list[str]]]:
    packages: list[Package] = []
    dependencies_index: dict[str, list[str]] = {}

    for index, pod in enumerate(podfile["PODS"]):
        pod_name, pod_version = extract_pod_info(pod)
        if not pod_name or not pod_version:
            return [], {}

        pod_root_package = pod_name.split("/")[0]
        if pod_root_package not in podfile["SPEC CHECKSUMS"]:
            LOGGER.error("Malformed podfile.lock. Incomplete checksums")
            return [], {}

        new_location = deepcopy(reader.location)
        if new_location.coordinates:
            new_location.coordinates.line = podfile["PODS"].get_position(index).start.line

        if pkg := new_cocoa_pods_package(
            pod_name,
            pod_version,
            podfile["SPEC CHECKSUMS"][pod_root_package],
            new_location,
        ):
            packages.append(pkg)
            dependencies_index[pod_name] = dependencies_index.get(pod_name, [])

    return packages, dependencies_index


def extract_pod_info(pod: str | IndexedDict) -> tuple[str, str]:
    if isinstance(pod, str):
        pod_blob = pod
    else:
        pod_blob = list(pod.keys())[0]
    pod_name = pod_blob.split(" ")[0]
    pod_version = pod_blob.split(" ")[1].strip("()")
    return pod_name, pod_version


def generate_relations(
    dependencies_index: dict[str, list[str]],
    packages: list[Package],
) -> list[Relationship]:
    relationships: list[Relationship] = []
    for package_name, dependencies in dependencies_index.items():
        package = next(x for x in packages if x.name == package_name)
        for dependency in dependencies:
            if package_dep := next(
                (x for x in packages if x.name == dependency.split(" ")[0]),
                None,
            ):
                relationships.append(
                    Relationship(
                        from_=package_dep,
                        to_=package,
                        type=RelationshipType.DEPENDENCY_OF_RELATIONSHIP,
                        data=None,
                    ),
                )

    return relationships
