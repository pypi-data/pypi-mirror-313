from typing import (
    Any,
)

import requests

from fluid_sbom.internal.cache import (
    dual_cache,
)


@dual_cache
def get_nuget_package(package_name: str, version: str | None = None) -> dict[str, Any] | None:
    package_name = package_name.lower()
    base_url = f"https://api.nuget.org/v3/registration5-gz-semver2/{package_name}"
    if version:
        base_url += f"/{version}"
    else:
        base_url += "/index"
    base_url += ".json"
    response = requests.get(base_url, timeout=30)
    if response.status_code == 200:
        package_data = response.json()
        if version:
            package_data = requests.get(package_data["catalogEntry"], timeout=30).json()
        else:
            items = requests.get(package_data["items"][-1]["@id"], timeout=30).json()["items"]
            try:
                package_data = next(
                    x["catalogEntry"] for x in reversed(items) if "catalogEntry" in x
                )
            except StopIteration:
                package_data = next(
                    (
                        y["catalogEntry"]
                        for x in reversed(items)
                        for y in reversed(x.get("items", []))
                        if "catalogEntry" in y
                        # not list preview versions
                        and "pre" not in y["catalogEntry"]["version"]
                    ),
                    None,
                )

        return package_data

    return None
