from enum import (
    Enum,
)


class DependencyType(Enum):
    DIRECT: str = "DIRECT"
    TRANSITIVE: str = "TRANSITIVE"
    UNKNOWN: str = "UNKNOWN"
