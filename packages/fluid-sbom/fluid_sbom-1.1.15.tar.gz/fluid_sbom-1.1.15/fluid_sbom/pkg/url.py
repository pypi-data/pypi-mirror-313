from fluid_sbom.linux.release import (
    Release,
)

PURL_QUALIFIER_ARCH = "arch"
PURL_QUALIFIER_DISTRO = "distro"
PURL_QUALIFIER_EPOCH = "epoch"
PURL_QUALIFIER_VCS_URL = "vcs_url"
PURL_QUALIFIER_UPSTREAM = "upstream"
PURL_CARGO_PKG_TYPE = "cargo"
PURL_GRADLE_PKG_TYPE = "gradle"


def purl_qualifiers(
    qualifiers: dict[str, str | None],
    release: Release | None = None,
) -> dict[str, str]:
    # Handling distro qualifiers
    if release:
        distro_qualifiers = []
        if release.id_:
            distro_qualifiers.append(release.id_)
        if release.version_id:
            distro_qualifiers.append(release.version_id)
        elif release.build_id:
            distro_qualifiers.append(release.build_id)

        if distro_qualifiers:
            qualifiers[PURL_QUALIFIER_DISTRO] = "-".join(distro_qualifiers)

    return {
        key: qualifiers.get(key, "") or ""
        for key in sorted(qualifiers.keys())
        if qualifiers.get(key)
    }
