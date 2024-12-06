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
from fluid_sbom.pkg.cataloger.swift.parse_package_resolved import (
    parse_package_resolved,
)
from fluid_sbom.pkg.cataloger.swift.parse_podfile_lock import (
    parse_podfile_lock,
)


def on_next_swift(
    source: reactivex.Observable[str],
) -> reactivex.Observable[Request]:
    def subscribe(
        observer: ObserverBase[Request],
        scheduler: SchedulerBase | None = None,
    ) -> reactivex.abc.DisposableBase:
        def on_next(value: str) -> None:
            try:
                if any(fnmatch(value, x) for x in ("**/Package.resolved", "**/.package.resolved")):
                    observer.on_next(
                        Request(
                            real_path=value,
                            parser=parse_package_resolved,
                            parser_name="parse-swift-parse-package-resolved",
                        ),
                    )
                elif fnmatch(value, "**/Podfile.lock"):
                    observer.on_next(
                        Request(
                            real_path=value,
                            parser=parse_podfile_lock,
                            parser_name="parse-swift-parse-podfile-lock",
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
