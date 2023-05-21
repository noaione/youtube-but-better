# Fetcher for the YouTube target build

import os
import sys

from rv_common import get_latest_compatible_version

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if GITHUB_TOKEN is None:
    print("GITHUB_TOKEN is not set")
    sys.exit(1)

BASE_REPOSITORY = os.getenv("BASE_REPOSITORY")

if BASE_REPOSITORY is None:
    print("BASE_REPOSITORY is not set")
    sys.exit(1)


print(f"Getting default branch for: {BASE_REPOSITORY}")
latest_compat_version, actual_latest_compat = get_latest_compatible_version(
    BASE_REPOSITORY, GITHUB_TOKEN
)

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
