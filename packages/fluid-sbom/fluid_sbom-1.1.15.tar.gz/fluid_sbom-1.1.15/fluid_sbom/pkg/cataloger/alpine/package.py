import logging
from contextlib import (
    suppress,
)
from datetime import (
    datetime,
)

from bs4 import (
    BeautifulSoup,
    Tag,
)
from packageurl import (
    PackageURL,
)
from pydantic import (
    BaseModel,
    ValidationError,
)

from fluid_sbom import (
    advisories,
)
from fluid_sbom.file.location import (
    Location,
)
from fluid_sbom.internal.package_information.alpine import (
    get_package_versions_html,
)
from fluid_sbom.linux.release import (
    Release,
)
from fluid_sbom.model.core import (
    HealthMetadata,
    Language,
    Package,
    PackageType,
)
from fluid_sbom.pkg.apk import (
    ApkDBEntry,
)
from fluid_sbom.utils.licenses.validation import (
    validate_licenses,
)

LOGGER = logging.getLogger(__name__)


class ParsedData(BaseModel):
    apk_db_entry: ApkDBEntry
    license: str | None


def package_url(entry: ApkDBEntry, distro: Release | None) -> str:
    qualifiers = {"arch": entry.architecture or ""} if entry else {}

    if entry and entry.origin_package != entry.package and entry.origin_package:
        qualifiers["upstream"] = entry.origin_package
    distro_qualifiers = []

    if distro and distro.id_:
        qualifiers["distro_id"] = distro.id_
        distro_qualifiers.append(distro.id_)

    if distro and distro.version_id:
        qualifiers["distro_version_id"] = distro.version_id
        distro_qualifiers.append(distro.version_id)
    elif distro and distro.build_id:
        distro_qualifiers.append(distro.build_id)

    if distro_qualifiers:
        qualifiers["distro"] = "-".join(distro_qualifiers)

    return PackageURL(
        type="apk",
        namespace=distro.id_.lower() if distro and distro.id_ else "",
        name=entry.package,
        version=entry.version,
        qualifiers=qualifiers,
        subpath="",
    ).to_string()


def new_package(
    data: ParsedData,
    release: Release | None,
    db_location: Location,
) -> Package | None:
    name = data.apk_db_entry.package
    version = data.apk_db_entry.version

    if not name or not version:
        return None

    try:
        return Package(
            name=name,
            version=version,
            locations=[db_location],
            licenses=validate_licenses(data.license.split(" ")) if data.license else [],
            p_url=package_url(data.apk_db_entry, release),
            type=PackageType.ApkPkg,
            metadata=data.apk_db_entry,
            found_by=None,
            health_metadata=None,
            language=Language.UNKNOWN_LANGUAGE,
        )
    except ValidationError as ex:
        LOGGER.warning(
            "Malformed package. Required fields are missing or data types are incorrect.",
            extra={
                "extra": {
                    "exception": ex.errors(include_url=False),
                    "location": db_location.path(),
                },
            },
        )
        return None


def _get_latest_version_and_latest_version_created_at(
    package: Package,
    distro_version: str | None,
    arch: str | None,
) -> tuple[str, datetime | None] | tuple[None, None]:
    html_content = get_package_versions_html(package.name, distro_version, arch)

    if not html_content:
        return None, None

    parsed_content = BeautifulSoup(html_content, features="html.parser")
    version_items: list[Tag] = list(parsed_content.find_all("td", {"class": "version"}))

    if version_items:
        latest_version = version_items[0].text.strip()
        latest_version_created_at = None
        with suppress(IndexError):
            parent_tr = list(version_items[0].fetchPrevious("tr", limit=1))[0]
            if build_date_tag := parent_tr.find_next("td", {"class": "bdate"}):
                latest_version_created_at = datetime.fromisoformat(build_date_tag.text.strip())
        return latest_version, latest_version_created_at

    return None, None


def _set_health_metadata(package: Package, arch: str | None, distro_version: str | None) -> None:
    authors = (
        package.metadata.maintainer
        if package.metadata and hasattr(package.metadata, "maintainer")
        else None
    )
    (
        latest_version,
        latest_version_created_at,
    ) = _get_latest_version_and_latest_version_created_at(package, distro_version, arch)

    package.health_metadata = HealthMetadata(
        latest_version=latest_version,
        latest_version_created_at=latest_version_created_at,
        authors=authors,
    )


def complete_package(
    package: Package,
    distro_id: str | None = None,
    distro_version: str | None = None,
    arch: str | None = None,
) -> Package:
    pkg_advisories = advisories.get_package_advisories(
        package,
        distro_id=distro_id,
        distro_version=distro_version,
    )

    if pkg_advisories:
        package.advisories = pkg_advisories

    _set_health_metadata(package, arch, distro_version)

    return package
