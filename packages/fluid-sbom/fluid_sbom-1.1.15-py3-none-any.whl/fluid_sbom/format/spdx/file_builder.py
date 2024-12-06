import logging
from concurrent.futures import (
    ThreadPoolExecutor,
)
from datetime import (
    UTC,
    datetime,
)
from multiprocessing import (
    cpu_count,
)

from spdx_tools.spdx.model.actor import (
    Actor,
    ActorType,
)
from spdx_tools.spdx.model.document import (
    CreationInfo,
    Document,
)
from spdx_tools.spdx.model.package import (
    Package as SPDX_Package,
)
from spdx_tools.spdx.model.package import (
    PackagePurpose,
)
from spdx_tools.spdx.model.relationship import (
    Relationship as SPDXRelationship,
)
from spdx_tools.spdx.model.relationship import (
    RelationshipType as SPDXRelationshipType,
)
from spdx_tools.spdx.validation.document_validator import (
    validate_full_spdx_document,
)
from spdx_tools.spdx.validation.validation_message import (
    ValidationMessage,
)
from spdx_tools.spdx.writer.write_anything import (
    write_file,
)

from fluid_sbom.artifact.relationship import (
    Relationship,
)
from fluid_sbom.config.config import (
    SbomConfig,
)
from fluid_sbom.format.common import (
    get_document_namespace,
    set_namespace_version,
)
from fluid_sbom.format.spdx.complete_file import (
    NOASSERTION,
    add_authors,
    add_empty_package,
    add_external_refs,
    add_integrity,
    add_license,
    get_spdx_id,
)
from fluid_sbom.model.core import (
    Package,
)
from fluid_sbom.utils.exceptions import (
    SPDXValidationError,
)

LOGGER = logging.getLogger(__name__)


def package_to_spdx_pkg(package: Package) -> SPDX_Package:
    return SPDX_Package(
        spdx_id=get_spdx_id(package),
        name=package.name,
        download_location=NOASSERTION,
        version=package.version,
        license_declared=add_license(package.licenses),
        originator=add_authors(package.health_metadata),
        primary_package_purpose=PackagePurpose.LIBRARY,
        external_references=add_external_refs(package),
        checksums=add_integrity(package.health_metadata),
    )


def create_package_cache(packages: list[Package]) -> dict:
    with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
        return dict(zip(packages, executor.map(package_to_spdx_pkg, packages), strict=False))


def create_document_relationships(
    document: Document,
    spdx_packages: list[SPDX_Package],
) -> list[SPDXRelationship]:
    doc_spdx_id = document.creation_info.spdx_id
    return [
        SPDXRelationship(doc_spdx_id, SPDXRelationshipType.DESCRIBES, pkg.spdx_id)
        for pkg in spdx_packages
    ]


def process_relationships(
    document: Document,
    _relationships: list[Relationship],
    spdx_id_cache: dict,
    document_relationships: list[SPDXRelationship],
) -> None:
    def process_relationship(
        relationship: Relationship,
    ) -> SPDXRelationship | None:
        to_pkg = relationship.to_
        from_pkg = relationship.from_

        if isinstance(to_pkg, Package) and isinstance(from_pkg, Package):
            to_pkg_id = spdx_id_cache.get(to_pkg)
            from_pkg_id = spdx_id_cache.get(from_pkg)

            if to_pkg_id and from_pkg_id:
                return SPDXRelationship(to_pkg_id, SPDXRelationshipType.DEPENDENCY_OF, from_pkg_id)
        return None

    with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
        relationship_results = filter(None, executor.map(process_relationship, _relationships))
        document_relationships.extend(relationship_results)

    document.relationships = document_relationships


def add_packages_and_relationships(
    document: Document,
    packages: list[Package],
    _relationships: list[Relationship],
) -> None:
    package_cache = create_package_cache(packages)

    spdx_id_cache = {pkg: spdx_pkg.spdx_id for pkg, spdx_pkg in package_cache.items()}

    document.packages = list(package_cache.values())

    document_relationships = create_document_relationships(document, document.packages)

    process_relationships(document, _relationships, spdx_id_cache, document_relationships)


def format_spdx_sbom(
    packages: list[Package],
    _relationships: list[Relationship],
    file_format: str,
    output: str,
    config: SbomConfig,
) -> None:
    now_utc = datetime.now(UTC)
    namespace, _ = set_namespace_version(config=config)
    creation_info = CreationInfo(
        spdx_version="SPDX-2.3",
        spdx_id="SPDXRef-DOCUMENT",
        name=namespace,
        data_license="CC0-1.0",
        document_namespace=get_document_namespace(namespace),
        creators=[Actor(ActorType.TOOL, "Fluid-Sbom", None)],
        created=now_utc,
    )

    document = Document(creation_info)

    if not packages and not _relationships:
        add_empty_package(document)
    else:
        add_packages_and_relationships(document, packages, _relationships)

    validation_errors: list[ValidationMessage] = validate_full_spdx_document(document)

    if validation_errors:
        raise SPDXValidationError(validation_errors)

    LOGGER.info(
        "🆗 Valid SPDX %s format, generating output file at %s.%s",
        file_format.upper(),
        output,
        file_format,
    )

    write_file(document, f"{output}.{file_format}")
    LOGGER.info("✅ Output file successfully generated")
