# Not used in the base.yml
# But on auto-build.yml

import os
import sys
import json
import hashlib
from pathlib import Path

import requests


CWD = Path.cwd()
REPOSITORY = "inotia00"
GITHUB_TOKEN = os.getenv("GITHUB_GIST_TOKEN")
VERSION_BUILD = os.getenv("VERSION_BUILD")
OPTIONS_NON_ROOT = os.getenv("OPTIONS_NON_ROOT")
OPTIONS_ROOT = os.getenv("OPTIONS_ROOT")
FILENAME_NON_ROOT = os.getenv("FILENAME_NON_ROOT")
FILENAME_ROOT = os.getenv("FILENAME_ROOT")

if GITHUB_TOKEN is None:
    print("GITHUB_TOKEN is not set")
    sys.exit(1)
if VERSION_BUILD is None:
    print("VERSION_BUILD is not set")
    sys.exit(1)
if OPTIONS_NON_ROOT is None:
    print("OPTIONS_NON_ROOT is not set")
    sys.exit(1)
if OPTIONS_ROOT is None:
    print("OPTIONS_ROOT is not set")
    sys.exit(1)
if FILENAME_NON_ROOT is None:
    print("FILENAME_NON_ROOT is not set")
    sys.exit(1)
if FILENAME_ROOT is None:
    print("FILENAME_ROOT is not set")
    sys.exit(1)

gist_data = "https://gist.githubusercontent.com/noaione/87dcf373a2d968cd13e1837729db9018/raw/revanced-build.json"  # noqa
gist_id = "87dcf373a2d968cd13e1837729db9018"

req = requests.get(gist_data)
req.raise_for_status()

res_json = req.json()

# Append the new version
res_json["versions"].append(VERSION_BUILD)

# Make patch request
req_patch = requests.patch(
    f"https://api.github.com/gists/{gist_id}",
    headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    },
    data=json.dumps({
        "description": "ReVanced Auto Build — Version Build List",
        "files": {
            "revanced-build.json": {
                "content": json.dumps(res_json, indent=4)
            }
        }
    })
)
req_patch.raise_for_status()


BASE_MARKDOWN = f"""This is an automated build for ReVanced, this build is not official and not supported by the ReVanced Team.
This build is based on [inotia00](https://github.com/inotia00/) version.

Based on: **YouTube v{VERSION_BUILD}**

---

## Checksums

| Name | Checksum |
|------|:--------:|
"""  # noqa

# Check if filename location is kinda fucked?
for filename in (FILENAME_NON_ROOT, FILENAME_ROOT):
    path_test = CWD / filename
    if not path_test.is_file():
        path_act = path_test / filename
        if not path_act.is_file():
            print(f"Unable to actually found the file??? ({path_act})")
            sys.exit(1)
        print(f"Rewiring {path_act} to {path_test}")
        path_fin = CWD / f"{filename}.temp"
        path_act.rename(path_fin)
        path_test.rmdir()
        path_fin.rename(CWD / filename)

# sha256 sum the files
checksums = []
for filename in (FILENAME_NON_ROOT, FILENAME_ROOT):
    with open(filename, "rb") as fp:  # weird way, I know
        checksums.append((filename, hashlib.sha256(fp.read()).hexdigest()))

# Append to markdown
for filename, checksum in checksums:
    BASE_MARKDOWN += f"| {filename} | `{checksum}` |\n"

BASE_MARKDOWN += "\n"
option_root = json.loads(OPTIONS_ROOT)
option_non_root = json.loads(OPTIONS_NON_ROOT)

# Append options
BASE_MARKDOWN += "## Options\n\n"
BASE_MARKDOWN += "### Root\n\n"
for option in option_root:
    BASE_MARKDOWN += f"- `{option}`\n"
BASE_MARKDOWN += "\n"
BASE_MARKDOWN += "### Non-Root\n\n"
for option in option_non_root:
    BASE_MARKDOWN += f"- `{option}`\n"

# Write file
print(BASE_MARKDOWN)
with open("GENERATED_RELEASE_NOTES.md", "w") as fp:
    fp.write(BASE_MARKDOWN)
