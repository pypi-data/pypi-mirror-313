import re

from fluid_sbom.pkg.java import (
    JavaPomProperties,
)


def parse_pom_properties(path: str, file_content: str) -> JavaPomProperties | None:
    prop_map = {}

    for line in file_content.splitlines():
        line = line.strip()
        # Skip empty lines and comments
        if line == "" or line.lstrip().startswith("#"):
            continue

        # Find the first occurrence of ':' or '='
        idx = next((i for i in range(len(line)) if line[i] in ":="), -1)
        if idx == -1:
            raise ValueError(f"Unable to split pom.properties key-value pairs: {line}")

        key = line[:idx].strip()
        value = line[idx + 1 :].strip()
        prop_map[key] = value

    # Convert the dictionary to a JavaPomProperties object
    props = JavaPomProperties(path=path)
    for key, value in prop_map.items():
        key = re.sub(r"(?<!^)(?=[A-Z])", "_", key).lower()
        if hasattr(props, key):
            setattr(props, key, value)
        else:
            props.extra[  # pylint:disable=unsupported-assignment-operation
                key
            ] = value

    return props
