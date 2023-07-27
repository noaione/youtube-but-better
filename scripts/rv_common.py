from typing import Any
import requests

API_URL = "https://api.github.com"


def get_latest_compatible_version(base_repo: str, github_token: str):
    req = requests.get(
        f"{API_URL}/repos/{base_repo}/revanced-patches",
        headers={
            "Authorization": f"Bearer {github_token}",
        }
    )

    response = req.json()
    default_branch = response["default_branch"]

    patches_url = f"https://raw.githubusercontent.com/{base_repo}/revanced-patches/{default_branch}/patches.json"  # noqa
    print(f"Using the following patch URL: {patches_url}")

    req_patch = requests.get(patches_url)
    patches = req_patch.json()

    latest_compat_version = None
    actual_latest_compat = None
    for patch in patches:
        for compat in patch["compatiblePackages"]:
            if not compat["name"] == "com.google.android.youtube":
                continue
            # Some patches might not be compatible with the latest version
            versions = compat["versions"]
            if not versions:
                # No target version, assume it's compatible
                continue
            versions.sort()
            versions_splits = []
            for version in versions:
                versions_splits.append(tuple(map(int, version.split("."))))

            if latest_compat_version is None:
                latest_compat_version = versions_splits[-1]
                actual_latest_compat = versions_splits[-1]
                continue

            # If this compat version is lower than the latest compat version,
            # use it
            if versions_splits[-1] < latest_compat_version:
                latest_compat_version = versions_splits[-1]

    return latest_compat_version, actual_latest_compat


def parse_as_bool(value: Any):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in ["true", "1", "yes", "y", "t"]
    try:
        return bool(value)
    except Exception:
        return False
