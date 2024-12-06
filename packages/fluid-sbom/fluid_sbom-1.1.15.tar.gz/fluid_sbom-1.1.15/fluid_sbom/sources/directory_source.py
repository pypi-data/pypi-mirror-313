import glob
import logging
import os
import re
from collections.abc import Callable, Generator
from fnmatch import (
    translate,
)
from typing import (
    TextIO,
)

import magic
from pydantic import (
    BaseModel,
)

from fluid_sbom.file.coordinates import (
    Coordinates,
)
from fluid_sbom.file.location import (
    Location,
)
from fluid_sbom.file.metadata import (
    Metadata,
)
from fluid_sbom.file.resolver import (
    Resolver,
)
from fluid_sbom.file.type import (
    Type,
)

LOGGER = logging.getLogger(__name__)


def _normalize_rules(rules: tuple[str, ...]) -> tuple[str, ...]:
    normalized_rules: list[str] = []
    for rule in rules:
        normalized_rule = rule
        if normalized_rule == ".":
            normalized_rule = "glob(**)"
        elif normalized_rule.endswith("/"):
            normalized_rule += "**"

        if not normalized_rule.startswith("glob"):
            normalized_rule = f"glob({normalized_rule})"

        normalized_rules.append(normalized_rule)

    return tuple(normalized_rules)


class Directory(Resolver, BaseModel):
    root: str
    exclude: tuple[str, ...]

    def __post__init__(self, root: str, exclude: tuple[str, ...]) -> None:
        self.root = os.path.realpath(os.path.abspath(root))
        self.exclude = exclude

    def has_path(self, path: str) -> bool:
        path = os.path.join(self.root, path.lstrip("/"))
        return os.path.exists(path)

    def files_by_path(self, *paths: str) -> list[Location]:
        locations: list[Location] = []
        for path in paths:
            relative_path = path.replace(self.root, "").lstrip("/")
            full_path = os.path.join(self.root, relative_path)
            if os.path.exists(full_path):
                locations.append(
                    Location(
                        coordinates=Coordinates(real_path=full_path, file_system_id=""),
                        access_path=relative_path,
                        annotations={},
                    ),
                )
        return locations

    def files_by_glob(self, *patters: str) -> list[Location]:
        result = []
        for pattern in patters:
            for item in glob.glob(pattern, root_dir=self.root):
                result.append(
                    Location(
                        coordinates=Coordinates(
                            real_path=os.path.join(self.root, item),
                            file_system_id="",
                        ),
                        access_path=item,
                        annotations={},
                    ),
                )

        return result

    def files_by_mime_type(self, mime_type: str) -> list[Location]:
        matching_files = []
        mime_detector = magic.Magic(mime=True)

        for dirpath, _, filenames in os.walk(self.root):
            for filename in filenames:
                relative_path = os.path.join(dirpath, filename).replace(self.root, "").lstrip("/")
                result_mime_type = mime_detector.from_file(relative_path)
                if mime_type == result_mime_type:
                    matching_files.append(
                        Location(
                            coordinates=Coordinates(
                                real_path=os.path.join(self.root, relative_path),
                                file_system_id="",
                            ),
                            access_path=relative_path,
                            annotations={},
                        ),
                    )

        return matching_files

    def file_contents_by_location(
        self,
        location: Location,
        *,
        function_reader: Callable[..., TextIO] | None = None,
        mode: str | None = None,
    ) -> TextIO | None:
        if (
            location.coordinates
            and location.coordinates.real_path is not None
            and os.path.exists(location.coordinates.real_path)
        ):
            return (function_reader or open)(  # type: ignore
                location.coordinates.real_path,
                encoding="utf-8",
                mode=mode or "r",
            )

        return None

    def file_metadata_by_location(self, location: Location) -> Metadata | None:
        link_destination = None
        if not location.access_path:
            return None

        stats = os.stat(location.access_path, follow_symlinks=False)

        if os.path.islink(location.access_path):
            file_type = Type.TYPE_SYM_LINK
            link_destination = os.readlink(location.access_path)
        elif os.path.isdir(location.access_path):
            file_type = Type.TYPE_DIRECTORY
        elif os.path.isfile(location.access_path):
            file_type = Type.TYPE_REGULAR
        else:
            file_type = Type.TYPE_IRREGULAR

        mime_type = magic.Magic(mime=True).from_file(location.access_path)

        return Metadata(
            path=location.access_path,
            link_destination=link_destination or "",
            user_id=stats.st_uid,
            group_id=stats.st_gid,
            type=file_type,
            mime_type=mime_type,
        )

    def relative_file_path(self, _: Location, _path: str) -> Location:
        return Location(
            coordinates=Coordinates(real_path=_path, file_system_id="", line=None),
            access_path=_path.replace(self.root, "").lstrip("/"),
        )

    def walk_file(self) -> Generator[str, None, None]:
        excluded_dirs = ["node_modules", "dist", "__pycache__"]
        exclude_regex = [
            translate(os.path.join(self.root, glob[5:-1]))
            for glob in _normalize_rules(self.exclude)
        ]

        for dirpath, _, filenames in os.walk(self.root):
            if any(
                (
                    dirpath.endswith(excluded_dir)
                    or f"{os.path.sep}{excluded_dir}{os.path.sep}" in dirpath
                )
                for excluded_dir in excluded_dirs
            ):
                continue

            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                if any(re.match(regex, full_path) for regex in exclude_regex):
                    continue

                relative_path = full_path.replace(self.root, "").lstrip("/")
                yield relative_path


class DirectoryConfig(BaseModel):
    path: str
    exclude: tuple[str, ...]


class DirectorySource(BaseModel):
    config: DirectoryConfig
    resolver: Directory | None = None

    def file_resolver(self) -> Resolver:
        if self.resolver is None:
            self.resolver = Directory(root=self.config.path, exclude=self.config.exclude)
        return self.resolver


def new_from_directory_path(path: str, exclude: tuple[str, ...]) -> DirectorySource | None:
    return new_from_directory(DirectoryConfig(path=path, exclude=exclude))


def new_from_directory(cfg: DirectoryConfig) -> DirectorySource | None:
    if not os.path.isdir(cfg.path):
        LOGGER.error("Given path is not a directory: %s", cfg.path)
        return None

    return DirectorySource(config=cfg, resolver=None)
