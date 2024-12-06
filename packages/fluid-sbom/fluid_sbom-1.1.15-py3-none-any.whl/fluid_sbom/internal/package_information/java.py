import logging
from datetime import (
    datetime,
)
from xml.etree import (  # nosec
    ElementTree,
)

from pydantic import (
    BaseModel,
    ConfigDict,
)

from fluid_sbom.internal.package_information.api_interface import (
    make_get,
)

LOGGER = logging.getLogger(__name__)


class MavenSearchDocResponse(BaseModel):
    id_: str
    group: str
    artifact: str
    version: str
    timestamp: int
    extra_classifiers: list[str]
    packaging: str | None = None
    tags: list[str] | None = None
    model_config = ConfigDict(frozen=True)


class AuthorsLicenses(BaseModel):
    authors: list[str]
    licenses: list[str]
    model_config = ConfigDict(frozen=True)


class MavenPackageInfo(BaseModel):
    group_id: str
    artifact_id: str
    latest_version: str | None = None
    release_date: int | None = None
    authors: list[str] | None = None
    licenses: list[str] | None = None
    version: str | None = None
    jar_url: str | None = None
    hash: str | None = None
    model_config = ConfigDict(frozen=True)


def search_maven_package(artifact_id: str, version: str) -> MavenSearchDocResponse | None:
    base_url = "https://search.maven.org/solrsearch/select"
    if version:
        query = f"a:{artifact_id} AND v:{version}"
    else:
        query = f"a:{artifact_id}"

    params: dict[str, str | int] = {"q": query, "rows": 5, "wt": "json"}

    package_data = make_get(base_url, params=params, timeout=30)
    if package_data:
        docs = package_data["response"].get("docs", [])

        if not docs or len(docs) > 1:
            return None

        try:
            result = MavenSearchDocResponse(
                id_=docs[0]["id"],
                group=docs[0]["g"],
                artifact=docs[0]["a"],
                version=docs[0]["v"] if "v" in docs[0] else docs[0]["latestVersion"],
                packaging=docs[0].get("p", None),
                timestamp=int(docs[0]["timestamp"] // 1000),
                extra_classifiers=docs[0]["ec"],
                tags=docs[0].get("tags", None),
            )
        except KeyError as exc:
            LOGGER.exception(
                "Error parsing Maven search response",
                extra={
                    "extra": {
                        "artifact_id": artifact_id,
                        "version": version,
                        "doc": docs[0],
                        "key": exc.args[0],
                    },
                },
            )
            return None
        return result

    return None


def _get_latest_version_authors_licenses(
    group_id: str,
    artifact_id: str,
    latest_version: str,
) -> AuthorsLicenses | None:
    group_id_path = group_id.replace(".", "/")
    # Fetch the latest version's POM file
    pom_url = (
        f"https://repo1.maven.org/maven2"
        f"/{group_id_path}/{artifact_id}/{latest_version}"
        f"/{artifact_id}-{latest_version}.pom"
    )
    response = make_get(pom_url, content=True, timeout=30)
    if response:
        pom_xml = ElementTree.fromstring(response)  # nosec
        namespace = {"m": "http://maven.apache.org/POM/4.0.0"}

        # Extract authors and licenses
        authors = [
            author.text
            for author in pom_xml.findall("m:developers/m:developer/m:name", namespace)
            if author.text
        ]
        licenses = [
            getattr(package_license.find("m:name", namespace), "text", "")
            for package_license in pom_xml.findall("m:licenses/m:license", namespace)
        ]
        return AuthorsLicenses(authors=authors, licenses=licenses)
    return None


def _get_all_package(group_id: str, artifact_id: str) -> MavenPackageInfo | None:
    group_id_path = group_id.replace(".", "/")
    # URL for the metadata file
    metadata_url = (
        f"https://repo1.maven.org/maven2/{group_id_path}/{artifact_id}/maven-metadata.xml"
    )
    response = make_get(metadata_url, content=True, timeout=30)
    if response:
        # Parse the metadata XML response
        metadata_xml = ElementTree.fromstring(response)  # nosec
        latest_version = metadata_xml.find("versioning/latest")
        release_date_tag = metadata_xml.find("versioning/lastUpdated")
        release_date: int | None = None
        if release_date_tag is not None and release_date_tag.text:
            release_date = int(datetime.strptime(release_date_tag.text, "%Y%m%d%H%M%S").timestamp())

        authors_licenses = (
            _get_latest_version_authors_licenses(group_id, artifact_id, latest_version.text or "")
            if latest_version is not None
            else None
        )
        return MavenPackageInfo(
            group_id=group_id,
            artifact_id=artifact_id,
            latest_version=latest_version.text if latest_version is not None else None,
            release_date=release_date,
            authors=authors_licenses.authors if authors_licenses else None,
            licenses=authors_licenses.licenses if authors_licenses else None,
        )

    return None


def get_maven_package_info(
    group_id: str,
    artifact_id: str,
    version: str | None = None,
) -> MavenPackageInfo | None:
    group_id_path = group_id.replace(".", "/")

    if version:
        # URL for the specific version's POM file
        pom_url = (
            f"https://repo1.maven.org/maven2/{group_id_path}"
            f"/{artifact_id}/{version}/{artifact_id}-{version}.pom"
        )
        response = make_get(pom_url, timeout=30, content=True)
        if response:
            # Extract the download URL and hash
            jar_url = (
                f"https://repo1.maven.org/maven2/{group_id_path}"
                f"/{artifact_id}/{version}/{artifact_id}-{version}.jar"
            )
            hash_url = (
                f"https://repo1.maven.org/maven2/{group_id_path}"
                f"/{artifact_id}/{version}/{artifact_id}-{version}.jar.sha1"
            )
            hash_response: str | None = make_get(hash_url, content=True, timeout=30)
            if hash_response:
                package_hash = hash_response.strip()
            else:
                package_hash = "Hash not available"

            return MavenPackageInfo(
                group_id=group_id,
                artifact_id=artifact_id,
                version=version,
                jar_url=jar_url,
                hash=package_hash,
            )

        return None

    return _get_all_package(group_id, artifact_id)
