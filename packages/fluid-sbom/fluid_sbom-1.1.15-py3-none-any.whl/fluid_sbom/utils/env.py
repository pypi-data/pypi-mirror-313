from os import (
    environ,
)
from typing import (
    Literal,
)


def guess_environment() -> Literal["development", "production"]:
    return (
        "production"
        if environ.get("AWS_BATCH_JOB_ID") or environ.get("CI_COMMIT_REF_NAME") == "trunk"
        else "development"
    )
