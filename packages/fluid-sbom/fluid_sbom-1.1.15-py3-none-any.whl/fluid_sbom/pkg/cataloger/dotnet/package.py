import base64
from typing import (
    Any,
)

from fluid_sbom import (
    advisories,
)
from fluid_sbom.internal.package_information.dotnet import (
    get_nuget_package,
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


def _update_advisories(package: Package) -> None:
    pkg_advisories = advisories.get_package_advisories(package)
    if pkg_advisories:
        package.advisories = pkg_advisories


def _get_artifact(current_package: dict[str, Any] | None) -> Artifact | None:
    if current_package:
        # {LOWER_ID}/{LOWER_VERSION}/{LOWER_ID}.{LOWER_VERSION}.nupkg
        lower_id: str | None = current_package["id"].lower()
        lower_version: str | None = current_package["version"].lower()

        digest_value: str | None = current_package.get("packageHash") or None
        algorithm: str | None = current_package.get("packageHashAlgorithm") or None

        if algorithm:
            algorithm = algorithm.lower()
            if algorithm == "sha512" and digest_value:
                digest_value = base64.b64decode(digest_value).hex()

        return Artifact(
            url=(
                f"https://api.nuget.org/v3-flatcontainer/{lower_id}"
                f"/{lower_version}/{lower_id}.{lower_version}.nupkg"
            ),
            integrity=Digest(
                algorithm=infer_algorithm(digest_value),
                value=digest_value,
            ),
        )
    return None


def _set_health_metadata(
    package: Package,
    nuget_package: dict[str, Any],
    current_package: dict[str, Any] | None,
) -> None:
    package.health_metadata = HealthMetadata(
        latest_version=nuget_package.get("version"),
        latest_version_created_at=nuget_package.get("published"),
        authors=nuget_package.get("authors"),
        artifact=_get_artifact(current_package) if current_package else None,
    )


def complete_package(package: Package) -> Package:
    _update_advisories(package)
    current_package = get_nuget_package(package.name, package.version)
    nuget_package = get_nuget_package(package.name)

    if not nuget_package:
        return package

    _set_health_metadata(package, nuget_package, current_package)

    nuget_licenses = nuget_package["licenseExpression"]
    package.licenses = validate_licenses([nuget_licenses]) if nuget_licenses else []

    return package
