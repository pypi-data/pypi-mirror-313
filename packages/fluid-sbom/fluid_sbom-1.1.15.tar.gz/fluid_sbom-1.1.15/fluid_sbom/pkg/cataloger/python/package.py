import logging
from typing import (
    Any,
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
from fluid_sbom.file.location import (
    Location,
)
from fluid_sbom.file.resolver import (
    Resolver,
)
from fluid_sbom.internal.package_information.python import (
    get_pypi_package,
)
from fluid_sbom.model.core import (
    Artifact,
    HealthMetadata,
    Language,
    Package,
    PackageType,
)
from fluid_sbom.pkg.cataloger.python.parse_wheel_egg_metadata import (
    ParsedData,
)
from fluid_sbom.pkg.common import (
    infer_algorithm,
)
from fluid_sbom.pkg.python import (
    PythonPackage,
)
from fluid_sbom.utils.file import (
    Digest,
)
from fluid_sbom.utils.licenses.validation import (
    validate_licenses,
)

LOGGER = logging.getLogger(__name__)


def new_package_for_package(
    _resolver: Resolver,
    data: ParsedData,
    sources: Location,
) -> Package | None:
    name = data.python_package.name
    version = data.python_package.version

    if not name or not version:
        return None

    try:
        return Package(
            name=name,
            version=version,
            p_url=package_url(
                name,
                version,
                data.python_package,
            ),
            locations=[sources],
            language=Language.PYTHON,
            type=PackageType.PythonPkg,
            metadata=data.python_package,
            licenses=[],
        )
    except ValidationError as ex:
        LOGGER.warning(
            "Malformed package. Required fields are missing or data types are incorrect.",
            extra={
                "extra": {
                    "exception": ex.errors(include_url=False),
                    "location": sources.path(),
                },
            },
        )
        return None


def package_url(name: str, version: str, package: PythonPackage | None) -> str:
    return PackageURL(
        type="pypi",
        namespace="",
        name=name,
        version=version,
        qualifiers=_purl_qualifiers_for_package(package),
        subpath="",
    ).to_string()


def _purl_qualifiers_for_package(
    package: PythonPackage | None,
) -> dict[str, str]:
    if not package:
        return {}
    if (
        hasattr(package, "direct_url_origin")
        and package.direct_url_origin
        and package.direct_url_origin.vcs
    ):
        url = package.direct_url_origin
        return {"vcs_url": f"{url.vcs}+{url.url}@{url.commit_id}"}
    return {}


def _set_health_metadata(
    package: Package,
    pypi_package: dict[str, Any],
    current_package: dict[str, Any] | None,
) -> None:
    pypi_package_version = pypi_package.get("info", {}).get("version")
    upload_time = pypi_package.get("releases", {}).get(pypi_package_version, [])
    latest_version_created_at = upload_time[0].get("upload_time_iso_8601") if upload_time else None
    package.health_metadata = HealthMetadata(
        latest_version=pypi_package_version,
        latest_version_created_at=latest_version_created_at,
        authors=_get_authors(pypi_package),
        artifact=_get_artifact(package, current_package) if current_package else None,
    )


def _get_artifact(package: Package, current_package: dict[str, Any]) -> Artifact | None:
    url = next(
        (x for x in current_package["urls"] if x["url"].endswith(".tar.gz")),
        None,
    )

    digest_value: str | None = url.get("digests", {}).get("sha256") or None if url else None

    return Artifact(
        url=url["url"] if url else f"https://pypi.org/pypi/{package.name}",
        integrity=Digest(
            algorithm=infer_algorithm(digest_value),
            value=digest_value,
        ),
    )


def _get_authors(pypi_package: dict[str, Any]) -> str | None:
    package_info = pypi_package["info"]
    if "author" in package_info:
        author: str | None = None
        package_author = package_info["author"]
        author_email = package_info.get("author_email")
        if isinstance(package_author, str) and package_author:
            author = package_author
        if not author and author_email:
            author = author_email
        if author and author_email and author_email not in author:
            author = f"{author} <{author_email}>"
        return author
    return None


def complete_package(package: Package) -> Package:
    pkg_advisories = advisories.get_package_advisories(package)
    if pkg_advisories:
        package.advisories = pkg_advisories

    pypi_package = get_pypi_package(package.name)
    if not pypi_package:
        return package

    current_package = get_pypi_package(package.name, package.version)

    _set_health_metadata(package, pypi_package, current_package)

    licenses = pypi_package.get("info", {}).get("license")
    if licenses and isinstance(licenses, str):
        package.licenses = validate_licenses([licenses])

    return package
