import logging
from typing import (
    Any,
)

import phpserialize
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
from fluid_sbom.pkg.cataloger.php.package import (
    package_url_from_pecl,
)

LOGGER = logging.getLogger(__name__)


def php_to_python(obj: Any) -> Any:
    if isinstance(obj, phpserialize.phpobject):
        return {k: php_to_python(v) for k, v in obj.__dict__.items()}
    if isinstance(obj, dict):
        return {php_to_python(k): php_to_python(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [php_to_python(i) for i in obj]

    return obj


def parse_pecl_serialized(
    _: Resolver | None,
    __: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    packages: list[Package] = []
    relationships: list[Relationship] = []

    unserialized_data = phpserialize.loads(reader.read_closer.read().encode(), decode_strings=True)
    parsed_data = php_to_python(unserialized_data)
    name = parsed_data.get("name")
    version = parsed_data.get("version", {}).get("release")

    if not name or not version:
        return [], []

    try:
        packages.append(
            Package(
                name=name,
                version=version,
                locations=[reader.location],
                language=Language.PHP,
                licenses=[],
                type=PackageType.PhpPeclPkg,
                metadata=None,
                p_url=package_url_from_pecl(name, version),
            ),
        )
        return packages, relationships
    except ValidationError as ex:
        LOGGER.warning(
            "Malformed package. Required fields are missing or data types are incorrect.",
            extra={
                "extra": {
                    "exception": ex.errors(include_url=False),
                    "location": reader.location.path(),
                },
            },
        )
        return [], []
