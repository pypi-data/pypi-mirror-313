from cyclonedx.validation import (
    ValidationError as CycloneDXError,
)
from jsonschema import (
    ValidationError as JSONSchemaError,
)
from spdx_tools.spdx.validation.validation_message import (
    ValidationMessage,
)
from tree_sitter import (
    Node,
)


class CustomBaseError(Exception):
    """Base exception class for custom exceptions."""


class CycloneDXValidationError(CustomBaseError):
    """Exception for CycloneDX validation errors."""

    def __init__(self, error: CycloneDXError) -> None:
        """Initialize the constructor."""
        header = "Exception - CycloneDx validation error\n"
        msg = f"❌ {header}{error}"
        super().__init__(msg)


class DuplicatedKeyError(CustomBaseError):
    """Exception raised for duplicated keys."""

    def __init__(self, key: str) -> None:
        """Initialize the constructor."""
        super().__init__(f"Defining a key multiple times is invalid: {key}")


class ForbiddenModuleImportedError(CustomBaseError):
    """Exception raised when a forbidden module is imported."""


class FluidJSONValidationError(CustomBaseError):
    """Exception for Fluid JSON validation errors."""

    def __init__(self, error: JSONSchemaError) -> None:
        """Initialize the constructor."""
        header = "Exception - Fluid JSON validation error\n"
        msg = f"❌ {header}{error}"
        super().__init__(msg)


class InvalidDocumentKeyPairError(CustomBaseError):
    """Exception raised for invalid document key pairs."""


class InvalidDBFormatError(CustomBaseError):
    """Exception raised for invalid DB format."""


class InvalidTypeError(CustomBaseError):
    """Exception raised for invalid types."""


class InvalidMetadataError(CustomBaseError):
    """Exception raised for when metadata is invalid."""

    def __init__(self, error_message: str) -> None:
        message = error_message
        super().__init__(message)


class InvalidConfigFileError(CustomBaseError):
    """Exception raised for when the sbom config file is invalid."""

    def __init__(self, error_message: str) -> None:
        message = error_message
        super().__init__(message)


class SPDXValidationError(CustomBaseError):
    """Exception for SPDX validation errors."""

    def __init__(self, error_messages: list[ValidationMessage]) -> None:
        """Initialize the constructor."""
        header = "Exception - SPDX validation error\n"
        error_details = "\n".join(
            (f"Validation error: {message.validation_message}\nContext: {message.context}")
            for message in error_messages
        )
        msg = f"❌ {header}{error_details}"
        super().__init__(msg)


class UnexpectedExceptionError(CustomBaseError):
    """Exception for unexpected errors encountered during SBOM execution."""

    def __init__(self, error: Exception) -> None:
        """Initialize the constructor."""
        header = (
            "Exception - An unexpected exception was encountered "
            "during SBOM execution. The process will be terminated to prevent "
            "potential inconsistencies.\n"
        )
        msg = f"❌ {header}{error}"
        super().__init__(msg)


class UnexpectedNodeError(CustomBaseError):
    """Exception raised for unexpected nodes."""

    def __init__(self, node: Node | str) -> None:
        type_name = node.type if isinstance(node, Node) else node
        if isinstance(node, Node) and node.text:
            value = node.text.decode("utf-8")
            super().__init__(
                f"Unexpected node type {type_name} with value {value}",
            )
        else:
            super().__init__(f"Unexpected node type {type_name}")


class UnexpectedNodeTypeError(CustomBaseError):
    """Exception raised for unexpected node types."""

    def __init__(self, node: Node | str, expected_type: str | None = None) -> None:
        type_name = node.type if isinstance(node, Node) else node
        if expected_type:
            super().__init__(f"Unexpected node type {type_name} for {expected_type}")
        else:
            super().__init__(f"Unexpected node type {type_name}")


class UnexpectedValueTypeError(CustomBaseError):
    """Exception raised for unexpected value types."""


class UnexpectedChildrenLengthError(CustomBaseError):
    """Exception raised for nodes with unexpected number of children."""

    def __init__(self, node: Node | str, expected_length: int) -> None:
        type_name = node.type if isinstance(node, Node) else node
        super().__init__(f"Unexpected node type {type_name} for {expected_length} children")
