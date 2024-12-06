import logging
import os
import stat
import tempfile
import zipfile
from pathlib import (
    Path,
)

from pydantic import (
    ValidationError,
)

from fluid_sbom.artifact.relationship import (
    Relationship,
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
    JavaPomProperties,
)

LOGGER = logging.getLogger(__name__)


def is_safe_path(base_path: str, target_path: str) -> bool:
    base_path = os.path.normpath(base_path)
    target_path = os.path.normpath(target_path)
    return os.path.commonpath([base_path]) == os.path.commonpath([base_path, target_path])


def safe_extract(apk_file: zipfile.ZipFile, destination: str) -> None:
    for file_info in apk_file.infolist():
        file_name = file_info.filename
        if os.path.isabs(file_name) or file_name.startswith(("..", "./")):
            continue

        target_path = os.path.join(destination, file_name)

        if not is_safe_path(destination, target_path):
            continue

        if (file_info.external_attr >> 16) & stat.S_IFLNK:
            continue

        try:
            apk_file.extract(file_name, destination)
        except Exception as ex:
            LOGGER.exception("Error extracting %s: %s", file_name, ex)


def parse_apk(
    _resolver: Resolver | None,
    _env: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    packages: list[Package] = []
    with tempfile.TemporaryDirectory() as output_folder:
        with zipfile.ZipFile(reader.read_closer.name, "r") as apk_file:
            safe_extract(apk_file, output_folder)
        files: list[str] = []
        meta_dir = os.path.join(output_folder, "META-INF")
        if os.path.exists(meta_dir):
            files = [
                os.path.join(meta_dir, file)
                for file in os.listdir(meta_dir)
                if file.endswith(".version")
            ]
        for file in files:
            with open(file, encoding="utf-8") as version_reader:
                version = version_reader.read().strip()
            parts = Path(file).name.replace(".version", "").split("_", 1)
            group_id = parts[0]
            artifact_id = parts[1]

            if any(not value for value in (artifact_id, version, group_id)):
                continue

            java_archive = JavaArchive(
                pom_properties=JavaPomProperties(
                    group_id=group_id,
                    artifact_id=artifact_id,
                    version=version,
                ),
            )

            try:
                packages.append(
                    Package(
                        name=artifact_id,
                        version=version,
                        licenses=[],
                        locations=[reader.location],
                        language=Language.JAVA,
                        type=PackageType.JavaPkg,
                        metadata=java_archive,
                        p_url=package_url(artifact_id, version, java_archive),
                    ),
                )
            except ValidationError as ex:
                LOGGER.warning(
                    "Malformed package. Required fields are missing or data "
                    "types are incorrect.",
                    extra={
                        "extra": {
                            "exception": ex.errors(include_url=False),
                            "location": reader.location.path(),
                        },
                    },
                )
                continue

    return packages, []
