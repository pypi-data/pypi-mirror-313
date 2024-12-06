from fnmatch import (
    fnmatch,
)

import reactivex
from reactivex.abc import (
    ObserverBase,
    SchedulerBase,
)

from fluid_sbom.pkg.cataloger.dotnet.parse_csproj import (
    parse_csproj,
)
from fluid_sbom.pkg.cataloger.dotnet.parse_dotnet_package_config import (
    parse_dotnet_pkgs_config,
)
from fluid_sbom.pkg.cataloger.dotnet.parse_dotnet_package_lock import (
    parse_dotnet_package_lock,
)
from fluid_sbom.pkg.cataloger.dotnet.parse_dotnet_portable_executable import (
    parse_dotnet_portable_executable,
)
from fluid_sbom.pkg.cataloger.generic.cataloger import (
    Request,
)


def on_next_dotnet(
    source: reactivex.Observable[str],
) -> reactivex.Observable[Request]:
    def subscribe(
        observer: ObserverBase[Request],
        scheduler: SchedulerBase | None = None,
    ) -> reactivex.abc.DisposableBase:
        def on_next(value: str) -> None:
            try:
                if any(
                    fnmatch(value, x)
                    for x in (
                        "**/packages.config",
                        "packages.config",
                    )
                ):
                    observer.on_next(
                        Request(
                            real_path=value,
                            parser=parse_dotnet_pkgs_config,
                            parser_name="dotnet-parse-packages-config",
                        ),
                    )
                elif any(
                    fnmatch(value, x)
                    for x in (
                        "**/packages.lock.json",
                        "packages.lock.json",
                    )
                ):
                    observer.on_next(
                        Request(
                            real_path=value,
                            parser=parse_dotnet_package_lock,
                            parser_name="dotnet-parse-package-lock",
                        ),
                    )
                elif any(
                    fnmatch(value, x)
                    for x in (
                        "**/*.csproj",
                        "*.csproj",
                    )
                ):
                    observer.on_next(
                        Request(
                            real_path=value,
                            parser=parse_csproj,
                            parser_name="dotnet-parse-csproj",
                        ),
                    )
                elif any(
                    fnmatch(value, x)
                    for x in (
                        "**/*.dll",
                        "*.dll",
                        "**/*.exe",
                        "*.exe",
                    )
                ):
                    observer.on_next(
                        Request(
                            real_path=value,
                            parser=parse_dotnet_portable_executable,
                            parser_name="dotnet-parse-portable-executable",
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
