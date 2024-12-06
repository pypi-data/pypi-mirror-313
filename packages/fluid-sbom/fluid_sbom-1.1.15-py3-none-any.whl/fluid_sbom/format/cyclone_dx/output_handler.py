import logging
from typing import (
    TYPE_CHECKING,
)

from cyclonedx.model.bom import (
    Bom,
)
from cyclonedx.output import (
    make_outputter,
)
from cyclonedx.schema import (
    OutputFormat,
    SchemaVersion,
)
from cyclonedx.validation import (
    make_schemabased_validator,
)
from cyclonedx.validation.json import (
    JsonStrictValidator,
)

from fluid_sbom.utils.exceptions import (
    CycloneDXValidationError,
)

LOGGER = logging.getLogger(__name__)

if TYPE_CHECKING:
    from cyclonedx.output.json import (
        Json as JsonOutputter,
    )
    from cyclonedx.output.xml import (
        Xml as XmlOutputter,
    )
    from cyclonedx.validation.xml import (
        XmlValidator,
    )


def format_cyclone_json(bom: Bom, output: str) -> None:
    file_path = f"{output}.json"
    json_output: JsonOutputter = make_outputter(
        bom=bom,
        output_format=OutputFormat.JSON,
        schema_version=SchemaVersion.V1_6,
    )
    serialized_json = json_output.output_as_string()

    json_validator = JsonStrictValidator(SchemaVersion.V1_6)
    validation_error = json_validator.validate_str(serialized_json)

    if validation_error:
        raise CycloneDXValidationError(validation_error)

    LOGGER.info(
        "🆗 Valid CYCLONEDX JSON format, generating output file at %s",
        file_path,
    )
    json_output.output_to_file(file_path, True, indent=2)
    LOGGER.info("✅ Output file successfully generated")


def format_cyclone_xml(bom: Bom, output: str) -> None:
    file_path = f"{output}.xml"
    xml_outputter: XmlOutputter = make_outputter(
        bom=bom,
        output_format=OutputFormat.XML,
        schema_version=SchemaVersion.V1_6,
    )
    serialized_xml = xml_outputter.output_as_string()

    xml_validator: XmlValidator = make_schemabased_validator(
        output_format=OutputFormat.XML,
        schema_version=SchemaVersion.V1_6,
    )
    validation_error = xml_validator.validate_str(serialized_xml)

    if validation_error:
        raise CycloneDXValidationError(validation_error)

    LOGGER.info("🆗 Valid CYCLONEDX XML format, generating output file at %s", file_path)
    xml_outputter.output_to_file(file_path, True, indent=2)
    LOGGER.info("✅ Output file successfully generated")
