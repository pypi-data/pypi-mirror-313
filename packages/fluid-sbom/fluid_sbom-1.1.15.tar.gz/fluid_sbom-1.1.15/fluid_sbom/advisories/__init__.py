from __future__ import (
    annotations,
)

import functools
import json
import logging
from concurrent.futures import (
    ThreadPoolExecutor,
)
from multiprocessing import (
    cpu_count,
)
from typing import (
    cast,
)

from packageurl import (
    PackageURL,
)

from fluid_sbom.advisories.database import (
    DATABASE,
)
from fluid_sbom.advisories.namespace import (
    matches_namespace,
)
from fluid_sbom.advisories.version import (
    matches_version,
)
from fluid_sbom.model.core import (
    Advisory,
    Language,
    Package,
)

LOGGER = logging.getLogger(__name__)


VALID_NAMESPACES = [
    "alpine:distro:alpine:3.10",
    "alpine:distro:alpine:3.11",
    "alpine:distro:alpine:3.12",
    "alpine:distro:alpine:3.13",
    "alpine:distro:alpine:3.14",
    "alpine:distro:alpine:3.15",
    "alpine:distro:alpine:3.16",
    "alpine:distro:alpine:3.17",
    "alpine:distro:alpine:3.18",
    "alpine:distro:alpine:3.19",
    "alpine:distro:alpine:3.2",
    "alpine:distro:alpine:3.20",
    "alpine:distro:alpine:3.3",
    "alpine:distro:alpine:3.4",
    "alpine:distro:alpine:3.5",
    "alpine:distro:alpine:3.6",
    "alpine:distro:alpine:3.7",
    "alpine:distro:alpine:3.8",
    "alpine:distro:alpine:3.9",
    "alpine:distro:alpine:edge",
    "amazon:distro:amazonlinux:2",
    "amazon:distro:amazonlinux:2022",
    "amazon:distro:amazonlinux:2023",
    "chainguard:distro:chainguard:rolling",
    "debian:distro:debian:11",
    "debian:distro:debian:12",
    "debian:distro:debian:13",
    "debian:distro:debian:unstable",
    "github:language:dart",
    "github:language:dotnet",
    "github:language:go",
    "github:language:java",
    "github:language:javascript",
    "github:language:php",
    "github:language:python",
    "github:language:ruby",
    "github:language:rust",
    "github:language:swift",
    "mariner:distro:mariner:1.0",
    "mariner:distro:mariner:2.0",
    "nvd:cpe",
    "oracle:distro:oraclelinux:5",
    "oracle:distro:oraclelinux:6",
    "oracle:distro:oraclelinux:7",
    "oracle:distro:oraclelinux:8",
    "oracle:distro:oraclelinux:9",
    "redhat:distro:redhat:5",
    "redhat:distro:redhat:6",
    "redhat:distro:redhat:7",
    "redhat:distro:redhat:8",
    "redhat:distro:redhat:9",
    "sles:distro:sles:11",
    "sles:distro:sles:11.1",
    "sles:distro:sles:11.2",
    "sles:distro:sles:11.3",
    "sles:distro:sles:11.4",
    "sles:distro:sles:12",
    "sles:distro:sles:12.1",
    "sles:distro:sles:12.2",
    "sles:distro:sles:12.3",
    "sles:distro:sles:12.4",
    "sles:distro:sles:12.5",
    "sles:distro:sles:15",
    "sles:distro:sles:15.1",
    "sles:distro:sles:15.2",
    "sles:distro:sles:15.3",
    "sles:distro:sles:15.4",
    "sles:distro:sles:15.5",
    "sles:distro:sles:15.6",
    "ubuntu:distro:ubuntu:12.04",
    "ubuntu:distro:ubuntu:12.10",
    "ubuntu:distro:ubuntu:13.04",
    "ubuntu:distro:ubuntu:14.04",
    "ubuntu:distro:ubuntu:14.10",
    "ubuntu:distro:ubuntu:15.04",
    "ubuntu:distro:ubuntu:15.10",
    "ubuntu:distro:ubuntu:16.04",
    "ubuntu:distro:ubuntu:16.10",
    "ubuntu:distro:ubuntu:17.04",
    "ubuntu:distro:ubuntu:17.10",
    "ubuntu:distro:ubuntu:18.04",
    "ubuntu:distro:ubuntu:18.10",
    "ubuntu:distro:ubuntu:19.04",
    "ubuntu:distro:ubuntu:19.10",
    "ubuntu:distro:ubuntu:20.04",
    "ubuntu:distro:ubuntu:20.10",
    "ubuntu:distro:ubuntu:21.04",
    "ubuntu:distro:ubuntu:21.10",
    "ubuntu:distro:ubuntu:22.04",
    "ubuntu:distro:ubuntu:22.10",
    "ubuntu:distro:ubuntu:23.04",
    "ubuntu:distro:ubuntu:23.10",
    "ubuntu:distro:ubuntu:24.04",
    "wolfi:distro:wolfi:rolling",
]


AdvisoryRow = tuple[str, str, str, str, str, float | None, float | None, str, str]


def _format_advisory(row: AdvisoryRow) -> Advisory:
    return Advisory(
        cpes=cast(list[str], json.loads(row[0] or "[]")),
        description=row[4] or None,
        epss=row[5] or 0.0,
        id=row[1],
        namespace=row[2],
        percentile=row[6] or 0.0,
        severity=row[7],
        urls=[url for url in cast(list[str], json.loads(row[8] or "[]")) if url],
        version_constraint=row[3] or None,
    )


