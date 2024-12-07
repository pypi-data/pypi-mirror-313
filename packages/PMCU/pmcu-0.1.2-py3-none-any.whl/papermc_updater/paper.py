import requests
from .hash import hasher
from .vars import HEADERS
import os

URL_BASE = 'https://api.papermc.io'


def download():
    print("Querying version list from PaperMC...")

    versions = requests.get(URL_BASE + '/v2/projects/paper', headers=HEADERS, allow_redirects=True)

    versions = versions.json()
    ver_list = versions.get("versions")
    print("Current Version list for PaperMC:")
    print(ver_list)

    selected_version = input("Choose a version: ")

    builds = requests.get(URL_BASE + '/v2/projects/paper/versions/' + selected_version, headers=HEADERS,
                          allow_redirects=True)
    builds = builds.json()
    build_list = builds.get("builds")
    build = build_list[-1]
    print("Latest Build: " + str(build))

    build_info = requests.get(URL_BASE + "/v2/projects/paper/versions/" + selected_version + "/builds/" + str(build),
                              headers=HEADERS, allow_redirects=True)
    build_info = build_info.json()
    build_info = build_info.get("downloads")
    build_info = build_info.get("application")
    filename = build_info["name"]

    print("File to download: " + filename)

    sha256 = build_info["sha256"]

    print("Downloading...")

    response = requests.get(
        URL_BASE + "/v2/projects/paper/versions/" + selected_version + "/builds/" + str(
            build) + "/downloads/" + filename, allow_redirects=True)

    with open(filename, 'wb') as f:
        f.write(response.content)

    # Hash it to be sure nothing funky happened on the way.

    new_hash = hasher(filename, 256)
    print("Hash of the downloaded file: " + new_hash)  # Get the hexadecimal digest of the hash

    if new_hash == str(sha256):
        print("Hash OK")
    else:
        print("Bad hash, incorrect or unexpected file. Exiting.")
        exit()

    os.system("chmod a+x " + filename)

    return filename, selected_version
