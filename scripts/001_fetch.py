# Fetcher for the YouTube target build

import os
import sys
import requests

API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if GITHUB_TOKEN is None:
    print("GITHUB_TOKEN is not set")
    sys.exit(1)

BASE_REPOSITORY = os.getenv("BASE_REPOSITORY")

if BASE_REPOSITORY is None:
    print("BASE_REPOSITORY is not set")
    sys.exit(1)


print(f"Getting default branch for: {BASE_REPOSITORY}")
req = requests.get(
    f"{API_URL}/repos/{BASE_REPOSITORY}/revanced-patches",
    headers={
        "Authorization": f"Bearer {GITHUB_TOKEN}",
    }
)

response = req.json()
default_branch = response["default_branch"]

patches_url = f"https://raw.githubusercontent.com/{BASE_REPOSITORY}/revanced-patches/{default_branch}/patches.json"  # noqa
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

if latest_compat_version is None:
    print("No compatible version found")
    sys.exit(1)

if latest_compat_version != actual_latest_compat:
    print(f"Latest compatible (all modules) version is {actual_latest_compat}, "
          f"but the latest supported version is {latest_compat_version}")
else:
    print(f"Latest compatible version is {latest_compat_version}")

# Set to github output actions
version_string = ".".join(map(str, latest_compat_version))
with open(os.environ["GITHUB_OUTPUT"], "a") as fp:
    print(f"version={version_string}", file=fp)
