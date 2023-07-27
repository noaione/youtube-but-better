# Fetcher for the Assets needed

import os
import sys
import requests

__UA__ = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"  # noqa
API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if GITHUB_TOKEN is None:
    print("GITHUB_TOKEN is not set")
    sys.exit(1)

BASE_REPOSITORY = os.getenv("BASE_REPOSITORY")

if BASE_REPOSITORY is None:
    print("BASE_REPOSITORY is not set")
    sys.exit(1)


def download_target(url: str, filename: str):
    print(f"Downloading: {url}")
    print(f"Saving to: {filename}")
    with requests.get(url, headers={"User-Agent": __UA__}, stream=True) as r:
        r.raise_for_status()
        with open(filename, "wb") as fp:
            for chunk in r.iter_content(chunk_size=8192):
                fp.write(chunk)


print(f"Getting patches for: {BASE_REPOSITORY}")
req_patches = requests.get(
    f"{API_URL}/repos/{BASE_REPOSITORY}/revanced-patches/releases",
    headers={
        "Authorization": f"Bearer {GITHUB_TOKEN}",
    }
)
res_patches = req_patches.json()
print(f"Getting integrations for: {BASE_REPOSITORY}")
req_integrations = requests.get(
    f"{API_URL}/repos/{BASE_REPOSITORY}/revanced-integrations/releases",
    headers={
        "Authorization": f"Bearer {GITHUB_TOKEN}",
    }
)
res_integrations = req_integrations.json()
print(f"Getting CLI for: {BASE_REPOSITORY}")
req_cli = requests.get(
    f"{API_URL}/repos/{BASE_REPOSITORY}/revanced-cli/releases",
    headers={
        "Authorization": f"Bearer {GITHUB_TOKEN}",
    }
)
res_cli = req_cli.json()

first_patches = res_patches[0]
first_integrations = res_integrations[0]
first_cli = res_cli[0]

patches_download = None
integrations_download = None
cli_download = None
for asset in first_patches["assets"]:
    if asset["name"].endswith(".apk") or asset["name"].endswith(".jar"):
        patches_download = asset
        break
for asset in first_integrations["assets"]:
    if asset["name"].endswith(".apk") or asset["name"].endswith(".jar"):
        integrations_download = asset
        break
for asset in first_cli["assets"]:
    if asset["name"].endswith(".apk") or asset["name"].endswith(".jar"):
        cli_download = asset
        break

print()
print(f"Patches: {patches_download['browser_download_url']}")
print(f"Integrations: {integrations_download['browser_download_url']}")
print(f"CLI: {cli_download['browser_download_url']}")

# Downloading the files
print()

print("Downloading patches...")
download_target(patches_download["browser_download_url"], "revanced-patches.jar")
print("Downloading integrations...")
download_target(
    integrations_download["browser_download_url"], "revanced-integrations.apk"
)
print("Downloading CLI...")
download_target(cli_download["browser_download_url"], "revanced-cli.jar")
print("Done!")
