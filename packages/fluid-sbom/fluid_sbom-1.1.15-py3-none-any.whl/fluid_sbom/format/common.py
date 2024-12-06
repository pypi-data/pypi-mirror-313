import os
import re
import uuid
from urllib.parse import (
    urlunparse,
)

from fluid_sbom.config.config import (
    SbomConfig,
    SourceType,
)
from fluid_sbom.internal.file_resolver.container_image import (
    ContainerImage,
)
from fluid_sbom.model.core import (
    HealthMetadata,
    Package,
)
from fluid_sbom.sources.directory_source import (
    Directory,
)


def is_valid_email(email: str) -> bool:
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_regex, email) is not None


def get_author_info(
    health_metadata: HealthMetadata,
) -> list[tuple[str | None, str | None]]:
    author_info = []

    if health_metadata.authors:
        authors_list = health_metadata.authors.split(", ")
        for author in authors_list:
            name: str | None = None
            email: str | None = None
            email_match = re.search(r"<([^<>]+)>", author)

            if email_match:
                email_candidate: str = email_match.group(1)
                if is_valid_email(email_candidate):
                    email = email_candidate
                else:
                    email = None
                name = author.replace(email_match.group(0), "").strip() or None
            else:
                name = author.strip() or None

            author_info.append((name, email))

    return author_info


def sanitize_name(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9.-]", "-", text)


def get_document_namespace(working_dir: str) -> str:
    input_type = "unknown-source-type"

    if os.path.isfile(working_dir):
        input_type = "file"
    elif os.path.isdir(working_dir):
        input_type = "dir"

    unique_id = uuid.uuid4()
    identifier = os.path.join(input_type, str(unique_id))
    if working_dir != ".":
        identifier = os.path.join(input_type, f"{working_dir}-{unique_id}")

    return urlunparse(
        ("https", "fluidattacks.com", identifier, "", "", ""),
    )


def merge_packages(packages: list[Package]) -> list[Package]:
    merged_packages: dict = {}

    for package in packages:
        if package.id_:
            if package.id_ in merged_packages:
                merged_packages[package.id_].locations.extend(
                    x for x in package.locations if x not in merged_packages[package.id_].locations
                )
            else:
                merged_packages[package.id_] = package
        else:
            merged_packages[package] = package

    return list(merged_packages.values())


def process_packages(packages: list[Package]) -> list[Package]:
    return merge_packages(packages)


def set_namespace_version(config: SbomConfig) -> tuple[str, str | None]:
    namespace = ""
    version = None
    if config.source_type == SourceType.DIRECTORY and isinstance(config.resolver, Directory):
        namespace = config.resolver.root
    if config.source_type == SourceType.DOCKER and isinstance(config.resolver, ContainerImage):
        namespace = config.resolver.context.image_ref
        version = config.resolver.context.id
    return namespace, version
