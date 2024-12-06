import logging
import re
from contextlib import (
    suppress,
)
from copy import (
    deepcopy,
)

from bs4 import (
    BeautifulSoup,
    NavigableString,
    Tag,
)
from pydantic import (
    BaseModel,
    ValidationError,
)

from fluid_sbom.artifact.relationship import (
    Relationship,
)
from fluid_sbom.file.location import (
    Location,
)
from fluid_sbom.file.location_read_closer import (
    LocationReadCloser,
)
from fluid_sbom.file.resolver import (
    Resolver,
)
from fluid_sbom.model.core import (
    Language,
    Package,
    PackageType,
)
from fluid_sbom.pkg.cataloger.generic.parser import (
    Environment,
)
from fluid_sbom.pkg.cataloger.java.maven_repo_utils import (
    recursively_find_versions_from_parent_pom,
)
from fluid_sbom.pkg.cataloger.java.package import (
    package_url,
)
from fluid_sbom.pkg.java import (
    JavaArchive,
    JavaPomParent,
    JavaPomProject,
    JavaPomProperties,
)

LOGGER = logging.getLogger(__name__)


class ParsedPomProject(BaseModel):
    java_pom_project: JavaPomProject
    licenses: list[str]


def extract_bracketed_text(item: str) -> str:
    match = re.search(r"\$\{([^}]+)\}", item)
    if match:
        return match.group(1)
    return ""


def _get_text(parent: Tag | NavigableString, name: str) -> str | None:
    element = parent.find_next(name)
    if element:
        return element.get_text()
    return None


def new_package_from_pom_xml(project: Tag, dependency: Tag, location: Location) -> Package | None:
    java_archive = JavaArchive(
        pom_properties=JavaPomProperties(
            group_id=_get_text(dependency, "groupid"),
            artifact_id=_get_text(dependency, "artifactid"),
            version=_get_text(dependency, "version") if dependency.version else None,
        ),
    )
    name = _get_text(dependency, "artifactid")
    version = dependency.version.get_text() if dependency.version else None
    if (
        version
        and version.startswith("${")
        and (parent_version_node := project.find_next(extract_bracketed_text(version)))
    ):
        version_text = parent_version_node.get_text()
        if version_text and not version_text.startswith("${"):
            version = version_text
    if (
        not version  # pylint:disable=too-many-boolean-expressions
        and java_archive.pom_properties
        and java_archive.pom_properties.group_id
        and java_archive.pom_properties.artifact_id
        and (parent := project.find_next("parent"))
        and (parent_groupid_node := parent.find_next("groupid"))
        and (parent_artifactid_node := parent.find_next("artifactid"))
        and (parent_version_node := parent.find_next("version"))
    ):
        version = recursively_find_versions_from_parent_pom(
            group_id=java_archive.pom_properties.group_id,
            artifact_id=java_archive.pom_properties.artifact_id,
            parent_group_id=parent_groupid_node.get_text(),
            parent_artifact_id=parent_artifactid_node.get_text(),
            parent_version=parent_version_node.get_text(),
        )

    if location.coordinates:
        location.coordinates.line = dependency.sourceline

    if not name or not version:
        return None

    try:
        return Package(
            name=name,
            version=version,
            licenses=[],
            locations=[location],
            language=Language.JAVA,
            type=PackageType.JavaPkg,
            metadata=java_archive,
            p_url=package_url(name, version, java_archive),
        )
    except ValidationError as ex:
        LOGGER.warning(
            "Malformed package. Required fields are missing or data types are incorrect.",
            extra={
                "extra": {
                    "exception": ex.errors(include_url=False),
                    "location": location.path(),
                },
            },
        )
        return None


def parse_pom_xml(
    _resolver: Resolver | None,
    _env: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    root = None
    with suppress(UnicodeError):
        try:
            root = BeautifulSoup(reader.read_closer, features="html.parser")
        except AssertionError:
            return [], []

    if not root:
        return [], []

    pkgs = []
    if (
        (project := root.project)
        and str(project.get("xmlns")) == "http://maven.apache.org/POM/4.0.0"
        and (dependencies := project.find("dependencies", recursive=False))
        and isinstance(dependencies, Tag)
    ):
        for dependency in dependencies.find_all("dependency"):
            pkg = new_package_from_pom_xml(project, dependency, deepcopy(reader.location))
            if pkg:
                pkgs.append(pkg)
    return pkgs, []


def decode_pom_xml(content: str) -> Tag:
    return BeautifulSoup(content, features="html.parser")


def pom_parent(parent: Tag | None) -> JavaPomParent | None:
    if not parent:
        return None

    group_id = _get_text(parent, "groupId")
    artifact_id = _get_text(parent, "artifactId")
    version = _get_text(parent, "version")
    if not group_id or not artifact_id or not version:
        return None

    result = JavaPomParent(
        group_id=group_id,
        artifact_id=artifact_id,
        version=version,
    )

    if not result.group_id and not result.artifact_id and not result.version:
        return None

    return result


def parse_pom_xml_project(path: str, reader: str, _location: Location) -> ParsedPomProject | None:
    project = BeautifulSoup(reader, features="xml").project
    if not project:
        return None
    return new_pom_project(path, project, _location)


def _find_direct_child(parent: Tag, tag: str) -> Tag | None:
    return next(
        (child for child in parent.find_all(tag, recursive=False) if child.parent == parent),
        None,
    )


def new_pom_project(path: str, project: Tag, _location: Location) -> ParsedPomProject:
    artifact_id = _safe_string(_find_direct_child(project, "artifactId"))
    name = _safe_string(_find_direct_child(project, "name"))
    project_url = _safe_string(_find_direct_child(project, "url"))

    licenses: list[str] = []
    if project.licenses:
        for license_ in project.licenses.find_all("license"):
            license_name: str | None = None
            license_url: str | None = None
            if name_node := license_.find_next("name"):
                license_name = name_node.get_text()
            elif url_node := license_.find_next("url"):
                license_url = url_node.get_text()

            if not license_name and not license_url:
                continue
            if license_name:
                licenses.append(license_name)
            elif license_url:
                licenses.append(license_url)

    return ParsedPomProject(
        java_pom_project=JavaPomProject(
            path=path,
            parent=pom_parent(_find_direct_child(project, "parent")),
            group_id=_safe_string(_find_direct_child(project, "groupId")),
            artifact_id=artifact_id,
            version=_safe_string(_find_direct_child(project, "version")),
            name=name,
            description=_safe_string(_find_direct_child(project, "description")),
            url=project_url,
        ),
        licenses=licenses,
    )


def _safe_string(value: Tag | None) -> str:
    if not value:
        return ""
    return value.get_text()
