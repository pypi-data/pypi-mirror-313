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
from fluid_sbom.pkg.cataloger.java.archive_parser import (
    parse_java_archive,
)
from fluid_sbom.pkg.cataloger.java.parse_android_apk import (
    parse_apk,
)
from fluid_sbom.pkg.cataloger.java.parse_build_stb import (
    build_stb,
)
from fluid_sbom.pkg.cataloger.java.parse_gradle_kts import (
    parse_gradle_lockfile_kts,
)
from fluid_sbom.pkg.cataloger.java.parse_gradle_lockfile import (
    parse_gradle_lockfile,
)
from fluid_sbom.pkg.cataloger.java.parse_pom_xml import (
    parse_pom_xml,
)


def on_next_java(  # mccabe: disable=MC0001
    source: reactivex.Observable[str],
) -> reactivex.Observable[Request]:
    def subscribe(
        observer: ObserverBase[Request],
        scheduler: SchedulerBase | None = None,
    ) -> reactivex.abc.DisposableBase:
        def on_next(value: str) -> None:
            patterns = [
                (
                    (
                        "**/pom.xml",
                        "/pom.xml",
                        "pom.xml",
                    ),
                    parse_pom_xml,
                    "java-parse-pom-xml",
                ),
                (
                    (
                        "**/*.jar",
                        "*.jar",
                        "**/*.war",
                        "*.war",
                        "**/*.ear",
                        "*.ear",
                        "**/*.par",
                        "*.par",
                        "**/*.sar",
                        "*.sar",
                        "**/*.nar",
                        "*.nar",
                        "**/*.jpi",
                        "*.jpi",
                        "**/*.hpi",
                        "*.hpi",
                        "**/*.lpkg",
                        "*.lpkg",
                    ),
                    parse_java_archive,
                    "java-archive-parse",
                ),
                (
                    (
                        "gradle.lockfile*",
                        "**/gradle.lockfile*",
                    ),
                    parse_gradle_lockfile,
                    "java-parse-gradle-lock",
                ),
                (
                    (
                        "build.gradle*",
                        "**/build.gradle",
                    ),
                    parse_gradle_lockfile_kts,
                    "java-parse-gradle-lock",
                ),
                (
                    (
                        "**/*.apk",
                        "*.apk",
                    ),
                    parse_apk,
                    "java-parse-apk",
                ),
                (
                    (
                        "**/build.sbt",
                        "build.sbt",
                    ),
                    build_stb,
                    "java-parse-build-stb",
                ),
            ]
            try:
                for pattern, parser, parser_name in patterns:
                    if any(fnmatch(value, x) for x in pattern):
                        observer.on_next(
                            Request(
                                real_path=value,
                                parser=parser,
                                parser_name=parser_name,
                            ),
                        )
                        break

            except Exception as ex:  # noqa: BLE001
                observer.on_error(ex)

        return source.subscribe(
            on_next,
            observer.on_error,
            observer.on_completed,
            scheduler=scheduler,
        )

    return reactivex.create(subscribe)
