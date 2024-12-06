import bugsnag
from bugsnag_client import (
    add_batch_metadata as bugsnag_add_batch_metadata,
)
from bugsnag_client import (
    remove_nix_hash as bugsnag_remove_nix_hash,
)

from fluid_sbom.context import (
    BASE_DIR,
    CI_COMMIT_SHORT_SHA,
)
from fluid_sbom.utils import (
    env,
)


def initialize_bugsnag() -> None:
    bugsnag.before_notify(bugsnag_add_batch_metadata)
    bugsnag.before_notify(bugsnag_remove_nix_hash)
    bugsnag.configure(
        notify_release_stages=["production"],
        release_stage=env.guess_environment(),
        app_version=CI_COMMIT_SHORT_SHA,
        project_root=BASE_DIR,
        send_environment=True,
    )
    bugsnag.start_session()
