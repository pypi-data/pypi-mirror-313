from typing import (
    Any,
)

import requests

from fluid_sbom.internal.cache import (
    dual_cache,
)


@dual_cache
def get_gem_package(package_name: str, version: str | None = None) -> dict[str, Any] | None:
    if version:
        url = f"https://rubygems.org/api/v2/rubygems/{package_name}/versions/{version}.json"
    else:
        url = f"https://rubygems.org/api/v1/gems/{package_name}.json"

    response = requests.get(url, timeout=30)
    if response.status_code == 200:
        package_info = response.json()
        return package_info

    return None
