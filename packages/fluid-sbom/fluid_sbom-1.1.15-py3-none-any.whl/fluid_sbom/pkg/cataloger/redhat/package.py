from packageurl import (
    PackageURL,
)

from fluid_sbom.linux.release import (
    Release,
)


def package_url(
    *,
    name: str,
    arch: str | None,
    epoch: int | None,
    source_rpm: str,
    version: str,
    release: str,
    distro: Release | None,
) -> str:
    namespace = ""
    if distro:
        namespace = distro.id_
    qualifiers: dict[str, str] = {}
    if arch:
        qualifiers["arch"] = arch
    if epoch:
        qualifiers["epoch"] = str(epoch)
    if source_rpm:
        qualifiers["upstream"] = source_rpm

    return PackageURL(
        type="rpm",
        namespace=namespace,
        name=name,
        version=f"{version}-{release}",
        qualifiers=qualifiers,
        subpath="",
    ).to_string()
