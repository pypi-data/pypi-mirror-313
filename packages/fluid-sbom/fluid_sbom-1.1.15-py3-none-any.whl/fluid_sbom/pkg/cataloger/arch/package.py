import logging

from packageurl import (
    PackageURL,
)
from pydantic import (
    ValidationError,
)

from fluid_sbom.file.location import (
    Location,
)
from fluid_sbom.linux.release import (
    Release,
)
from fluid_sbom.model.core import (
    Language,
    Package,
    PackageType,
)
from fluid_sbom.pkg.alpm import (
    AlpmDBEntry,
)
from fluid_sbom.pkg.url import (
    purl_qualifiers,
)
from fluid_sbom.utils.licenses.validation import (
    validate_licenses,
)

LOGGER = logging.getLogger(__name__)


def package_url(entry: AlpmDBEntry, distro: Release | None = None) -> str:
    qualifiers = {"arch": entry.architecture}
    if entry.base_package:
        qualifiers["upstream"] = entry.base_package
    return PackageURL(
        type="alpm",
        name=entry.package,
        version=entry.version,
        qualifiers=purl_qualifiers(qualifiers, distro),  # type: ignore
        subpath="",
    ).to_string()


def new_package(
    entry: AlpmDBEntry,
    release: Release | None,
    db_location: Location,
) -> Package | None:
    name = entry.package
    version = entry.version

    if not name or not version:
        return None

    licenses_candidates = entry.licenses.split("\n")

    try:
        return Package(
            name=name,
            version=version,
            locations=[db_location],
            licenses=validate_licenses(licenses_candidates),
            type=PackageType.AlpmPkg,
            metadata=entry,
            p_url=package_url(entry, release),
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
