from typing import (
    cast,
)

from cpe import (
    CPE,
)

from fluid_sbom.model.core import (
    Advisory,
    Language,
    Package,
    PackageType,
)


def _get_target_software(cpe: str) -> list[str]:
    return cast(
        list[str],
        CPE(cpe).get_target_software(),  # type: ignore[misc]
    )


def _matches_cpe(package: Package, advisory: Advisory) -> bool:
    mapping: dict[Language, list[str]] = {
        Language.DART: ["dart"],
        Language.DOTNET: [".net", "asp.net"],
        Language.GO: ["go", "golang"],
        Language.JAVA: ["java", "*"],
        Language.JAVASCRIPT: ["javascript", "node.js", "nodejs"],
        Language.PHP: ["php"],
        Language.PYTHON: ["pypi", "python"],
        Language.RUBY: ["rails", "ruby", "ruby_on_rails"],
        Language.RUST: ["rust"],
        Language.SWIFT: ["swift"],
    }
    return package.language in mapping and any(
        target_software == "*" or target_software in mapping[package.language]
        for cpe in advisory.cpes
        for target_software in _get_target_software(cpe)
    )


def matches_namespace(package: Package, advisory: Advisory) -> bool:
    namespace_type = advisory.namespace.split(":")[1]
    if namespace_type == "language":
        return package.language.value in {
            "dotnet",
            "go",
            "java",
            "javascript",
            "php",
            "python",
            "ruby",
            "rust",
            "swift",
        }

    if namespace_type == "distro":
        return package.type in {
            PackageType.DebPkg,
            PackageType.ApkPkg,
            PackageType.RpmPkg,
        }
    if namespace_type == "cpe":
        return _matches_cpe(package, advisory)

    return False
