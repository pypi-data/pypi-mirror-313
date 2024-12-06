import json
import logging
from datetime import (
    UTC,
    datetime,
)
from enum import (
    Enum,
)
from typing import (
    Any,
    cast,
)

from jsonschema import (
    validate,
)
from jsonschema.exceptions import (
    ValidationError,
)
from pydantic import (
    BaseModel,
)

from fluid_sbom.artifact.relationship import (
    Relationship,
)
from fluid_sbom.config.config import (
    SbomConfig,
)
from fluid_sbom.format.common import (
    set_namespace_version,
)
from fluid_sbom.format.types import (
    FLUID_SBOM_JSON_SCHEMA,
)
from fluid_sbom.internal.collection.types import (
    IndexedDict,
    IndexedList,
)
from fluid_sbom.model.core import (
    Package,
)
from fluid_sbom.utils.exceptions import (
    FluidJSONValidationError,
)

LOGGER = logging.getLogger(__name__)


class EnumEncoder(json.JSONEncoder):
    def default(self, item: Any) -> Any:  # pylint:disable=arguments-renamed
        if isinstance(item, Enum):
            return item.value
        if isinstance(item, IndexedList):
            return list(item.data)

        if isinstance(item, IndexedDict):
            return dict(item.data)
        if isinstance(item, BaseModel):
            item = item.model_dump if item else None
        if isinstance(item, datetime):
            return item.isoformat()
        return json.JSONEncoder.default(self, item)


def validate_pkgs(sbom_pkgs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pkgs_to_remove = []
    for index, pkg in enumerate(sbom_pkgs):
        try:
            pkg = json.loads(json.dumps(pkg, cls=EnumEncoder))
            sbom_pkgs[index] = pkg
        except TypeError:
            pkgs_to_remove.append(index)

    for index in reversed(sorted(pkgs_to_remove)):
        sbom_pkgs.pop(index)
    return sbom_pkgs


def format_fluid_sbom(  # pylint:disable=too-many-locals
    packages: list[Package],
    relationships: list[Relationship],
    output: str,
    config: SbomConfig,
) -> None:
    now_utc = datetime.now(UTC).isoformat()
    namespace, version = set_namespace_version(config=config)
    file_path = f"{output}.json"
    sbom_pkgs = [
        {
            "id": package.id_,
            "name": package.name,
            "version": package.version,
            "locations": [
                {
                    "path": location.path(),
                    "line": location.coordinates.line
                    if location.coordinates and location.coordinates.line
                    else None,
                    "layer": location.coordinates.file_system_id
                    if location.coordinates and location.coordinates.file_system_id
                    else None,
                    "dependency_type": location.dependency_type.value,
                }
                for location in package.locations
            ],
            "licenses": package.licenses,
            "type": package.type.value,
            "language": package.language.value,
            "platform": package.language.get_platform_value(),
            "package_url": package.p_url,
            "found_by": package.found_by,
            "health_metadata": package.health_metadata.model_dump()
            if package.health_metadata
            else None,
            "advisories": [advisory.model_dump() for advisory in package.advisories or []],
        }
        for package in packages
    ]

    sbom_pkgs = validate_pkgs(sbom_pkgs)
    sbom_details = {
        "name": namespace,
        "version": version if version else None,
        "timestamp": now_utc,
        "tool": "Fluid-Sbom",
        "organization": "Fluid attacks",
    }
    dependency_map: dict[str, list[str]] = {}

    for relationship in relationships:
        from_pkg = cast(Package, relationship.from_)
        to_pkg = cast(Package, relationship.to_)
        ref = f"{to_pkg.id_}"
        dep = f"{from_pkg.id_}"

        if ref not in dependency_map:
            dependency_map[ref] = []

        dependency_map[ref].append(dep)

    sbom_relationships = [
        {"from": ref, "to": depends_on_list} for ref, depends_on_list in dependency_map.items()
    ]
    result = {
        "sbom_details": sbom_details,
        "packages": sbom_pkgs,
        "relationships": sbom_relationships,
    }

    try:
        validate(result, FLUID_SBOM_JSON_SCHEMA)
    except ValidationError as ex:
        raise FluidJSONValidationError(ex) from None

    LOGGER.info("🆗 Valid Fluid JSON format, generating output file at %s", file_path)
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(result, json_file, indent=4, cls=EnumEncoder)
    LOGGER.info("✅ Output file successfully generated")
