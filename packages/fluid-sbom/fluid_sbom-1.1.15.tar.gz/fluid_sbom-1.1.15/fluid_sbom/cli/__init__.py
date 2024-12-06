# pylint:disable=no-value-for-parameter
import logging
import os
import tempfile
import textwrap
from concurrent.futures import (
    ThreadPoolExecutor,
)
from typing import (
    Unpack,
)

import click

from fluid_sbom.advisories.database import (
    DATABASE,
)
from fluid_sbom.cli.options import (
    MutuallyExclusiveOption,
    RequiredAnyCommand,
)
from fluid_sbom.cli.sbom_config import (
    ScanArgs,
    build_sbom_config,
)
from fluid_sbom.config.bugsnag import (
    initialize_bugsnag,
)
from fluid_sbom.config.config import (
    SourceType,
)
from fluid_sbom.config.logger import (
    configure_logger,
)
from fluid_sbom.format import (
    format_sbom,
)
from fluid_sbom.internal.file_resolver.container_image import (
    ContainerImage,
    ImageContext,
)
from fluid_sbom.pkg.cataloger.complete import (
    complete_package,
)
from fluid_sbom.pkg.operations.package_operation import (
    package_operations_factory,
)
from fluid_sbom.sources.directory_source import (
    Directory,
)
from fluid_sbom.sources.docker import (
    ImageMetadata,
    extract_docker_image,
    get_docker_image,
)

LOGGER = logging.getLogger(__name__)


def show_banner() -> None:
    logo = textwrap.dedent(
        """
         ───── ⌝
        |    ⌝|  Fluid Attacks
        |  ⌝  |  We hack your software.
         ─────
        """,
    )
    click.secho(logo, fg="red")


def get_context(
    image: ImageMetadata,
    *,
    username: str | None = None,
    password: str | None = None,
    token: str | None = None,
    daemon: bool = False,
) -> ImageContext | None:
    temp_dir = tempfile.mkdtemp()
    layers_dir, manifest = extract_docker_image(
        image,
        temp_dir,
        username=username,
        password=password,
        token=token,
        daemon=daemon,
    )

    return ImageContext(
        id=image.digest,
        name=image.name,
        publisher="",
        arch=image.architecture,
        size=str(sum(x.size for x in image.layersdata)),
        full_extraction_dir=temp_dir,
        layers_dir=layers_dir,
        manifest=manifest,
        image_ref=image.image_ref,
    )


@click.command(cls=RequiredAnyCommand, required_any=["o_from", "config"])
@click.argument("arg")
@click.option(
    "--from",
    "o_from",
    type=click.Choice(["docker", "dir", "docker-daemon"], case_sensitive=False),
    help=(
        "Source of the scan: 'docker' for scanning Docker images "
        "or 'dir' for scanning directories."
    ),
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["config"],
)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(
        [
            "fluid-json",
            "cyclonedx-json",
            "spdx-json",
            "cyclonedx-xml",
            "spdx-xml",
        ],
        case_sensitive=False,
    ),
    default="fluid-json",
    help="Output format for the scanned data.",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["config"],
)
@click.option(
    "--output",
    "-o",
    help="Output filename.",
    default="sbom",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["config"],
)
@click.option(
    "--docker-user",
    default=None,
    help="Docker registry username.",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["config"],
)
@click.option(
    "--docker-password",
    default=None,
    help="Docker registry password.",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["config"],
)
@click.option(
    "--config",
    "-c",
    is_flag=True,
    default=False,
    cls=MutuallyExclusiveOption,
    help="Path to an advanced configuration file with additional settings.",
    mutually_exclusive=[
        "docker-user",
        "docker-password",
        "output_format",
        "output",
        "o_from",
    ],
)
def scan(arg: str, **kwargs: Unpack[ScanArgs]) -> None:
    configure_logger()
    initialize_bugsnag()
    show_banner()

    sbom_config = build_sbom_config(arg, **kwargs)

    match sbom_config.source_type:
        case SourceType.DIRECTORY:
            sbom_config.resolver = Directory(root=sbom_config.source, exclude=sbom_config.exclude)
        case SourceType.DOCKER | SourceType.DOCKER_DAEMON:
            daemon = sbom_config.source_type == SourceType.DOCKER_DAEMON
            docker_image = get_docker_image(
                sbom_config.source,
                username=sbom_config.docker_user,
                password=sbom_config.docker_password,
                daemon=daemon,
            )
            if not docker_image:
                raise ValueError(f"No image found for {sbom_config.source}")

            context = get_context(
                docker_image,
                username=sbom_config.docker_user,
                password=sbom_config.docker_password,
                daemon=daemon,
            )
            if context is None:
                raise ValueError(f"No context found for {docker_image}")
            sbom_config.resolver = ContainerImage(img=docker_image, context=context, lazy=False)
        case _:
            raise ValueError(f"Unknown source: {sbom_config.source}")

    DATABASE.initialize()
    LOGGER.info(
        "📦 Generating SBOM from %s: %s",
        sbom_config.source_type.value,
        sbom_config.source,
    )

    packages, relationships = package_operations_factory(sbom_config.resolver)
    with ThreadPoolExecutor(
        max_workers=min(32, (os.cpu_count() or 1) * 5 if os.cpu_count() is not None else 32),
    ) as executor:
        LOGGER.info("📦 Gathering additional package information")
        packages = list(filter(None, executor.map(complete_package, packages)))

    LOGGER.info("📦 Preparing %s report", sbom_config.output_format)
    format_sbom(packages, relationships, sbom_config)


if __name__ == "__main__":
    scan(prog_name="sbom")
