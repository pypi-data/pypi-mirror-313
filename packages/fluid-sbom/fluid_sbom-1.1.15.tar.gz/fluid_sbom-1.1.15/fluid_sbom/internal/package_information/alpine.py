from fluid_sbom.internal.package_information.api_interface import (
    make_get,
)


def get_package_versions_html(
    name: str,
    distro_version: str | None = None,
    arch: str | None = None,
) -> str | None:
    # Create a mapping for arch equivalence
    arch_mapping = {
        "x86": "x86",
        "x86_64": "x86_64",
        "amd64": "x86_64",
        "i386": "x86",
        "i686": "x86",
        "arm": "arm",
        "armhf": "arm",
        "armv7": "arm",
        "arm64": "aarch64",
        "aarch64": "aarch64",
        "ppc64le": "ppc64le",
        "s390x": "s390x",
    }

    # Use the mapping to get the equivalent arch
    arch = arch_mapping.get(arch.lower(), arch) if arch else None

    if arch is None:
        return None

    # Convert distro_version format if necessary
    if distro_version:
        parts = distro_version.split(".")
        if len(parts) == 3:
            distro_version = f"v{parts[0]}.{parts[1]}"

    response = make_get(
        "https://pkgs.alpinelinux.org/packages",
        params={
            "name": name,
            "branch": distro_version or "edge",
            "repo": "",
            "arch": arch or [],
            "maintainer": "",
        },
        content=True,
    )
    return response