def get_namespace_sufix(
    package: Package,
    *,
    distro_id: str | None = None,
    distro_version: str | None = None,
) -> list[str] | None:
    distro_result = []
    if (not distro_id or not distro_version) and (
        package.p_url
        and (
            pacakge_url := PackageURL.from_string(  # type: ignore[misc]
                package.p_url,
            )
        )
        and isinstance(pacakge_url.qualifiers, dict)  # type: ignore[misc]
    ):
        qualifiers = pacakge_url.qualifiers  # type: ignore[misc]
        distro_id = qualifiers.get("distro_id")
        distro_version = qualifiers.get("distro_version_id")

    if distro_id and distro_version:
        distro_version = ".".join(distro_version.split(".")[0:2])
        namespace = f"{distro_id}:distro:{distro_id}:{distro_version}"
        if namespace in VALID_NAMESPACES:
            distro_result.append(namespace)
        elif distro_id == "alpine":
            # If the distro version does not have the x.y.z format, edge should
            distro_result.append("alpine:distro:alpine:edge")
        distro_result.append("nvd:cpe")
    if distro_result:
        return distro_result

    if package.language != Language.UNKNOWN_LANGUAGE:
        return [
            "nvd:cpe",
            f"github:language:{package.language.value}",
        ]

    return None


def remove_duplicates(advisories: list[Advisory]) -> list[Advisory]:
    advisory_dict: dict[str, Advisory] = {}

    for advisory in advisories:
        if advisory.id in advisory_dict:
            if advisory.get_info_count() > advisory_dict[advisory.id].get_info_count():
                advisory_dict[advisory.id] = advisory
        else:
            advisory_dict[advisory.id] = advisory

    return list(advisory_dict.values())


def _handle_raw_advisory(package: Package, raw_advisory: AdvisoryRow) -> Advisory | None:
    advisory = _format_advisory(raw_advisory)
    if matches_namespace(package, advisory) and matches_version(package, advisory):
        return advisory
    return None


def _get_matching_advisories(
    package: Package,
    *,
    distro_id: str | None = None,
    distro_version: str | None = None,
) -> list[Advisory]:
    connection = DATABASE.get_connection()
    if connection is None:
        return []
    advisories_raw = []
    cursor = connection.cursor()
    if namespace_sufix := get_namespace_sufix(
        package,
        distro_id=distro_id,
        distro_version=distro_version,
    ):
        for namespace in namespace_sufix:
            if namespace not in VALID_NAMESPACES:
                LOGGER.warning(
                    "Invalid namespace",
                    extra={"extra": {"namespace": namespace}},
                )
                continue
            cursor.execute(
                """
                SELECT
                    vuln.cpes,
                    vuln.id,
                    vuln.namespace,
                    vuln.version_constraint,
                    vuln_meta.description,
                    vuln_meta.epss,
                    vuln_meta.percentile,
                    vuln_meta.severity,
                    vuln_meta.urls
                FROM
                    vulnerability vuln
                INNER JOIN vulnerability_metadata vuln_meta
                    ON vuln.id = vuln_meta.id
                    AND vuln.namespace = vuln_meta.namespace
                WHERE vuln.package_name = ?
                AND vuln.namespace = ?
                """,
                (package.name.lower(), namespace),
            )
            advisories_raw.extend(cast(list[AdvisoryRow], cursor.fetchall()))
    else:
        cursor.execute(
            """
            SELECT
                vuln.cpes,
                vuln.id,
                vuln.namespace,
                vuln.version_constraint,
                vuln_meta.description,
                vuln_meta.epss,
                vuln_meta.percentile,
                vuln_meta.severity,
                vuln_meta.urls
            FROM
                vulnerability vuln
            INNER JOIN vulnerability_metadata vuln_meta
                ON vuln.id = vuln_meta.id
                AND vuln.namespace = vuln_meta.namespace
            WHERE vuln.package_name = ?
            """,
            (package.name.lower(),),
        )
        advisories_raw.extend(cast(list[AdvisoryRow], cursor.fetchall()))
    with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
        result = list(
            filter(
                None,
                executor.map(
                    functools.partial(_handle_raw_advisory, package),
                    advisories_raw,
                ),
            ),
        )
    return remove_duplicates(result)


def get_package_advisories(
    package: Package,
    *,
    distro_id: str | None = None,
    distro_version: str | None = None,
) -> list[Advisory]:
    try:
        return _get_matching_advisories(package, distro_id=distro_id, distro_version=distro_version)
    except Exception:  # pylint:disable=broad-exception-caught
        LOGGER.exception(
            "Unable to get advisories for package %s",
            package.name,
        )
        return []


def extract_related_vulnerability(vuln_data: str) -> str | None:
    """Extract the first related vulnerability from the JSON string."""
    try:
        related_vulns = json.loads(vuln_data)  # type: ignore[misc]
        if (
            isinstance(related_vulns, list)  # type: ignore[misc]
            and related_vulns
        ):
            first_vuln = related_vulns[0]
            if isinstance(first_vuln, dict):
                return str(list(first_vuln.values())[0])  # type: ignore[misc]
    except json.JSONDecodeError:
        return None
    return None


def get_related_vulns(package_name: str, adv_id: str) -> str | None:
    """Get the related vulnerabilities for a given package using its name."""
    connection = DATABASE.get_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT
            vuln.related_vulnerabilities
        FROM
            vulnerability vuln
        WHERE vuln.package_name = ?
        AND vuln.id = ?
        """,
        (package_name.lower(), adv_id),
    )
    query_result = cast(list[tuple[str]], cursor.fetchall())
    for row in query_result:
        dict_str = row[0]
        if isinstance(dict_str, str):
            return extract_related_vulnerability(dict_str)

    return None
