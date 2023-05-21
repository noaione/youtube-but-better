# Builder script

import os
import sys
from typing import Optional
import subprocess as sp


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
sp.run(commands)
