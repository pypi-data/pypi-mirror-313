from fluid_sbom.artifact.relationship import (
    Relationship,
)
from fluid_sbom.config.config import (
    SbomConfig,
)
from fluid_sbom.format.common import (
    process_packages,
)
from fluid_sbom.format.cyclone_dx.file_builder import (
    format_cyclonedx_sbom,
)
from fluid_sbom.format.fluid import (
    format_fluid_sbom,
)
from fluid_sbom.format.spdx.file_builder import (
    format_spdx_sbom,
)
from fluid_sbom.model.core import (
    Package,
)


def format_sbom(
    packages: list[Package],
    relationships: list[Relationship],
    config: SbomConfig,
) -> None:
    packages = process_packages(packages)
    match config.output_format:
        case "fluid-json":
            format_fluid_sbom(
                packages,
                relationships,
                config.output,
                config,
            )
        case "cyclonedx-json":
            format_cyclonedx_sbom(
                packages,
                relationships,
                config.output_format,
                config.output,
                config,
            )
        case "cyclonedx-xml":
            format_cyclonedx_sbom(
                packages,
                relationships,
                config.output_format,
                config.output,
                config,
            )
        case "spdx-json":
            format_spdx_sbom(
                packages,
                relationships,
                "json",
                config.output,
                config,
            )
        case "spdx-xml":
            format_spdx_sbom(
                packages,
                relationships,
                "xml",
                config.output,
                config,
            )
