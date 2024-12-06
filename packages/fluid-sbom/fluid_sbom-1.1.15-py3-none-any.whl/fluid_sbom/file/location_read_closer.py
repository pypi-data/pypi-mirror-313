from io import (
    TextIOWrapper,
)
from typing import (
    TextIO,
)

from pydantic import (
    BaseModel,
    ConfigDict,
)

from fluid_sbom.file.location import (
    Location,
)


class LocationReadCloser(BaseModel):
    location: Location
    read_closer: TextIO | TextIOWrapper
    model_config = ConfigDict(arbitrary_types_allowed=True)
