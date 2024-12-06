from enum import (
    StrEnum,
)


class Platform(StrEnum):
    CARGO = "CARGO"
    COMPOSER = "COMPOSER"
    CONAN = "CONAN"
    ERLANG = "ERLANG"
    GEM = "GEM"
    GITHUB_ACTIONS = "GITHUB_ACTIONS"
    GO = "GO"
    MAVEN = "MAVEN"
    NPM = "NPM"
    NUGET = "NUGET"
    PIP = "PIP"
    PUB = "PUB"
    SWIFT = "SWIFT"
    CABAL = "CABAL"
    CRAN = "CRAN"


class Language(StrEnum):
    UNKNOWN_LANGUAGE: str = "unknown_language"
    CPP: str = "c++"
    DART: str = "dart"
    DOTNET: str = "dotnet"
    ELIXIR: str = "elixir"
    ERLANG: str = "erlang"
    GO: str = "go"
    HASKELL: str = "haskell"
    JAVA: str = "java"
    JAVASCRIPT: str = "javascript"
    PHP: str = "php"
    PYTHON: str = "python"
    R: str = "R"
    RUBY: str = "ruby"
    RUST: str = "rust"
    SWIFT: str = "swift"

    def get_platform_value(self) -> str | None:
        language_to_platform = {
            Language.CPP: Platform.CONAN.value,
            Language.DART: Platform.PUB.value,
            Language.DOTNET: Platform.NUGET.value,
            Language.ELIXIR: Platform.GEM.value,
            Language.ERLANG: Platform.ERLANG.value,
            Language.GO: Platform.GO.value,
            Language.HASKELL: Platform.CABAL.value,
            Language.JAVA: Platform.MAVEN.value,
            Language.JAVASCRIPT: Platform.NPM.value,
            Language.PHP: Platform.COMPOSER.value,
            Language.PYTHON: Platform.PIP.value,
            Language.R: Platform.CRAN.value,
            Language.RUBY: Platform.GEM.value,
            Language.RUST: Platform.CARGO.value,
            Language.SWIFT: Platform.SWIFT.value,
            Language.UNKNOWN_LANGUAGE: None,
        }
        return language_to_platform.get(self)
