import logging
from copy import (
    deepcopy,
)
from typing import (
    Any,
)

from packageurl import (
    PackageURL,
)
from pydantic import (
    ValidationError,
)

from fluid_sbom.file.location import (
    Location,
)
from fluid_sbom.internal.collection.types import (
    IndexedDict,
)
from fluid_sbom.internal.package_information.php import (
    get_composer_package,
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
from fluid_sbom.pkg.php import (
    PhpComposerAuthors,
    PhpComposerExternalReference,
    PhpComposerInstalledEntry,
)
from fluid_sbom.utils.file import (
    Digest,
)
from fluid_sbom.utils.licenses.validation import (
    validate_licenses,
)

LOGGER = logging.getLogger(__name__)


def package_url(name: str, version: str) -> str:
    fields = name.split("/")

    vendor = ""
    if len(fields) == 1:
        name = fields[0]
    elif len(fields) >= 2:
        vendor = fields[0]
        name = "-".join(fields[1:])

    return PackageURL(
        type="composer",
        namespace=vendor,
        name=name,
        version=version,
        qualifiers=None,
        subpath="",
    ).to_string()


def new_package_from_composer(
    package: IndexedDict,
    location: Location,
    is_dev: bool = False,
) -> Package | None:
    new_location = deepcopy(location)
    if new_location.coordinates:
        new_location.coordinates.line = package.position.start.line

    try:
        source = package.get("source")
        dist = package.get("dist")
        name = package.get("name")
        version = package.get("version")

        if not name or not version:
            return None

        return Package(
            name=name,
            version=version,
            locations=[new_location],
            language=Language.PHP,
            licenses=list(package.get("license", [])),
            type=PackageType.PhpComposerPkg,
            p_url=package_url(name, version),
            metadata=PhpComposerInstalledEntry(
                name=name,
                version=version,
                source=PhpComposerExternalReference(
                    type=source.get("type"),
                    url=source.get("url"),
                    reference=source.get("reference"),
                    shasum=source.get("shasum"),
                )
                if source
                else None,
                dist=PhpComposerExternalReference(
                    type=dist.get("type"),
                    url=dist.get("url"),
                    reference=dist.get("reference"),
                    shasum=dist.get("shasum"),
                )
                if dist
                else None,
                require=package.get("require"),
                provide=package.get("provide"),
                require_dev=package.get("require-dev"),
                suggest=package.get("suggest"),
                license=package.get("license", []),
                type=package.get("type"),
                notification_url=package.get("notification-url"),
                bin=package.get("bin", []),
                authors=[
                    PhpComposerAuthors(
                        name=x.get("name"),
                        email=x.get("email"),
                        homepage=x.get("homepage"),
                    )
                    for x in package.get("authors", [])
                ],
                description=package.get("description"),
                homepage=package.get("homepage"),
                keywords=package.get("keywords", []),
                time=package.get("time"),
            ),
            is_dev=is_dev,
        )
    except ValidationError as ex:
        LOGGER.warning(
            "Malformed package. Required fields are missing or data types are incorrect.",
            extra={
                "extra": {
                    "exception": ex.errors(include_url=False),
                    "location": new_location.path(),
                },
            },
        )
        return None


def package_url_from_pecl(pkg_name: str, version: str) -> str:
    purl = PackageURL(
        type="pecl",
        namespace="",
        name=pkg_name,
        version=version,
        qualifiers=None,
        subpath="",
    )
    return purl.to_string()


def _get_author(composer_package: dict[str, Any]) -> str | None:
    if not composer_package.get("authors"):
        return None

    authors = []
    for author_item in composer_package["authors"]:
        author = author_item["name"]
        if "email" in author_item:
            author += f" <{author_item['email']}>"
        authors.append(author)

    return ", ".join(authors)


def _set_health_metadata(
    package: Package,
    composer_package: dict[str, Any],
    current_package: dict[str, Any] | None,
) -> None:
    package.health_metadata = HealthMetadata(
        latest_version=composer_package["version"],
        latest_version_created_at=composer_package["time"],
        artifact=_get_artifact_metadata(current_package) if current_package else None,
        authors=_get_author(composer_package),
    )


def _get_artifact_metadata(current_package: dict[str, Any] | None) -> Artifact | None:
    if current_package:
        dist_info = current_package.get("dist")
        if dist_info and isinstance(dist_info.get("url"), str):
            digest_value = dist_info.get("shasum") or None
            return Artifact(
                url=dist_info["url"],
                integrity=Digest(
                    algorithm=infer_algorithm(digest_value),
                    value=digest_value,
                ),
            )
    return None


def complete_package(package: Package) -> Package:
    current_package = get_composer_package(package.name, package.version)
    composer_package = get_composer_package(package.name)

    if not composer_package:
        return package

    _set_health_metadata(package, composer_package, current_package)

    package.licenses = validate_licenses(composer_package["license"])

    return package
