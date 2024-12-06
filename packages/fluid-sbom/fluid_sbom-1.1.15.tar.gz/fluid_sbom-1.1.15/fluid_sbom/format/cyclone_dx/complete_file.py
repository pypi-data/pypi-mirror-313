from decimal import (
    Decimal,
)

from cyclonedx.model import (
    HashType,
    Property,
    XsUri,
)
from cyclonedx.model.contact import (
    OrganizationalContact,
)
from cyclonedx.model.vulnerability import (
    BomTarget,
    BomTargetVersionRange,
    Vulnerability,
    VulnerabilityAdvisory,
    VulnerabilityRating,
    VulnerabilitySeverity,
)

from fluid_sbom.file.location import (
    Location,
)
from fluid_sbom.format.common import (
    get_author_info,
)
from fluid_sbom.model.core import (
    HealthMetadata,
    Package,
)

# Constants
NAMESPACE = "fluid-attacks"


def add_vulnerabilities(package: Package) -> list[Vulnerability]:
    vulnerabilities = []
    if package.advisories:
        for advisory in package.advisories:
            rating = VulnerabilityRating(
                severity=VulnerabilitySeverity(advisory.severity.lower()),
                score=Decimal(str(advisory.percentile)),
            )

            advisory_obj = (
                [VulnerabilityAdvisory(url=XsUri(url)) for url in advisory.urls]
                if advisory.urls
                else []
            )

            bom_target = BomTarget(
                ref=f"{package.name}@{package.version}",
                versions=[
                    BomTargetVersionRange(
                        version=package.version if not advisory.version_constraint else None,
                        range=advisory.version_constraint,
                    ),
                ],
            )

            additional_properties = [
                Property(name=f"{NAMESPACE}:advisory:epss", value=str(advisory.epss)),
            ]
            vulnerability = Vulnerability(
                bom_ref=f"{package.name}@{advisory.id}",
                id=advisory.id,
                description=advisory.description,
                advisories=advisory_obj,
                ratings=[rating],
                affects=[bom_target],
                properties=additional_properties,
            )
            vulnerabilities.append(vulnerability)

    return vulnerabilities


def add_health_metadata_properties(
    health_metadata: HealthMetadata,
) -> list[Property]:
    properties = []
    if health_metadata.latest_version:
        properties.append(
            Property(
                name=f"{NAMESPACE}:health_metadata:latest_version",
                value=health_metadata.latest_version,
            ),
        )

    if health_metadata.latest_version_created_at:
        properties.append(
            Property(
                name=f"{NAMESPACE}:health_metadata:latest_version_created_at",
                value=str(health_metadata.latest_version_created_at),
            ),
        )

    return properties


def add_locations_properties(locations: list[Location]) -> list[Property]:
    properties = []
    for idx, location in enumerate(locations):
        path = location.path()
        line = (
            location.coordinates.line
            if location.coordinates and location.coordinates.line
            else None
        )
        layer = (
            location.coordinates.file_system_id
            if location.coordinates and location.coordinates.file_system_id
            else None
        )

        properties.append(Property(name=f"{NAMESPACE}:locations:{idx}:path", value=path))
        if line:
            properties.append(Property(name=f"{NAMESPACE}:locations:{idx}:line", value=str(line)))
        if layer:
            properties.append(Property(name=f"{NAMESPACE}:locations:{idx}:layer", value=layer))

    return properties


def add_component_properties(package: Package) -> list[Property]:
    properties = [Property(name=f"{NAMESPACE}:language", value=package.language)]

    if package.health_metadata:
        properties.extend(add_health_metadata_properties(package.health_metadata))

    if package.locations:
        properties.extend(add_locations_properties(package.locations))

    return properties


def add_integrity(health_metadata: HealthMetadata) -> list[HashType] | None:
    integrity = health_metadata.artifact.integrity if health_metadata.artifact else None
    if integrity and integrity.algorithm and integrity.value:
        return [HashType.from_hashlib_alg(integrity.algorithm, integrity.value)]
    return None


def add_authors(
    health_metadata: HealthMetadata | None,
) -> list[OrganizationalContact]:
    if health_metadata is None:
        return []

    authors_info = get_author_info(health_metadata)
    authors = []

    for name, email in authors_info:
        if name or email:
            authors.append(
                OrganizationalContact(
                    name=name,
                    email=email,
                ),
            )

    return authors
