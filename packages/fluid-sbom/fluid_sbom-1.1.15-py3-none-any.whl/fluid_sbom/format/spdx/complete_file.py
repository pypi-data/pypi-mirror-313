from license_expression import (
    ExpressionError,
    LicenseExpression,
    get_spdx_licensing,
)
from spdx_tools.spdx.model.actor import (
    Actor,
    ActorType,
)
from spdx_tools.spdx.model.checksum import (
    Checksum,
    ChecksumAlgorithm,
)
from spdx_tools.spdx.model.document import (
    Document,
)
from spdx_tools.spdx.model.package import (
    ExternalPackageRef,
    ExternalPackageRefCategory,
    PackagePurpose,
)
from spdx_tools.spdx.model.package import (
    Package as SPDX_Package,
)
from spdx_tools.spdx.model.spdx_no_assertion import (
    SpdxNoAssertion,
)

from fluid_sbom.file.location import (
    Location,
)
from fluid_sbom.format.common import (
    get_author_info,
    sanitize_name,
)
from fluid_sbom.model.core import (
    HealthMetadata,
    Package,
)

# Constants
NOASSERTION = SpdxNoAssertion()
NAMESPACE = "fluid-attacks"


def add_vulnerabilities_spdx(package: Package) -> list[ExternalPackageRef]:
    vulnerabilities_refs = []
    if package.advisories:
        combined_urls = ", ".join(
            url for advisory in package.advisories for url in advisory.urls if url
        )
        for advisory in package.advisories:
            comment_parts = [
                f"Severity: {advisory.severity}",
                f"EPSs: {advisory.epss}",
                f"Score: {advisory.percentile}",
                f"Affected Version: {package.version}",
                f"Affected Version Range: {advisory.version_constraint}"
                if advisory.version_constraint
                else None,
                f"Description: {advisory.description}" if advisory.description else None,
            ]
            comment_text = "; ".join(filter(None, comment_parts))

            vulnerabilities_refs.append(
                ExternalPackageRef(
                    category=ExternalPackageRefCategory.SECURITY,
                    reference_type="advisory",
                    locator=combined_urls,
                    comment=comment_text,
                ),
            )

    return vulnerabilities_refs


def add_authors(
    health_metadata: HealthMetadata | None,
) -> Actor | SpdxNoAssertion:
    if health_metadata is None:
        return NOASSERTION

    authors_info = get_author_info(health_metadata)

    names = []
    emails = []

    for name, email in authors_info:
        if name:
            names.append(name)
        if email:
            emails.append(email)

    concatenated_names = ", ".join(names)
    concatenated_emails = ", ".join(emails) or None

    return Actor(
        actor_type=ActorType.PERSON,
        name=concatenated_names,
        email=concatenated_emails,
    )


def add_locations_external_refs(
    locations: list[Location],
) -> list[ExternalPackageRef]:
    locations_external_refs = []
    for idx, location in enumerate(locations):
        path = location.path()
        coordinates = location.coordinates
        line = coordinates.line if coordinates else None
        layer = coordinates.file_system_id if coordinates else None

        if path:
            locations_external_refs.append(
                ExternalPackageRef(
                    category=ExternalPackageRefCategory.OTHER,
                    reference_type=f"{NAMESPACE}:locations:{idx}:path",
                    locator=path,
                ),
            )

        if line:
            locations_external_refs.append(
                ExternalPackageRef(
                    category=ExternalPackageRefCategory.OTHER,
                    reference_type=f"{NAMESPACE}:locations:{idx}:line",
                    locator=str(line),
                ),
            )

        if layer:
            locations_external_refs.append(
                ExternalPackageRef(
                    category=ExternalPackageRefCategory.OTHER,
                    reference_type=f"{NAMESPACE}:locations:{idx}:layer",
                    locator=layer,
                ),
            )

    return locations_external_refs


def add_external_refs(package: Package) -> list[ExternalPackageRef]:
    external_refs = []
    health_metadata = package.health_metadata

    external_refs.append(
        ExternalPackageRef(
            category=ExternalPackageRefCategory.OTHER,
            reference_type=f"{NAMESPACE}:language",
            locator=package.language,
        ),
    )

    if health_metadata:
        if health_metadata.latest_version:
            external_refs.append(
                ExternalPackageRef(
                    category=ExternalPackageRefCategory.OTHER,
                    reference_type=(f"{NAMESPACE}:health_metadata:latest_version"),
                    locator=health_metadata.latest_version,
                ),
            )
        if health_metadata.latest_version_created_at:
            external_refs.append(
                ExternalPackageRef(
                    category=ExternalPackageRefCategory.OTHER,
                    reference_type=(f"{NAMESPACE}:health_metadata:latest_version_created_at"),
                    locator=str(health_metadata.latest_version_created_at).replace(" ", ""),
                ),
            )

    if package.p_url:
        external_refs.append(
            ExternalPackageRef(
                category=ExternalPackageRefCategory.PACKAGE_MANAGER,
                reference_type="purl",
                locator=package.p_url,
            ),
        )

    external_refs.extend(add_locations_external_refs(package.locations))
    external_refs.extend(add_vulnerabilities_spdx(package))

    return external_refs


def add_integrity(health_metadata: HealthMetadata | None) -> list[Checksum]:
    if health_metadata:
        integrity = health_metadata.artifact.integrity if health_metadata.artifact else None
        if integrity and integrity.algorithm and integrity.value:
            return [
                Checksum(
                    algorithm=ChecksumAlgorithm[integrity.algorithm.upper()],
                    value=integrity.value,
                ),
            ]
    return []


def add_empty_package(document: Document) -> None:
    document.creation_info.document_comment = "No packages or relationships were found in the root."

    empty_package = SPDX_Package(
        name="NONE",
        spdx_id="SPDXRef-Package-NONE",
        download_location=NOASSERTION,
        license_concluded=NOASSERTION,
        primary_package_purpose=PackagePurpose.LIBRARY,
    )

    document.packages = [empty_package]
    document.relationships = []


def get_spdx_id(package: Package) -> str:
    name = sanitize_name(package.name)
    pkg_platform = sanitize_name(package.type.value.lower())
    pkg_id = package.id_
    return f"SPDXRef-Package-{pkg_platform}-{name}-{pkg_id}"


def add_license(licenses: list[str]) -> LicenseExpression | SpdxNoAssertion:
    licensing = get_spdx_licensing()
    parsed = NOASSERTION
    try:
        parsed = licensing.parse(" AND ".join(licenses))
    except ExpressionError:
        return NOASSERTION

    return parsed
