from contextlib import (
    suppress,
)

from fluid_sbom.pkg.cataloger.redhat.rpmdb import (
    berkeley,
    sqlite,
)
from fluid_sbom.pkg.cataloger.redhat.rpmdb.entry import (
    header_import,
)
from fluid_sbom.pkg.cataloger.redhat.rpmdb.ndb import (
    RpmNDB,
)
from fluid_sbom.pkg.cataloger.redhat.rpmdb.package import (
    PackageInfo,
    get_nevra,
)
from fluid_sbom.pkg.cataloger.redhat.rpmdb.rpmdb_interface import (
    RpmDBInterface,
)
from fluid_sbom.utils.exceptions import (
    InvalidDBFormatError,
)


class RpmDB:  # pylint:disable=too-few-public-methods
    def __init__(self, database: RpmDBInterface) -> None:
        self.database = database

    def list_packages(
        self,
    ) -> list[PackageInfo]:
        packages: list[PackageInfo] = []
        for entry in self.database.read():
            try:
                index_entries = header_import(entry)
            except ValueError as exc:
                raise ValueError("Failed to import header") from exc
            if index_entries:
                package = get_nevra(index_entries)
                packages.append(package)
        return packages


def open_db(file_path: str) -> RpmDB | None:
    """Attempt to open an RPM database from the specified file path and returns an RpmDB instance.

    If the database is invalid or the metadata cannot be
    validated, None is returned.

    The function first tries to open the database as an SQLite database, and
    if that fails, it attempts to open it as a Berkeley DB. If both attempts
    fail, None is returned.

    :param file_path: The path to the RPM database file.
    :type file_path: str
    :return: An RpmDB instance if the database is valid, otherwise None.
    :rtype: RpmDB | None
    """
    with suppress(InvalidDBFormatError):
        return RpmDB(sqlite.open_sqlite(file_path))

    with suppress(InvalidDBFormatError):
        return RpmDB(RpmNDB.open(file_path))

    with suppress(InvalidDBFormatError):
        return RpmDB(berkeley.open_berkeley(file_path))

    return None
