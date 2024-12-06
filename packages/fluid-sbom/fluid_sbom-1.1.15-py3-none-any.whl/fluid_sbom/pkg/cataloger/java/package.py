from datetime import (
    datetime,
)
from typing import (
    Any,
)

from packageurl import (
    PackageURL,
)

from fluid_sbom import (
    advisories,
)
from fluid_sbom.internal.package_information.java import (
    MavenPackageInfo,
    get_maven_package_info,
    search_maven_package,
)
from fluid_sbom.model.core import (
    Artifact,
    HealthMetadata,
    Package,
)
from fluid_sbom.pkg.common import (
    infer_algorithm,
)
from fluid_sbom.pkg.java import (
    JavaArchive,
    JavaPomProject,
    JavaPomProperties,
)
from fluid_sbom.utils.file import (
    Digest,
)
from fluid_sbom.utils.licenses.validation import (
    validate_licenses,
)


def _update_advisories(package: Package) -> None:
    pkg_advisories = advisories.get_package_advisories(package)
    if pkg_advisories:
        package.advisories = pkg_advisories


def looks_like_group_id(group_id: str) -> bool:
    return "." in group_id


def remove_osgi_directives(group_id: str) -> str:
    return group_id.split(";")[0]


def clean_group_id(group_id: str) -> str:
    return remove_osgi_directives(group_id).strip()


def group_id_from_pom_properties(properties: JavaPomProperties | None) -> str:
    if not properties:
        return ""
    if properties.group_id:
        return clean_group_id(properties.group_id)
    if properties.artifact_id and looks_like_group_id(properties.artifact_id):
        return clean_group_id(properties.artifact_id)
    return ""


def group_id_pom_project(project: JavaPomProject | None) -> str:
    if not project:
        return ""
    if project.group_id:
        return clean_group_id(project.group_id)
    if project.artifact_id and looks_like_group_id(project.artifact_id):
        return clean_group_id(project.artifact_id)
    if project.parent:
        if project.parent.group_id:
            return clean_group_id(project.parent.group_id)
        if looks_like_group_id(project.parent.artifact_id):
            return clean_group_id(project.parent.artifact_id)
    return ""


def group_id_from_java_metadata(_pkg_name: str, metadata: Any) -> str | None:
    if hasattr(metadata, "pom_properties") and (
        group_id := group_id_from_pom_properties(metadata.pom_properties)
    ):
        return group_id
    if hasattr(metadata, "pom_project") and (
        group_id := group_id_pom_project(metadata.pom_project)
    ):
        return group_id
    return None


def package_url(name: str, version: str, metadata: JavaArchive) -> str:
    group_id = name
    if (g_id := group_id_from_java_metadata(name, metadata)) and g_id:
        group_id = g_id
    return PackageURL(
        type="maven",
        namespace=group_id,
        name=name,
        version=version,
        qualifiers=None,
        subpath="",
    ).to_string()


def _get_health_metadata_artifact(
    current_package: MavenPackageInfo | None,
) -> Artifact | None:
    if current_package and current_package.jar_url:
        digest_value = current_package.hash or None
        return Artifact(
            url=current_package.jar_url,
            integrity=Digest(
                algorithm=infer_algorithm(digest_value),
                value=digest_value,
            ),
        )
    return None


def _get_group_id(package: Package) -> str | None:
    if g_id := group_id_from_java_metadata(package.name, package.metadata):
        return g_id
    if package_candidate := search_maven_package(package.name, package.version):
        return package_candidate.group
    return None


def _set_health_metadata(
    package: Package,
    maven_package: MavenPackageInfo,
    current_package: MavenPackageInfo | None,
) -> None:
    authors = maven_package.authors or []
    package.health_metadata = HealthMetadata(
        latest_version=maven_package.latest_version,
        latest_version_created_at=datetime.fromtimestamp(maven_package.release_date)
        if maven_package.release_date
        else None,
        authors=", ".join(authors) if authors else None,
        artifact=_get_health_metadata_artifact(current_package),
    )


def complete_package(package: Package) -> Package:
    _update_advisories(package)
    group_id = _get_group_id(package)
    if not group_id:
        return package

    maven_package = get_maven_package_info(group_id, package.name)
    if not maven_package:
        if package_candidate := search_maven_package(package.name, package.version):
            maven_package = get_maven_package_info(package_candidate.group, package.name)
        if not maven_package:
            return package

    current_package = get_maven_package_info(group_id, package.name, package.version)

    _set_health_metadata(package, maven_package, current_package)

    maven_package_licenses = maven_package.licenses or []
    if maven_package_licenses:
        package.licenses = validate_licenses(
            [package_license for package_license in maven_package_licenses if package_license],
        )
    return package
