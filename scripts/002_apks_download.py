# Fetcher for the YouTube APKs

import sys

import requests
from bs4 import BeautifulSoup

__UA__ = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"  # noqa

try:
    version = sys.argv[1]
except IndexError:
    print("Usage: python scripts/002_apks_download.py <version>")
    sys.exit(1)

YOUTUBE_APK_FMT = "https://www.apkmirror.com/apk/google-inc/youtube/youtube-{}-release/"
YOUTUBE_APK_PAGE = YOUTUBE_APK_FMT.format(version.replace(".", "-"))
print(f"Getting APKs for version: {YOUTUBE_APK_PAGE}")


def build_url(url: str):
    if url.startswith("//"):
        return f"https:{url}"
    elif url.startswith("/"):
        return f"https://www.apkmirror.com{url}"
    return url


# req = requests.get(YOUTUBE_APK_PAGE, headers={"User-Agent": __UA__})

with open("test.html", "r") as fp:
    res_page = BeautifulSoup(fp.read(), "html.parser")

variants_table = res_page.find("div", {"class": "variants-table"})

for table_row in variants_table.find_all("div", {"class": "table-row"}):
    first_col = table_row.find("div")
    if first_col.text.lower().strip() == "variant":
        continue

    all_columns = table_row.find_all("div", {"class": "table-cell"})
    last_two = all_columns[-2].text.lower().strip()
    if "nodpi" not in last_two:
        continue

    url_target = build_url(all_columns[-1].find("a")["href"])
    print(f"Getting download page: {url_target}")

    req = requests.get(url_target, headers={"User-Agent": __UA__})
    res_page = BeautifulSoup(req.text, "html.parser")

    tab_content = res_page.find("div", {"class": "tab-content"})
    download_internal_button = tab_content.find("a", {"class": "downloadButton"})
    download_internal_href = build_url(download_internal_button["href"])

    print(f"Getting internal download link: {download_internal_href}")
    req = requests.get(download_internal_href, headers={"User-Agent": __UA__})
    res_page = BeautifulSoup(req.text, "html.parser")

    card_with_tabs = res_page.find("div", {"class": "card-with-tabs"})
    download_actual_frfr = card_with_tabs.find("a")  # noqa
    download_href = build_url(download_actual_frfr["href"])

    print(f"Downloading: {download_href}")
    # Stream download
    with requests.get(download_href, headers={"User-Agent": __UA__}, stream=True) as r:
        r.raise_for_status()
        with open(f"youtube-{version}.apk", "wb") as fp:
            for chunk in r.iter_content(chunk_size=8192):
                fp.write(chunk)
    print("Done!")
    break
