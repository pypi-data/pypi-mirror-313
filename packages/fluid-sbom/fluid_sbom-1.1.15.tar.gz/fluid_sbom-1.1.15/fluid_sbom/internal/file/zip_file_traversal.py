import logging
import zipfile
from collections.abc import Callable
from contextlib import (
    suppress,
)


def traverse_files_in_zip(
    archive_path: str,
    visitor: Callable[[zipfile.ZipInfo], None],
    *paths: str,
) -> None:
    """Traverse files in a zip file applying a visitor function to each file."""
    with zipfile.ZipFile(archive_path, "r") as zip_reader:
        for path in paths:
            try:
                visitor(zip_reader.getinfo(path))
            except KeyError:
                logging.exception("Unable to find file: %s", path)


def contents_from_zip(archive_path: str, *paths: str) -> dict[str, str]:
    """Extract specified files from a zip archive and return their contents."""
    results: dict[str, str] = {}

    if not paths:
        return results  # Return empty result if no paths are specified

    def visitor(file: zipfile.ZipInfo) -> None:
        """Visitor function to read the contents of a file in the zip."""
        if file.is_dir():
            logging.error("Unable to extract directories, only files: %s", file.filename)
            return
        with zipfile.ZipFile(archive_path, "r") as zip_reader:
            with zip_reader.open(file) as file_data:
                content = file_data.read()  # Read the content of the file
                with suppress(UnicodeDecodeError):
                    results[file.filename] = content.decode(
                        "utf-8",
                    )  # Assuming UTF-8 encoding for simplicity

    traverse_files_in_zip(archive_path, visitor, *paths)
    return results
