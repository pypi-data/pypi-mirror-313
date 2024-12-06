import base64
import logging
from contextlib import (
    suppress,
)
from copy import (
    deepcopy,
)

from packageurl import (
    PackageURL,
)
from pydantic import (
    ValidationError,
)

from fluid_sbom import (
    advisories,
)
from fluid_sbom.file.dependency_type import (
    DependencyType,
)
from fluid_sbom.file.location import (
    Location,
)
from fluid_sbom.internal.collection.types import (
    IndexedDict,
)
from fluid_sbom.internal.package_information.javascript import (
    NPMPackage,
    NPMPackageLicense,
    get_npm_package,
)
from fluid_sbom.model.core import (
    Artifact,
    HealthMetadata,
    Language,
    Package,
    PackageType,
)
from fluid_sbom.pkg.common import (
    infer_algorithm,
)
from fluid_sbom.pkg.npm import (
    NpmPackageLockEntry,
)
from fluid_sbom.utils.file import (
    Digest,
)
from fluid_sbom.utils.licenses.validation import (
    validate_licenses,
)

LOGGER = logging.getLogger(__name__)


def handle_licenses(
    licenses: str | list[str | dict[str, str]] | NPMPackageLicense,
) -> list[str]:
    if isinstance(licenses, dict):
        return [licenses["type"]] if "type" in licenses else []
    if isinstance(licenses, list):
        licenses_list = []
        for license_item in licenses:
            if isinstance(license_item, str):
                licenses_list.append(license_item)
            if isinstance(license_item, dict) and license_item["type"]:
                licenses_list.append(license_item["type"])
        return licenses_list
    return [licenses]


def new_package_lock_v1(
    is_transitive: bool,
    location: Location,
    name: str,
    value: IndexedDict,
) -> Package | None:
    version = value.get("version")
    if not name or not version:
        return None

    alias_prefix_package_lock = "npm:"
    if version.startswith(alias_prefix_package_lock):
        name, version = version.removeprefix(alias_prefix_package_lock).split("@")
    current_location = deepcopy(location)
    if current_location.coordinates:
        current_location.coordinates.line = value.position.start.line
        current_location.dependency_type = (
            DependencyType.TRANSITIVE if is_transitive else DependencyType.DIRECT
        )
    try:
        return Package(
            name=name,
            version=version,
            locations=[current_location],
            language=Language.JAVASCRIPT,
            licenses=[],
            type=PackageType.NpmPkg,
            metadata=NpmPackageLockEntry(
                resolved=value["resolved"],
                integrity=value["integrity"],
                is_dev=value.get("dev", False),
            )
            if value.get("resolved") and "integrity" in value
            else None,
            p_url=package_url(name, version),
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
        return None


def new_package_lock_v2(
    is_transitive: bool,
    location: Location,
    name: str,
    value: IndexedDict,
) -> Package | None:
    version: str | None = value.get("version")

    if not name or not version:
        return None

    current_location = location

    if current_location.coordinates:
        current_location.coordinates.line = value.position.start.line
        current_location.dependency_type = (
            DependencyType.TRANSITIVE if is_transitive else DependencyType.DIRECT
        )
    try:
        return Package(
            name=name,
            version=version,
            locations=[current_location],
            language=Language.JAVASCRIPT,
            licenses=[],
            type=PackageType.NpmPkg,
            metadata=NpmPackageLockEntry(
                resolved=value.get("resolved"),
                integrity=value.get("integrity"),
                is_dev=value.get("dev", False),
            ),
            p_url=package_url(name, version),
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
        return None


def package_url(name: str, version: str) -> str:
    namespace = ""
    fields = name.split("/", 2)
    if len(fields) > 1:
        namespace = fields[0]
        name = fields[1]

    if not name:
        return ""

    return PackageURL(
        type="npm",
        namespace=namespace,
        name=name,
        version=version,
        qualifiers={},
        subpath="",
    ).to_string()


def _get_author(npm_package: NPMPackage) -> str | None:
    author: str | None = None
    if "author" in npm_package:
        package_author = npm_package["author"]
        if isinstance(package_author, dict) and "name" in package_author:
            author = package_author["name"]
            if "email" in package_author:
                author = f'{author} <{package_author["email"]}>'
        elif package_author and isinstance(package_author, str):
            author = str(package_author)
        return author
    return None


def _update_advisories(package: Package) -> None:
    pkg_advisories = advisories.get_package_advisories(package)
    if pkg_advisories:
        package.advisories = pkg_advisories


def _get_latest_version_info(npm_package: NPMPackage, current_version: str) -> tuple:
    using_pre_release = "-" in current_version
    latest_version = None
    latest_version_created_at = None

    if using_pre_release:
        latest_version = list(npm_package["versions"].keys())[-1]
        latest_version_created_at = npm_package["time"]["modified"]
    elif npm_package.get("dist-tags"):
        latest_version = npm_package["dist-tags"]["latest"]
        latest_version_created_at = npm_package["time"][latest_version]

    return latest_version, latest_version_created_at


def _get_artifact_info(npm_package: NPMPackage, current_version: str) -> Artifact | None:
    current_package = npm_package["versions"].get(current_version)
    artifact = None

    if current_package:
        with suppress(KeyError):
            digest_value = current_package.get("dist", {}).get("integrity") or None

            if digest_value:
                algorithm, digest_hash = digest_value.split("-", 1)
                if algorithm == "sha512":
                    binary_hash = base64.b64decode(digest_hash)
                    digest_hash = binary_hash.hex()

                artifact = Artifact(
                    url=current_package["dist"]["tarball"],
                    integrity=Digest(
                        algorithm=infer_algorithm(digest_hash),
                        value=digest_hash,
                    ),
                )

    return artifact


def _set_health_metadata(package: Package, npm_package: NPMPackage) -> None:
    latest_version, latest_version_created_at = _get_latest_version_info(
        npm_package,
        package.version,
    )
    package.health_metadata = HealthMetadata(
        latest_version=latest_version,
        latest_version_created_at=latest_version_created_at,
        artifact=_get_artifact_info(npm_package, package.version),
        authors=_get_author(npm_package),
    )


def complete_package(package: Package) -> Package:
    _update_advisories(package)

    npm_package = get_npm_package(package.name)
    if not npm_package:
        return package

    _set_health_metadata(package, npm_package)

    licenses = npm_package.get("license")
    if licenses and isinstance(licenses, (str, list, dict)):
        package.licenses = validate_licenses(handle_licenses(licenses))

    return package
