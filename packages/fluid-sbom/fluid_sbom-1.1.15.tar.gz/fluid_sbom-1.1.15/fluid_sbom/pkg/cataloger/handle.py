# pylint:disable=not-callable
from collections.abc import Callable

import reactivex
from reactivex import (
    Observable,
)
from reactivex import (
    operators as ops,
)
from reactivex.scheduler import (
    ThreadPoolScheduler,
)

from fluid_sbom.pkg.cataloger.cpp.cataloger import (
    on_next_cpp,
)
from fluid_sbom.pkg.cataloger.dart.cataloger import (
    on_next_dart,
)
from fluid_sbom.pkg.cataloger.dotnet.cataloger import (
    on_next_dotnet,
)
from fluid_sbom.pkg.cataloger.elixir.cataloger import (
    on_next_elixir,
)
from fluid_sbom.pkg.cataloger.generic.cataloger import (
    Request,
    on_next_db_file,
)
from fluid_sbom.pkg.cataloger.golang.cataloger import (
    on_next_golang,
)
from fluid_sbom.pkg.cataloger.java.cataloger import (
    on_next_java,
)
from fluid_sbom.pkg.cataloger.javascript.cataloger import (
    on_next_javascript,
)
from fluid_sbom.pkg.cataloger.php.cataloger import (
    on_next_php,
)
from fluid_sbom.pkg.cataloger.python.cataloger import (
    on_next_python,
)
from fluid_sbom.pkg.cataloger.redhat.cataloger import (
    on_next_redhat,
)
from fluid_sbom.pkg.cataloger.ruby.cataloger import (
    on_next_ruby,
)
from fluid_sbom.pkg.cataloger.rust.cataloger import (
    on_next_rust,
)
from fluid_sbom.pkg.cataloger.swift.cataloger import (
    on_next_swift,
)


def handle_parser(
    scheduler: ThreadPoolScheduler,
) -> Callable[[Observable[str]], Observable[Request]]:
    def _apply_parsers(source: Observable[str]) -> Observable[Request]:
        return source.pipe(
            ops.flat_map(
                lambda item: reactivex.merge(  # type: ignore
                    (on_next_python(reactivex.just(item, scheduler))),
                    (on_next_db_file(reactivex.just(item, scheduler))),
                    (on_next_java(reactivex.just(item, scheduler))),
                    (on_next_javascript(reactivex.just(item, scheduler))),
                    (on_next_redhat(reactivex.just(item, scheduler))),
                    (on_next_dotnet(reactivex.just(item, scheduler))),
                    (on_next_rust(reactivex.just(item, scheduler))),
                    (on_next_ruby(reactivex.just(item, scheduler))),
                    (on_next_elixir(reactivex.just(item, scheduler))),
                    (on_next_php(reactivex.just(item, scheduler))),
                    (on_next_swift(reactivex.just(item, scheduler))),
                    (on_next_dart(reactivex.just(item, scheduler))),
                    (on_next_cpp(reactivex.just(item, scheduler))),
                    (on_next_golang(reactivex.just(item, scheduler))),
                ),
            ),
        )

    return _apply_parsers
