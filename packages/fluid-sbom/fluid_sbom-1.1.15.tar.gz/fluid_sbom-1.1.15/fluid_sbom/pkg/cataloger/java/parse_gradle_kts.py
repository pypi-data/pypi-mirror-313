import logging
import re
from copy import (
    deepcopy,
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
from fluid_sbom.pkg.cataloger.java.package import (
    package_url,
)
from fluid_sbom.pkg.java import (
    JavaArchive,
    JavaPomProject,
)

LOGGER = logging.getLogger(__name__)
# Constants
QUOTE = r'["\']'
NL = r"(\n?\s*)?"
TEXT = r"[a-zA-Z0-9._-]+"
RE_GRADLE_KTS: re.Pattern[str] = re.compile(
    rf"(runtimeOnly|api|compile|plugin|compileOnly|implementation)\({QUOTE}"
    rf"(?P<group>{TEXT}):(?P<name>{TEXT}):"
    rf"(?P<version>{TEXT})"
    rf"(?::(?P<classifier>{TEXT}))?"
    rf"{QUOTE}\)",
)


def is_comment(line: str) -> bool:
    return (
        line.strip().startswith("//")
        or line.strip().startswith("/*")
        or line.strip().endswith("*/")
    )


class LockFileDependency(BaseModel):
    group: str
    name: str
    version: str
    line: int | None = None


def parse_gradle_lockfile_kts(
    _resolver: Resolver | None,
    __: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    dependencies = parse_dependencies(reader)
    packages = create_packages(dependencies, reader.location)
    return packages, []


def parse_dependencies(reader: LocationReadCloser) -> list[LockFileDependency]:
    dependencies: list[LockFileDependency] = []
    is_block_comment = False

    for line_no, line in enumerate(reader.read_closer.readlines(), start=1):
        line = line.strip()
        is_block_comment = update_block_comment_status(line, is_block_comment)

        if is_block_comment or is_comment(line):
            continue

        dependency = extract_dependency(line, line_no)
        if dependency:
            dependencies.append(dependency)

    return dependencies


def update_block_comment_status(line: str, is_block_comment: bool) -> bool:
    if "/*" in line:
        return True
    if "*/" in line:
        return False
    return is_block_comment


def extract_dependency(line: str, line_no: int) -> LockFileDependency | None:
    if match := RE_GRADLE_KTS.match(line):
        version = match.group("version")
        if version:
            return LockFileDependency(
                group=match.group("group"),
                name=match.group("name"),
                version=version,
                line=line_no,
            )

    return None


def create_packages(
    dependencies: list[LockFileDependency],
    reader_location: Location,
) -> list[Package]:
    packages: list[Package] = []

    for dependency in dependencies:
        name = dependency.name
        version = dependency.version

        if not name or not version:
            continue

        location = deepcopy(reader_location)
        if location.coordinates:
            location.coordinates.line = dependency.line

        archive = create_java_archive(dependency, name, version)

        try:
            package = create_package(name, version, location, archive)
            packages.append(package)
        except ValidationError as ex:
            log_validation_error(ex, location)

    return packages


def create_java_archive(dependency: LockFileDependency, name: str, version: str) -> JavaArchive:
    return JavaArchive(
        pom_project=JavaPomProject(
            group_id=dependency.group,
            name=name,
            artifact_id=name,
            version=version,
        ),
    )


def create_package(name: str, version: str, location: Location, archive: JavaArchive) -> Package:
    return Package(
        name=name,
        version=version,
        locations=[location],
        language=Language.JAVA,
        type=PackageType.JavaPkg,
        metadata=archive,
        p_url=package_url(name, version, archive),
        licenses=[],
    )


def log_validation_error(ex: ValidationError, location: Location) -> None:
    LOGGER.warning(
        "Malformed package. Required fields are missing or data types are incorrect.",
        extra={
            "extra": {
                "exception": ex.errors(include_url=False),
                "location": location.path(),
            },
        },
    )
