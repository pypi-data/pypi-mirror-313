import logging
import os
from contextlib import (
    suppress,
)
from copy import (
    deepcopy,
)
from pathlib import (
    Path,
)
from typing import (
    TextIO,
    cast,
)

from bs4 import (
    BeautifulSoup,
    Tag,
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
from fluid_sbom.internal.package_information.debian import (
    DebianVersionInfo,
    get_deb_package_version_list,
    get_deb_snapshot,
)
from fluid_sbom.linux.release import (
    Release,
)
from fluid_sbom.model.core import (
    Artifact,
    HealthMetadata,
    Language,
    Package,
    PackageType,
)
from fluid_sbom.pkg.cataloger.debian.parse_copyright import (
    parse_licenses_from_copyright,
)
from fluid_sbom.pkg.cataloger.debian.parse_dpkg_info_files import (
    parse_dpkg_conffile_info,
    parse_dpkg_md5_info,
)
from fluid_sbom.pkg.common import (
    infer_algorithm,
)
from fluid_sbom.pkg.dpkg import (
    DpkgDBEntry,
    DpkgFileRecord,
)
from fluid_sbom.pkg.url import (
    purl_qualifiers,
)
from fluid_sbom.utils.file import (
    Digest,
)
from fluid_sbom.utils.licenses.validation import (
    validate_licenses,
)

LOGGER = logging.getLogger(__name__)


def package_url(pkg: DpkgDBEntry, distro: Release | None = None) -> str:
    qualifiers = {"arch": pkg.architecture}
    if distro and (distro.id_ == "debian" or "debian" in (distro.id_like or [])):
        if distro.version_id:
            qualifiers["distro_version_id"] = distro.version_id
        qualifiers["distro_id"] = distro.id_
    if pkg.source:
        qualifiers["upstream"] = (
            f"{pkg.source}@{pkg.source_version}" if pkg.source_version else pkg.source
        )

    return PackageURL(
        type="deb",
        namespace=distro.id_ if distro and distro.id_ else "",
        name=pkg.package,
        version=pkg.version,
        qualifiers=purl_qualifiers(qualifiers, distro),
        subpath="",
    ).to_string()


def md5_key(metadata: DpkgDBEntry) -> str:
    content_key = metadata.package
    if metadata.architecture not in ("", "all"):
        return f"{content_key}:{metadata.architecture}"
    return content_key


def fetch_md5_content(
    resolver: Resolver,
    db_location: Location,
    entry: DpkgDBEntry,
) -> tuple[TextIO | None, Location | None] | None:
    if not db_location.coordinates:
        return None
    search_path = str(Path(db_location.coordinates.real_path).parent)
    if not search_path.endswith("status.d"):
        search_path = os.path.join(search_path, "info")
    name = md5_key(entry)
    location = resolver.relative_file_path(
        db_location,
        os.path.join(search_path, name + ".md5sums"),
    )
    if not location:
        location = resolver.relative_file_path(
            db_location,
            os.path.join(search_path, entry.package + ".md5sums"),
        )
    if not location:
        return None

    reader = resolver.file_contents_by_location(location)
    if not reader:
        LOGGER.warning(
            "failed to fetch deb md5 contents (package=%s)",
            entry.package,
        )
    return reader, location


def fetch_conffile_contents(
    resolver: Resolver,
    db_location: Location,
    entry: DpkgDBEntry,
) -> tuple[TextIO | None, Location | None] | None:
    if not db_location.coordinates:
        return None
    parent_path = str(Path(db_location.coordinates.real_path).parent)

    name = md5_key(entry)
    location = resolver.relative_file_path(
        db_location,
        os.path.join(parent_path, "info", name + ".conffiles"),
    )
    if not location:
        location = resolver.relative_file_path(
            db_location,
            os.path.join(parent_path, "info", entry.package + ".conffiles"),
        )
    if not location:
        return None, None
    reader = resolver.file_contents_by_location(location)
    if not reader:
        LOGGER.warning(
            "failed to fetch deb conffiles contents (package=%s)",
            entry.package,
        )
    return reader, location


def get_additional_file_listing(
    resolver: Resolver,
    db_location: Location,
    entry: DpkgDBEntry,
) -> tuple[list[DpkgFileRecord], list[Location]]:
    files: list[DpkgFileRecord] = []
    locations: list[Location] = []
    md5_result = fetch_md5_content(resolver, db_location, entry)
    if not md5_result:
        return files, locations
    md5_reader, md5_location = md5_result
    if md5_reader is not None and md5_location is not None:
        files.extend(parse_dpkg_md5_info(md5_reader))
        locations.append(md5_location)
    conffiles = fetch_conffile_contents(resolver, db_location, entry)
    if not conffiles:
        return files, locations
    conffiles_reader, conffiles_location = conffiles

    if conffiles_reader is not None and conffiles_location is not None:
        files.extend(parse_dpkg_conffile_info(conffiles_reader))
        locations.append(conffiles_location)

    return files, locations


def merge_file_listing(resolver: Resolver, db_location: Location, pkg: Package) -> None:
    metadata: DpkgDBEntry = cast(DpkgDBEntry, pkg.metadata)
    files, info_locations = get_additional_file_listing(resolver, db_location, metadata)
    for new_file in files:
        exists = False
        for existing_file in metadata.files or []:
            if existing_file.path == new_file.path:
                exists = True
                break
        if not exists and metadata.files:
            metadata.files.append(new_file)
    sorted_files = sorted(metadata.files or [], key=lambda x: x.path)
    metadata.files = sorted_files
    pkg.metadata = metadata
    pkg.locations.extend(info_locations)


def fetch_copyright_contents(
    resolver: Resolver | None,
    db_location: Location,
    metadata: DpkgDBEntry,
) -> tuple[TextIO | None, Location | None]:
    if not resolver:
        return None, None

    copyright_path = os.path.join("/usr/share/doc", metadata.package, "copyright")
    location = resolver.relative_file_path(db_location, copyright_path)

    if not location:
        return None, None

    reader = resolver.file_contents_by_location(location)
    if not reader:
        LOGGER.warning(
            "failed to fetch deb copyright contents (package=%s)",
            metadata.package,
        )

    return reader, location


def add_licenses(resolver: Resolver, db_location: Location, pkg: Package) -> None:
    metadata: DpkgDBEntry = cast(DpkgDBEntry, pkg.metadata)

    pkg.licenses = []
    copyright_reader, copyright_location = fetch_copyright_contents(resolver, db_location, metadata)

    if copyright_reader is not None and copyright_location is not None:
        licenses_strs = parse_licenses_from_copyright(copyright_reader)
        pkg.licenses = validate_licenses(licenses_strs)


def new_dpkg_package(
    entry: DpkgDBEntry,
    db_location: Location,
    _resolver: Resolver | None,
    release: Release | None = None,
) -> Package | tuple[Package, Package] | None:
    name = entry.package
    version = entry.version

    if not name or not version:
        return None

    try:
        dpkg = Package(
            name=name,
            version=version,
            licenses=[],
            p_url=package_url(entry, release),
            locations=[db_location],
            type=PackageType.DebPkg,
            metadata=entry,
            found_by=None,
            language=Language.UNKNOWN_LANGUAGE,
        )
        if _resolver is not None:
            # side effects
            merge_file_listing(_resolver, db_location, dpkg)
            add_licenses(_resolver, db_location, dpkg)

        source_dpkg: Package | None = None
        if (entry.source and entry.source != dpkg.name) or (
            entry.source and entry.source_version and entry.source_version != dpkg.version
        ):
            new_entry = deepcopy(entry)
            new_entry.package = entry.source
            new_entry.version = entry.source_version or dpkg.version
            new_entry.source = None
            new_entry.source_version = None
            new_entry.dependencies = None
            new_entry.pre_dependencies = None

            source_dpkg = deepcopy(dpkg)
            source_dpkg.name = new_entry.package
            source_dpkg.version = new_entry.version
            source_dpkg.p_url = package_url(new_entry, release)

        if source_dpkg:
            return dpkg, source_dpkg
        return dpkg
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


def _search_download_url(
    package: Package,
    arch: str | None = None,
) -> tuple[str, str | None] | None:
    html_download = get_deb_snapshot(package.name, package.version)
    if not html_download:
        return None
    parsed = BeautifulSoup(html_download, features="html.parser")
    tags: list[Tag] = parsed.find_all("a", href=True)
    tag_href: str | list[str] | None = None
    for tag in tags:
        if (
            tag.text.endswith(".deb")
            and package.name in tag.text
            and package.version in tag.text
            and (arch in tag.text if arch else True)
        ):
            tag_href = tag.get("href")
            break
    else:
        for tag in tags:
            if (
                tag.text.endswith(".deb")
                and package.name in tag.text
                and package.version in tag.text
            ):
                tag_href = tag.get("href")
                break
    if not tag_href:
        return None
    sha1_hash: str | None = None
    with suppress(IndexError):
        sha1_hash = list(tag.fetchPrevious("code", limit=1))[0].text

    return f"https://snapshot.debian.org{tag_href}", sha1_hash


def _get_artifact(package: Package, arch: str | None) -> Artifact | None:
    download_url_item = _search_download_url(package, arch)
    if download_url_item:
        digest_value = download_url_item[1] or None
        return Artifact(
            url=download_url_item[0],
            integrity=Digest(
                algorithm=infer_algorithm(digest_value),
                value=digest_value,
            ),
        )
    return None


def _set_health_metadata(
    package: Package,
    versions_list: list[DebianVersionInfo] | None,
    arch: str | None,
) -> None:
    latest_version = versions_list[0]["version"] if versions_list else None
    authors = package.metadata.maintainer if hasattr(package.metadata, "maintainer") else None

    package.health_metadata = HealthMetadata(
        latest_version=latest_version,
        authors=authors,
        artifact=_get_artifact(package, arch),
    )


def complete_package(
    package: Package,
    release: Release | None = None,
    arch: str | None = None,
) -> Package:
    if release:
        pkg_advisories = advisories.get_package_advisories(
            package,
            distro_id=release.id_,
            distro_version=release.version_id,
        )
    else:
        pkg_advisories = advisories.get_package_advisories(package)

    if pkg_advisories:
        package.advisories = pkg_advisories

    version_code_name: str | None = None
    if release:
        version_code_name = release.version_code_name

    versions_list = get_deb_package_version_list(package.name, version_code_name)

    _set_health_metadata(package, versions_list, arch)

    return package
