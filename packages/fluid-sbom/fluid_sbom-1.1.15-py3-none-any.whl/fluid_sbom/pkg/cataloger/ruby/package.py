from typing import (
    Any,
)

from packageurl import (
    PackageURL,
)

from fluid_sbom.internal.package_information.ruby import (
    get_gem_package,
)
from fluid_sbom.model.core import (
    Artifact,
    HealthMetadata,
    Package,
)
from fluid_sbom.pkg.common import (
    infer_algorithm,
)
from fluid_sbom.utils.file import (
    Digest,
)
from fluid_sbom.utils.licenses.validation import (
    validate_licenses,
)


def package_url(name: str, version: str) -> str:
    return PackageURL(
        type="gem",
        namespace="",
        name=name,
        version=version,
        qualifiers=None,
        subpath="",
    ).to_string()


def _get_artifact(current_package: dict[str, Any]) -> Artifact | None:
    digest_value = current_package.get("sha") or None
    return Artifact(
        url=current_package["gem_uri"],
        integrity=Digest(
            algorithm=infer_algorithm(digest_value),
            value=digest_value,
        ),
    )


def _set_health_metadata(
    package: Package,
    gem_package: dict[str, Any],
    current_package: dict[str, Any] | None,
) -> None:
    package.health_metadata = HealthMetadata(
        latest_version=gem_package["version"],
        latest_version_created_at=gem_package["version_created_at"],
        authors=gem_package["authors"],
        artifact=_get_artifact(current_package) if current_package else None,
    )


def complete_package(package: Package) -> Package:
    current_package = get_gem_package(package.name, package.version)
    gem_package = get_gem_package(package.name)
    if not gem_package:
        return package

    _set_health_metadata(package, gem_package, current_package)

    gem_licenses = gem_package["licenses"]
    if gem_licenses:
        package.licenses = validate_licenses(gem_licenses)
    return package
