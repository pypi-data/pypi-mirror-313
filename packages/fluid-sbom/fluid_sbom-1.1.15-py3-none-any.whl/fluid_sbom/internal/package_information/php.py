from typing import (
    Any,
)

import requests

from fluid_sbom.internal.cache import (
    dual_cache,
)


@dual_cache
def get_composer_package(package_name: str, version: str | None = None) -> dict[str, Any] | None:
    base_url = f"https://repo.packagist.org/p2/{package_name}.json"
    response = requests.get(base_url, timeout=30)
    if response.status_code == 200:
        response_data = response.json()

        package_versions = response_data.get("packages", {}).get(package_name, [])

        if version:
            for version_data in package_versions:
                if version_data.get("version") == version:
                    return version_data
            return None

        if package_versions:
            latest_version_data = package_versions[0]
            return latest_version_data

        return None

    return None
