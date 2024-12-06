import fnmatch
import os
import tarfile
import tempfile
from collections.abc import Callable, Generator
from contextlib import (
    suppress,
)
from pathlib import (
    Path,
)
from typing import (
    Any,
    TextIO,
)

from pydantic import (
    BaseModel,
)

from fluid_sbom.file.location import (
    Location,
    new_location_from_image,
)
from fluid_sbom.file.metadata import (
    Metadata,
)
from fluid_sbom.file.resolver import (
    Resolver,
)
from fluid_sbom.file.type import (
    get_type_from_tar_member,
)
from fluid_sbom.sources.docker import (
    ImageMetadata,
)


class LayerInfo(BaseModel):
    id_: str
    tar_full_path: str
    metadata: dict[str, Any]


class ImageContext(BaseModel):
    id: str
    name: str
    publisher: str | None
    arch: str
    size: str
    full_extraction_dir: str
    layers_dir: str
    manifest: dict[str, Any]
    image_ref: str

    def get_layer_info(self, layer_id: str) -> LayerInfo | None:
        if layer_metadata := next(x for x in self.manifest["Layers"] if x["id"] == layer_id):
            return LayerInfo(
                id_=layer_id,
                tar_full_path=os.path.join(self.layers_dir, layer_metadata),
                metadata=layer_metadata,
            )
        return None


