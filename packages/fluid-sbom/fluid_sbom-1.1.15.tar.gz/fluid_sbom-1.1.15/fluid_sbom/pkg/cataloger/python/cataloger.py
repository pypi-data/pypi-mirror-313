from fnmatch import (
    fnmatch,
)

import reactivex
from reactivex.abc import (
    ObserverBase,
    SchedulerBase,
)

from fluid_sbom.pkg.cataloger.generic.cataloger import (
    Request,
)
from fluid_sbom.pkg.cataloger.python.parse_pipfile_deps import (
    parse_pipfile_deps,
)
from fluid_sbom.pkg.cataloger.python.parse_pipfile_lock import (
    parse_pipfile_lock_deps,
)
from fluid_sbom.pkg.cataloger.python.parse_poetry_lock import (
    parse_poetry_lock,
)
from fluid_sbom.pkg.cataloger.python.parse_pyproject_toml import (
    parse_pyproject_toml,
)
from fluid_sbom.pkg.cataloger.python.parse_requirements import (
    parse_requirements_txt,
)
from fluid_sbom.pkg.cataloger.python.parse_wheel_egg import (
    parse_wheel_or_egg,
)


def on_next_python(
    source: reactivex.Observable[str],
) -> reactivex.Observable[Request]:
    def subscribe(
        observer: ObserverBase[Request],
        scheduler: SchedulerBase | None = None,
    ) -> reactivex.abc.DisposableBase:
        def on_next(value: str) -> None:
            try:
                if fnmatch(value, "*requirements*.txt"):
                    observer.on_next(
                        Request(
                            real_path=value,
                            parser=parse_requirements_txt,
                            parser_name="python-requirements-cataloger",
                        ),
                    )
                elif any(
                    fnmatch(value, x) for x in ("*poetry.lock", "poetry.lock", "*/poetry.lock")
                ):
                    observer.on_next(
                        Request(
                            real_path=value,
                            parser=parse_poetry_lock,
                            parser_name="python-poetry-lock-cataloger",
                        ),
                    )
                elif any(
                    fnmatch(value, x)
                    for x in (
                        "**/*.egg-info",
                        "**/*dist-info/METADATA",
                        "**/*egg-info/PKG-INFO",
                        "**/*DIST-INFO/METADATA",
                        "**/*EGG-INFO/PKG-INFO",
                    )
                ):
                    observer.on_next(
                        Request(
                            real_path=value,
                            parser=parse_wheel_or_egg,
                            parser_name="python-installed-package-cataloger",
                        ),
                    )
                elif any(
                    fnmatch(value, pattern) for pattern in ("**/Pipfile.lock", "Pipfile.lock")
                ):
                    observer.on_next(
                        Request(
                            real_path=value,
                            parser=parse_pipfile_lock_deps,
                            parser_name="python-pipfile-lock-cataloger",
                        ),
                    )
                elif any(fnmatch(value, pattern) for pattern in ("**/Pipfile", "Pipfile")):
                    observer.on_next(
                        Request(
                            real_path=value,
                            parser=parse_pipfile_deps,
                            parser_name="python-pipfile-package-cataloger",
                        ),
                    )
                elif any(
                    fnmatch(value, pattern) for pattern in ("**/pyproject.toml", "pyproject.toml")
                ):
                    observer.on_next(
                        Request(
                            real_path=value,
                            parser=parse_pyproject_toml,
                            parser_name="python-pyproject-toml-cataloger",
                        ),
                    )
            except Exception as ex:  # noqa: BLE001
                observer.on_error(ex)

        return source.subscribe(
            on_next,
            observer.on_error,
            observer.on_completed,
            scheduler=scheduler,
        )

    return reactivex.create(subscribe)
