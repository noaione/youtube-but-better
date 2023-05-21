# Builder script

import json
import os
import subprocess as sp
import sys
from typing import List, Optional

try:
    version = sys.argv[1]
except IndexError:
    print("Usage: python scripts/004_build.py <version>")
    sys.exit(1)


def parse_module(module_thing: Optional[str]):
    if not module_thing:
        return []

    split_thing = module_thing.split(",")
    return [x.strip() for x in split_thing]


EXCLUDED_MODULES = parse_module(os.getenv("EXCLUDED_MODULE"))
INCLUDED_MODULES = parse_module(os.getenv("INCLUDED_MODULE"))

commands = [
    "java", "-jar", "revanced-cli.jar",
    "-a", f"youtube-{version}.apk",
    "-c", "-o", "revanced.apk",
    "-m", "revanced-integrations.apk",
    "-b", "revanced-patches.jar",
]

for module in EXCLUDED_MODULES:
    commands.append("-e")
    commands.append(module)
for module in INCLUDED_MODULES:
    commands.append("-i")
    commands.append(module)

print("Running command:")
print(" ".join(commands))
print()

applied_options: List[str] = []
# Intercept subprocess output
start_intercepting = False
with sp.Popen(commands, stdout=sp.PIPE, stderr=sp.PIPE, bufsize=1, universal_newlines=True) as p:
    for line in p.stdout:
        print(line, end="")
        if line.startswith("INFO: "):
            if "decoding resource" in line.lower():
                start_intercepting = True
                continue
            if "compiling" in line.lower():
                start_intercepting = False
            if start_intercepting:
                strip_line = line.strip().replace("INFO: ", "").split(" ", 1)
                applied_options.append(strip_line[0])

print(f"Options: {applied_options!r}")

print("Done building, setting options for next step!")
with open(os.environ["GITHUB_OUTPUT"], "a") as fp:
    dumped_opts = json.dumps(applied_options, ensure_ascii=False)
    print(f"BUILD_OPTIONS={dumped_opts}", file=fp)
