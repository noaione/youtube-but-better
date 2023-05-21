# Not used in the base.yml
# But on auto-build.yml

import os
import sys

import requests

from rv_common import get_latest_compatible_version

REPOSITORY = "inotia00"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

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

if latest_compat_str in res["versions"]:
    print(f"Version {latest_compat_str} is in the list, skipping build")
    sys.exit(1)

print(f"Version {latest_compat_str} is not in the list, building")
with open(os.environ["GITHUB_OUTPUT"], "a") as fp:
    print(f"VERSION={latest_compat_str}", file=fp)
sys.exit(0)
