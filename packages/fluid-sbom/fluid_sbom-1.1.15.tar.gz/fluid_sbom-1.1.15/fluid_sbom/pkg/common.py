from fluid_sbom.pkg.algorithm import (
    algorithm_length,
)


def infer_algorithm(digest_value: str | None) -> str | None:
    if digest_value:
        for algorithm, length in algorithm_length.items():
            if len(digest_value) == int(length):
                return algorithm.value
    return None
