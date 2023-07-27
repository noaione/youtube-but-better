# Not used in the base.yml
# But on auto-build.yml

import os
import sys

import requests

from rv_common import get_latest_compatible_version, parse_as_bool

REPOSITORY = "inotia00"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
FORCE_RUN = parse_as_bool(os.getenv("FORCE_BUILD", "false"))
print(f"Force run? {FORCE_RUN!r}")

if GITHUB_TOKEN is None:
    print("GITHUB_TOKEN is not set")
    sys.exit(1)

gist_data = "https://gist.githubusercontent.com/noaione/87dcf373a2d968cd13e1837729db9018/raw/revanced-build.json"  # noqa

req = requests.get(gist_data)
req.raise_for_status()

res = req.json()

latest_compat, _ = get_latest_compatible_version(REPOSITORY, GITHUB_TOKEN)

if latest_compat is None:
    print("No compatible version found")
    sys.exit(1)

latest_compat_str = ".".join(str(x) for x in latest_compat)
# Count how many occurence this version is in the list
counted_versions = res["versions"].count(latest_compat_str)
additional_tag = f"-{counted_versions - 1}" if (counted_versions - 1) > 0 else ""

compat_tag_version = f"{latest_compat_str}{additional_tag}"

should_run = "true"
if latest_compat_str in res["versions"] and not FORCE_RUN:
    print(f"Version {latest_compat_str} is in the list, skipping build")
    should_run = "false"
else:
    print(f"Version {latest_compat_str} is not in the list, building")
with open(os.environ["GITHUB_OUTPUT"], "a") as fp:
    print(f"VERSION={latest_compat_str}", file=fp)
    print(f"VERSION_TAG={compat_tag_version}", file=fp)
    print(f"SHOULD_RUN={should_run}", file=fp)
