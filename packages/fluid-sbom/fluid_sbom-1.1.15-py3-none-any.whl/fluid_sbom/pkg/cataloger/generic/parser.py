from collections.abc import Callable

from pydantic import (
    BaseModel,
    ConfigDict,
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
from fluid_sbom.linux.release import (
    Release,
)
from fluid_sbom.model.core import (
    Package,
)


class Environment(BaseModel):
    linux_release: Release | None
    model_config = ConfigDict(frozen=True)


Parser = Callable[
    [Resolver, Environment, LocationReadCloser],
    tuple[list[Package], list[Relationship]] | None,
]
