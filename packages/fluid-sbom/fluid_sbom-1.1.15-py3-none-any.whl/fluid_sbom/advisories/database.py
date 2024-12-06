import atexit
import logging
import os
import sqlite3
import subprocess  # nosec
import sys
from typing import (
    Literal,
    cast,
)

import boto3
from botocore import (
    UNSIGNED,
)
from botocore.config import (
    Config,
)
from botocore.exceptions import (
    ClientError,
)
from platformdirs import (
    user_data_dir,
)
from tqdm import (
    tqdm,
)

LOGGER = logging.getLogger(__name__)

BUCKET_NAME = "fluidattacks.public.storage"
DB_NAME = "vulnerability.db"
FILE_KEY = f"sbom/{DB_NAME}.zst"
CONFIG_DIRECTORY = user_data_dir(
    appname="fluid-sbom",
    appauthor="fluidattacks",
    ensure_exists=True,
)
DB_PATH = os.path.join(CONFIG_DIRECTORY, DB_NAME)
DB_COMPRESSED_PATH = f"{DB_PATH}.zst"

S3_SERVICE_NAME: Literal["s3"] = "s3"
S3_CLIENT = boto3.client(
    service_name=S3_SERVICE_NAME,
    config=Config(
        region_name="us-east-1",
        signature_version=UNSIGNED,  # type: ignore[misc]
    ),
)


def _download_database_file(download_size: float) -> None:
    LOGGER.info("⬇️ Downloading advisories database")
    with tqdm(
        leave=False,
        total=download_size,
        unit="B",
        unit_scale=True,
        file=sys.stdout,
    ) as progress_bar:
        S3_CLIENT.download_file(
            Bucket=BUCKET_NAME,
            Callback=progress_bar.update,
            Filename=DB_COMPRESSED_PATH,
            Key=FILE_KEY,
        )


def _decompress_database_file() -> None:
    LOGGER.info("🗜️ Decompressing advisories database")
    with subprocess.Popen(  # nosec
        ["zstd", "-d", "-f", DB_COMPRESSED_PATH],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ) as process:
        _, stderr = process.communicate()
        if cast(int, process.returncode) != 0:
            raise RuntimeError(stderr.decode())


def _is_database_available() -> bool:
    local_database_exists = os.path.isfile(DB_PATH)

    try:
        db_metadata = S3_CLIENT.head_object(Bucket=BUCKET_NAME, Key=FILE_KEY)
        up_to_date = (
            local_database_exists
            and os.path.getmtime(DB_PATH) >= db_metadata["LastModified"].timestamp()
        )

        if up_to_date:
            LOGGER.info("✅ Advisories database is up to date")
            return True

        _download_database_file(db_metadata["ContentLength"])
        _decompress_database_file()
        os.unlink(DB_COMPRESSED_PATH)
        return True
    except (ClientError, RuntimeError):  # type: ignore[misc]
        if local_database_exists:
            LOGGER.warning(
                "⚠️ Advisories may be outdated, unable to update database",
            )
            return True

        LOGGER.exception(
            "❌ Advisories won't be included, unable to download database",
        )
        return False


class Database:
    def __init__(self) -> None:
        self.connection: sqlite3.Connection | None = None

    def initialize(self) -> None:
        if self.connection is None and _is_database_available():
            self.connection = sqlite3.connect(
                DB_PATH,
                # Should be OK as we are only reading, not writing
                check_same_thread=False,
            )
            atexit.register(self.connection.close)

    def get_connection(self) -> sqlite3.Connection | None:
        return self.connection


DATABASE = Database()
