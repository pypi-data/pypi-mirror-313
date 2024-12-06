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
from fluid_sbom.pkg.cataloger.javascript.parse_html_scripts import (
    parse_html_scripts,
)
from fluid_sbom.pkg.cataloger.javascript.parse_package_json import (
    parse_package_json,
)
from fluid_sbom.pkg.cataloger.javascript.parse_package_lock import (
    parse_package_lock,
)
from fluid_sbom.pkg.cataloger.javascript.parse_pnpm_lock import (
    parse_pnpm_lock,
)
from fluid_sbom.pkg.cataloger.javascript.parse_yarn_lock import (
    parse_yarn_lock,
)


def on_next_javascript(
    source: reactivex.Observable[str],
) -> reactivex.Observable[Request]:
    def subscribe(
        observer: ObserverBase[Request],
        scheduler: SchedulerBase | None = None,
    ) -> reactivex.abc.DisposableBase:
        def on_next(value: str) -> None:
            try:
                if any(fnmatch(value, x) for x in ("**/package.json", "package.json")):
                    observer.on_next(
                        Request(
                            real_path=value,
                            parser=parse_package_json,
                            parser_name="javascript-parse-package-json",
                        ),
                    )
                elif any(fnmatch(value, x) for x in ("**/package-lock.json", "package-lock.json")):
                    observer.on_next(
                        Request(
                            real_path=value,
                            parser=parse_package_lock,
                            parser_name="javascript-parse-package-lock",
                        ),
                    )
                elif any(fnmatch(value, x) for x in ("**/yarn.lock", "yarn.lock")):
                    observer.on_next(
                        Request(
                            real_path=value,
                            parser=parse_yarn_lock,
                            parser_name="javascript-parse-yarn-lock",
                        ),
                    )
                elif any(fnmatch(value, x) for x in ("**/pnpm-lock.yaml", "pnpm-lock.yaml")):
                    observer.on_next(
                        Request(
                            real_path=value,
                            parser=parse_pnpm_lock,
                            parser_name="javascript-parse-pnpm-lock",
                        ),
                    )
                elif fnmatch(value, "*.html"):
                    observer.on_next(
                        Request(
                            real_path=value,
                            parser=parse_html_scripts,
                            parser_name="javascript-parse-html-scripts",
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
