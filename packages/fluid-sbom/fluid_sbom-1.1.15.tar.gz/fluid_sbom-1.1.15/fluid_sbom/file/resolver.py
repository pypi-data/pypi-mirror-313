import abc
from collections.abc import Callable, Generator
from typing import (
    TextIO,
)

from pydantic import (
    BaseModel,
)

from fluid_sbom.file.location import (
    Location,
)
from fluid_sbom.file.metadata import (
    Metadata,
)


class ContentResolver(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls: type["ContentResolver"], subclass: object) -> bool:
        return (
            hasattr(subclass, "file_contents_by_location")
            and callable(subclass.file_contents_by_location)
        ) or NotImplemented

    @abc.abstractmethod
    def file_contents_by_location(
        self,
        location: Location,
        *,
        function_reader: Callable[..., TextIO] | None = None,
        mode: str | None = None,
    ) -> TextIO | None:
        """Resolve file context."""
        raise NotImplementedError


class MetadataResolver(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls: type["MetadataResolver"], subclass: object) -> bool:
        return (
            hasattr(subclass, "file_metadata_by_location")
            and callable(subclass.file_metadata_by_location)
        ) or NotImplemented

    @abc.abstractmethod
    def file_metadata_by_location(
        self,
        location: Location,
    ) -> Metadata | None:
        """Resolve file context."""
        raise NotImplementedError


class PathResolver(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls: type["PathResolver"], subclass: object) -> bool:
        return (
            hasattr(subclass, "has_path")
            and callable(subclass.has_path)
            and hasattr(subclass, "files_by_path")
            and callable(subclass.files_by_path)
            and hasattr(subclass, "files_by_glob")
            and callable(subclass.files_by_glob)
            and hasattr(subclass, "files_by_mime_type")
            and callable(subclass.files_by_mime_type)
            and hasattr(subclass, "relative_file_path")
            and callable(subclass.relative_file_path)
            and hasattr(subclass, "walk_file")
            and callable(subclass.walk_file)
        ) or NotImplemented

    @abc.abstractmethod
    def has_path(self, path: str) -> bool:
        """Resolve file context."""
        raise NotImplementedError

    @abc.abstractmethod
    def files_by_path(self, *paths: str) -> list[Location]:
        """Resolve file context."""
        raise NotImplementedError

    @abc.abstractmethod
    def files_by_glob(self, *patters: str) -> list[Location]:
        """Resolve file context."""
        raise NotImplementedError

    @abc.abstractmethod
    def files_by_mime_type(self, mime_type: str) -> list[Location]:
        """Resolve file context."""
        raise NotImplementedError

    @abc.abstractmethod
    def relative_file_path(self, _: Location, path: str) -> Location | None:
        """Resolve file context."""
        raise NotImplementedError

    @abc.abstractmethod
    def walk_file(self) -> Generator[str, None, None]:
        raise NotImplementedError


class Resolver(
    ContentResolver,
    PathResolver,
    MetadataResolver,
    BaseModel,
    metaclass=abc.ABCMeta,
):
    pass
