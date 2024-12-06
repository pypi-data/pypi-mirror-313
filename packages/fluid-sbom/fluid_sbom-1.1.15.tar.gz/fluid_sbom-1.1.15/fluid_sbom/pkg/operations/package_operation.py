import logging
import multiprocessing
from collections.abc import Callable
from typing import (
    cast,
)

import reactivex
import reactivex.operators
from reactivex import (
    Observable,
)
from reactivex.abc import (
    ObserverBase,
    SchedulerBase,
)
from reactivex.scheduler import (
    ThreadPoolScheduler,
)

from fluid_sbom.artifact.relationship import (
    Relationship,
    RelationshipType,
)
from fluid_sbom.file.resolver import (
    Resolver,
)
from fluid_sbom.linux.release import (
    identify_release,
)
from fluid_sbom.model.core import (
    Package,
)
from fluid_sbom.pkg.cataloger.generic.cataloger import (
    Request,
    Task,
    execute_parsers,
)
from fluid_sbom.pkg.cataloger.generic.parser import (
    Environment,
)
from fluid_sbom.pkg.cataloger.handle import (
    handle_parser,
)
from fluid_sbom.pkg.python import (
    PythonPackage,
)
from fluid_sbom.utils.exceptions import (
    UnexpectedExceptionError,
)

LOGGER = logging.getLogger(__name__)


def strip_version_specifier(item: str) -> str:
    # Define the characters that indicate the start of a version specifier
    specifiers = "[(<>="

    # Find the index of the first occurrence of any specifier character
    index = next((i for i, char in enumerate(item) if char in specifiers), None)

    # If no specifier character is found, return the original string
    if index is None:
        return item.strip()

    # Return the substring up to the first specifier character, stripped of
    # leading/trailing whitespace
    return item[:index].strip()


def handle_relationships(packages: list[Package]) -> list[Relationship]:
    relationships: list[Relationship] = []
    for package in packages:
        match package.found_by:
            case "python-installed-package-cataloger":
                python_package: PythonPackage = cast(PythonPackage, package.metadata)
                for dep in python_package.dependencies if python_package.dependencies else []:
                    dep_name = strip_version_specifier(dep)
                    if dep_package := next((x for x in packages if x.name == dep_name), None):
                        relationships.append(
                            Relationship(
                                from_=dep_package,
                                to_=package,
                                type=(RelationshipType.DEPENDENCY_OF_RELATIONSHIP),
                                data=None,
                            ),
                        )
    return relationships


def gen_location(
    resolver: Resolver,
) -> Callable[[Observable[Request]], Observable]:
    def _handle(source: Observable[Request]) -> Observable:
        def subscribe(
            observer: ObserverBase[Task],
            scheduler: SchedulerBase | None = None,
        ) -> reactivex.abc.DisposableBase:
            def on_next(value: Request) -> None:
                try:
                    locations = resolver.files_by_path(value.real_path)
                    for location in locations:
                        observer.on_next(
                            Task(
                                location=location,
                                parser=value.parser,
                                parser_name=value.parser_name,
                            ),
                        )
                except (
                    Exception  # noqa: BLE001
                ) as ex:
                    observer.on_error(ex)

            return source.subscribe(
                on_next,
                observer.on_error,
                observer.on_completed,
                scheduler=scheduler,
            )

        return reactivex.create(subscribe)

    return _handle


def package_operations_factory(
    resolver: Resolver,
) -> tuple[list[Package], list[Relationship]]:
    observer = reactivex.from_iterable(resolver.walk_file())
    result_packages: list[Package] = []
    result_relations: list[Relationship] = []
    completed_event = multiprocessing.Event()
    errors = []

    def on_completed() -> None:
        completed_event.set()

    def on_error(error: Exception) -> None:
        errors.append(error)
        on_completed()

    def on_next(value: tuple[list[Package], list[Relationship]]) -> None:
        packages, relations = value
        result_packages.extend(packages)
        result_relations.extend(relations)

    optimal_thread_count = multiprocessing.cpu_count()
    pool_scheduler = ThreadPoolScheduler(optimal_thread_count)

    observer.pipe(
        handle_parser(scheduler=pool_scheduler),
        gen_location(resolver),
        execute_parsers(resolver, Environment(linux_release=identify_release(resolver))),
    ).subscribe(
        on_next,
        on_error=on_error,
        on_completed=on_completed,
        scheduler=pool_scheduler,
    )
    completed_event.wait()
    result_relations.extend(handle_relationships(result_packages))

    if errors:
        for error in errors:
            raise UnexpectedExceptionError(error) from error

    return result_packages, result_relations