class ContainerImage(Resolver, BaseModel):
    img: ImageMetadata
    context: ImageContext
    lazy: bool = True

    def _has_path_lazy(self, path: str) -> bool:
        success = []
        paths = [path, path.lstrip("/")]
        for layer_info in self.context.manifest["Layers"]:
            layer_dir = os.path.join(layer_info["id"], "layer.tar")
            with tarfile.open(os.path.join(self.context.layers_dir, layer_dir)) as tar:
                exists = False
                for _path in paths:
                    try:
                        tar.getmember(_path)
                        success.append(True)
                        exists = True
                        break
                    except KeyError:
                        success.append(False)
                if exists:
                    break

        return any(success)

    def _has_path(self, path: str) -> bool:
        layer_ids = [x["digest"] for x in self.context.manifest["layers"]]

        success = []
        path = path.lstrip(os.path.sep)
        for layer_id in layer_ids:
            p_file_path = os.path.join(self.context.full_extraction_dir, layer_id, path)
            if os.path.exists(p_file_path):
                success.append(True)
                break

        return any(success)

    def has_path(self, path: str) -> bool:
        if self.lazy:
            return self._has_path_lazy(path)

        return self._has_path(path)

    def _search_path_lazy(self, path: str) -> list[Location]:
        # A path can be in multiple layers
        locations: list[Location] = []
        for layer_info in self.context.manifest["layers"]:
            layer_dir = os.path.join(layer_info["id"], "layer.tar")
            with tarfile.open(os.path.join(self.context.layers_dir, layer_dir)) as tar:
                with suppress(KeyError):
                    member = tar.getmember(path)
                    locations.append(
                        new_location_from_image(
                            member.name,
                            str(Path(layer_dir).parent),
                        ),
                    )

        return locations

    def _search_path(self, path: str) -> list[Location]:
        if self.lazy:
            return self._search_path_lazy(path)

        locations: list[Location] = []
        layer_ids = [x["digest"] for x in self.context.manifest["layers"]]

        # A path can be in multiple layers
        for layer_id in layer_ids:
            p_file_path = os.path.join(
                self.context.full_extraction_dir,
                layer_id,
                path.lstrip(os.path.sep),
            )
            if os.path.exists(p_file_path):
                locations.append(
                    new_location_from_image(
                        path,
                        layer_id,
                        p_file_path,
                    ),
                )
        return locations

    def files_by_path(self, *paths: str) -> list[Location]:
        locations: list[Location] = []

        for path in paths:
            if find_path := self._search_path(path.lstrip("/")):
                locations.extend(find_path)
            else:
                locations.extend(self._search_path(path))
        return locations

    def files_by_glob(self, *patterns: str) -> list[Location]:
        locations: list[Location] = []
        for layer_info in self.context.manifest["Layers"]:
            layer_dir = os.path.join(layer_info["id"], "layer.tar")
            with tarfile.open(os.path.join(self.context.layers_dir, layer_dir)) as tar:
                for member in tar.getmembers():
                    for glob in patterns:
                        if fnmatch.fnmatch(member.name, glob):
                            locations.append(
                                new_location_from_image(
                                    member.name,
                                    str(Path(layer_dir).parent),
                                    os.path.join(
                                        self.context.full_extraction_dir,
                                        member.name,
                                    ),
                                ),
                            )
        return locations

    def _file_contents_by_location_lazy(
        self,
        location: Location,
        *,
        function_reader: Callable[..., TextIO] | None = None,
        mode: str | None = None,
    ) -> TextIO | None:
        for layer_info in self.context.manifest["Layers"]:
            layer_dir = os.path.join(layer_info["id"], "layer.tar")
            if (
                location.coordinates
                and location.coordinates.file_system_id
                and location.coordinates.file_system_id not in layer_dir
            ):
                continue
            with tarfile.open(os.path.join(self.context.layers_dir, layer_dir)) as tar:
                with suppress(KeyError):
                    if location.access_path:
                        member = tar.getmember(location.access_path)
                        if member.linkpath:
                            link_target_path = os.path.normpath(
                                os.path.join(
                                    os.path.dirname(member.name),
                                    member.linkname,
                                ),
                            )
                            member = tar.getmember(link_target_path)
                        temp_dir = tempfile.mkdtemp()
                        tar.extract(tar.getmember(member.name), temp_dir)
                        return (function_reader or open)(  # type: ignore
                            os.path.join(temp_dir, member.name),
                            encoding="utf-8",
                            mode=mode or "r",
                        )

        return None

    def file_contents_by_location(
        self,
        location: Location,
        *,
        function_reader: Callable[..., TextIO] | None = None,
        mode: str | None = None,
    ) -> TextIO | None:
        if (
            not self.lazy
            and location.coordinates
            and os.path.exists(location.coordinates.real_path)
        ):
            return (function_reader or open)(  # type: ignore
                location.coordinates.real_path,
                encoding="utf-8",
                mode=mode or "r",
            )

        if self.lazy:
            return self._file_contents_by_location_lazy(
                location,
                function_reader=function_reader,
                mode=mode,
            )

        return None

    def file_metadata_by_location(
        self,
        location: Location,
    ) -> Metadata | None:
        if (
            location.coordinates is not None
            and location.coordinates.file_system_id is not None
            and (_layer_info := self.context.get_layer_info(location.coordinates.file_system_id))
        ):
            with tarfile.open(os.path.join(_layer_info.tar_full_path)) as tar:
                tar_member = tar.getmember(location.coordinates.real_path)

                return Metadata(
                    path=tar_member.name,
                    link_destination=tar_member.linkname,
                    user_id=tar_member.uid,
                    group_id=tar_member.gid,
                    type=get_type_from_tar_member(tar_member),
                    mime_type="",
                )

        return None

    def files_by_mime_type(self, _mime_type: str) -> list[Location]:
        raise NotImplementedError

    def relative_file_path(self, _: Location, _path: str) -> Location | None:
        files = self.files_by_path(_path)
        if not files:
            return None
        return files[0]

    def walk_file_lazy(self) -> Generator[str, None, None]:
        for layer_info in self.context.manifest["Layers"]:
            layer_dir = os.path.join(layer_info["id"], "layer.tar")
            with tarfile.open(os.path.join(self.context.layers_dir, layer_dir)) as tar:
                for member in tar.getmembers():
                    yield member.name

    def walk_file(self) -> Generator[str, None, None]:
        if self.lazy:
            yield from self.walk_file_lazy()
        else:
            layer_ids = [x["digest"] for x in self.context.manifest["layers"]]
            for layer_id in layer_ids:
                current_layer_path = os.path.join(self.context.full_extraction_dir, layer_id)
                for root, _, files in os.walk(current_layer_path):
                    for file in files:
                        yield os.path.join(
                            os.path.sep,
                            root.replace(current_layer_path, ""),
                            file,
                        )
