import os_release
from os_release.parser import (
    OsReleaseParseException,
)
from pydantic import (
    BaseModel,
)

from fluid_sbom.file.resolver import (
    Resolver,
)


class Release(BaseModel):
    id_: str
    version_id: str
    name: str | None = None
    pretty_name: str | None = None
    version: str | None = None
    id_like: list[str] | None = None
    version_code_name: str | None = None
    build_id: str | None = None
    image_id: str | None = None
    image_version: str | None = None
    variant: str | None = None
    variant_id: str | None = None
    home_url: str | None = None
    support_url: str | None = None
    bug_report_url: str | None = None
    privacy_policy_url: str | None = None
    cpe_name: str | None = None
    support_end: str | None = None

    def __str__(self) -> str:
        if self.pretty_name:
            return self.pretty_name
        if self.name:
            return self.name
        if self.version:
            return f"{self.id_} {self.version}"
        if self.version_id != "":
            return f"{self.id_} {self.version_id}"
        return f"{self.id_} {self.build_id or ''}"


def _force_parse(content: str) -> dict[str, str] | None:
    lines: list[tuple[str, str]] = []
    for line in content.splitlines():
        line = line.rstrip("\n")
        line = line.strip()
        if not line:
            continue
        pair = line.split("=", 1)
        if len(pair) != 2:
            continue
        pair[-1] = pair[-1].strip("\"'")
        lines.append((pair[0], pair[1]))
    if not lines:
        return None

    return dict(lines)


def parse_os_release(content: str) -> Release | None:
    try:
        release = os_release.parse_str(content)
    except OsReleaseParseException:
        release = _force_parse(content)
    if release:
        if "ID_LIKE" in release:
            release["ID_LIKE"] = sorted(release["ID_LIKE"].split(" "))
        return Release(
            pretty_name=release.get("PRETTY_NAME", ""),
            name=release.get("NAME", ""),
            id_=release.get("ID", ""),
            id_like=release.get("ID_LIKE", []),
            version=release.get("VERSION", ""),
            version_id=release.get("VERSION_ID", ""),
            version_code_name=release.get("VERSION_CODENAME", ""),
            build_id=release.get("BUILD_ID", ""),
            image_id=release.get("IMAGE_ID", ""),
            image_version=release.get("IMAGE_VERSION", ""),
            variant=release.get("VARIANT", ""),
            variant_id=release.get("VARIANT_ID", ""),
            home_url=release.get("HOME_URL", ""),
            support_url=release.get("SUPPORT_URL", ""),
            bug_report_url=release.get("BUG_REPORT_URL", ""),
            privacy_policy_url=release.get("PRIVACY_POLICY_URL", ""),
            cpe_name=release.get("CPE_NAME", ""),
            support_end=release.get("SUPPORT_END", ""),
        )
    return None


def identify_release(resolver: Resolver) -> Release | None:
    possible_files = [
        "/etc/os-release",
        "/usr/lib/os-release",
        "/etc/system-release-cpe",
        "/etc/redhat-release",
        "/bin/busybox",
    ]

    for file in possible_files:
        if not resolver.has_path(file):
            continue
        location = resolver.files_by_path(file)[0]
        content_reader = resolver.file_contents_by_location(location)
        if not content_reader:
            continue
        content = content_reader.read()
        release = parse_os_release(content)
        if release:
            return release
    return None
