import os
from copy import (
    deepcopy,
)
from ctypes import (
    c_void_p,
    cdll,
)

from tree_sitter import (
    Language as TLanguage,
)
from tree_sitter import (
    Node,
    Parser,
)

from fluid_sbom.artifact.relationship import (
    Relationship,
    RelationshipType,
)
from fluid_sbom.file.location import (
    Location,
)
from fluid_sbom.file.location_read_closer import (
    LocationReadCloser,
)
from fluid_sbom.file.resolver import (
    Resolver,
)
from fluid_sbom.model.core import (
    Package,
)
from fluid_sbom.pkg.cataloger.elixir.package import (
    new_package,
)
from fluid_sbom.pkg.cataloger.generic.parser import (
    Environment,
)
from fluid_sbom.pkg.elixir import (
    ElixirMixLockEntry,
)


def lang_from_so(path: str, name: str) -> TLanguage:
    lib = cdll.LoadLibrary(os.fspath(path))
    language_function = getattr(lib, f"tree_sitter_{name}")
    language_function.restype = c_void_p
    language_ptr = language_function()
    return TLanguage(language_ptr)


def process_entry(entry: Node, location: Location) -> Package | None:
    name_value = next(x for x in entry.named_children if x.type == "package_name").text
    version_value = next(x for x in entry.named_children if x.type == "version").text
    pkg_hash_value = next(x for x in entry.named_children if x.type == "checksum").text
    pkg_hash_ext_value = next(x for x in entry.named_children if x.type == "optional_checksum").text

    if pkg_hash_ext_value and pkg_hash_value and version_value and name_value:
        name = name_value.decode("utf-8")[1:-1]
        version = version_value.decode("utf-8")[1:-1]
        pkg_hash = pkg_hash_value.decode("utf-8")[1:-1]
        pkg_hash_ext = pkg_hash_ext_value.decode("utf-8")[1:-1]
    else:
        return None

    new_location = deepcopy(location)
    if new_location.coordinates:
        new_location.coordinates.line = entry.start_point[0] + 1

    package = new_package(
        ElixirMixLockEntry(
            name=name,
            version=version,
            pkg_hash=pkg_hash,
            pkg_hash_ext=pkg_hash_ext,
        ),
        new_location,
    )

    return package if package else None


def collect_dependencies(
    packages: list[Package],
    package_entries: list[Node],
) -> list[Relationship]:
    relationships: list[Relationship] = []
    for entry in package_entries:
        pkg_name_value = next(x for x in entry.named_children if x.type == "package_name").text
        if pkg_name_value:
            current_package_name = pkg_name_value.decode("utf-8")[1:-1]
        else:
            continue

        for dependency_list in next(
            node for node in entry.named_children if node.type == "dependencies"
        ).named_children:
            dependencies = [
                value.decode("utf-8")[1:]
                for x in dependency_list.named_children
                if x.type == "dependency"
                and (value := next(y for y in x.named_children if y.type == "atom").text)
            ]
            relationships.extend(
                Relationship(
                    from_=next(x for x in packages if x.name == dep_name),
                    to_=next(x for x in packages if x.name == current_package_name),
                    type=RelationshipType.DEPENDENCY_OF_RELATIONSHIP,
                    data=None,
                )
                for dep_name in dependencies
                if next((x for x in packages if x.name == dep_name), None)
            )
    return relationships


def collect_entries(_content: str, location: Location) -> tuple[list[Package], list[Relationship]]:
    so_library_path: str = os.path.join(
        os.environ["TREE_SITTER_PARSERS_DIR"],
        "mix_lock.so",
    )
    parser_language = lang_from_so(so_library_path, "mix_lock")
    parser = Parser(parser_language)
    result = parser.parse(_content.encode("utf-8"))
    package_entries = list(
        node for node in result.root_node.children if node.type == "package_entry"
    )

    packages = [
        package for x in package_entries if (package := process_entry(x, location)) is not None
    ]
    relations = collect_dependencies(packages, package_entries)

    return packages, relations


def parse_mix_lock(
    _: Resolver | None,
    __: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    packages: list[Package] = []
    relationships: list[Relationship] = []
    so_library_path: str = os.path.join(
        os.environ["TREE_SITTER_PARSERS_DIR"],
        "mix_lock.so",
    )
    parser_language = lang_from_so(so_library_path, "mix_lock")
    parser = Parser(parser_language)

    result = parser.parse(reader.read_closer.read().encode("utf-8"))
    package_entries = list(
        node for node in result.root_node.children if node.type == "package_entry"
    )

    packages = [package for x in package_entries if (package := process_entry(x, reader.location))]
    relationships = collect_dependencies(packages, package_entries)

    return packages, relationships
