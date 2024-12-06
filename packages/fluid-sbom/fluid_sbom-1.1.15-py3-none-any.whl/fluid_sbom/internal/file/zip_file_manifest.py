import logging
from fnmatch import (
    fnmatch,
)
from zipfile import (
    BadZipFile,
    ZipFile,
    ZipInfo,
)

LOGGER = logging.getLogger(__name__)


def normalize_zip_entry_name(case_insensitive: bool, entry: str) -> str:
    if case_insensitive:
        entry = entry.lower()
    if not entry.startswith("/"):
        entry = "/" + entry

    return entry


def new_zip_file_manifest(archive_path: str) -> list[ZipInfo]:
    try:
        with ZipFile(archive_path, "r") as myzip:
            return myzip.infolist()
    except BadZipFile:
        return []


def zip_glob_match(manifest: list[ZipInfo], case_sensitive: bool, *patterns: str) -> list[str]:
    result = []

    for pattern in patterns:
        for entry in manifest:
            normalized_entry = normalize_zip_entry_name(case_sensitive, entry.filename)
            if entry.filename.endswith(pattern):
                result.append(entry.filename)
            if case_sensitive:
                pattern = pattern.lower()
            if fnmatch(normalized_entry, pattern):
                result.append(entry.filename)
    return result
