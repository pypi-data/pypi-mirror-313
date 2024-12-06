import logging
from collections import (
    defaultdict,
)
from typing import (
    cast,
)

from cyclonedx.factory.license import (
    LicenseFactory,
)
from cyclonedx.model.bom import (
    Bom,
)
from cyclonedx.model.component import (
    Component,
    ComponentType,
)
from cyclonedx.model.license import (
    LicenseExpression,
)
from cyclonedx.model.tool import (
    Tool,
)
from packageurl import (
    PackageURL,
)

from fluid_sbom.artifact.relationship import (
    Relationship,
)
from fluid_sbom.config.config import (
    SbomConfig,
)
from fluid_sbom.format.common import (
    set_namespace_version,
)
from fluid_sbom.format.cyclone_dx.complete_file import (
    add_authors,
    add_component_properties,
    add_integrity,
    add_vulnerabilities,
)
from fluid_sbom.format.cyclone_dx.output_handler import (
    format_cyclone_json,
    format_cyclone_xml,
)
from fluid_sbom.model.core import (
    Package,
)

LOGGER = logging.getLogger(__name__)


def pkg_to_component(package: Package) -> Component:
    lc_factory = LicenseFactory()
    licenses = [
        lc_factory.make_from_string(lic)
        for lic in package.licenses
        if not isinstance(lc_factory.make_from_string(lic), LicenseExpression)
    ]
    health_metadata = package.health_metadata
    return Component(
        type=ComponentType.LIBRARY,
        name=package.name,
        version=package.version,
        licenses=licenses,
        authors=add_authors(health_metadata) if health_metadata else [],
        bom_ref=f"{package.name}@{package.version}",
        purl=PackageURL.from_string(package.p_url),
        properties=add_component_properties(package),
        hashes=add_integrity(health_metadata) if health_metadata else [],
    )


def format_cyclonedx_sbom(  # pylint:disable=too-many-locals
    packages: list[Package],
    relationships: list[Relationship],
    file_format: str,
    output: str,
    config: SbomConfig,
) -> None:
    namespace, version = set_namespace_version(config=config)
    bom = Bom()
    bom.metadata.component = root_component = Component(
        name=namespace,
        type=ComponentType.APPLICATION,
        licenses=[],
        bom_ref="",
        version=version,
    )
    bom.metadata.tools.tools.add(Tool(vendor="Fluid Attacks", name="Fluid-Sbom"))

    component_cache = {pkg: pkg_to_component(pkg) for pkg in packages}
    for component in component_cache.values():
        bom.components.add(component)
        bom.register_dependency(root_component, [component])

        package = next(
            pkg
            for pkg in packages
            if pkg.name == component.name and pkg.version == component.version
        )
        if package.advisories:
            vulnerabilities = add_vulnerabilities(package)
            for vulnerability in vulnerabilities:
                bom.vulnerabilities.add(vulnerability)

    dependency_map: dict[Component, list[Component]] = defaultdict(list)
    for relationship in relationships:
        to_pkg = component_cache.get(
            cast(Package, relationship.to_),
            pkg_to_component(cast(Package, relationship.to_)),
        )
        from_pkg = component_cache.get(
            cast(Package, relationship.from_),
            pkg_to_component(cast(Package, relationship.from_)),
        )
        dependency_map[to_pkg].append(from_pkg)

    for ref, depends_on_list in dependency_map.items():
        bom.register_dependency(ref, depends_on_list)

    match file_format:
        case "cyclonedx-json":
            format_cyclone_json(bom, output)
        case "cyclonedx-xml":
            format_cyclone_xml(bom, output)
