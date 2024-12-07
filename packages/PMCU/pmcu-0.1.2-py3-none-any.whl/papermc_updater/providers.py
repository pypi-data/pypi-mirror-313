import requests
from .hash import hasher

import os


def plugin_version_exists(jarfile):
    return os.path.exists("./plugins/" + jarfile)


def download(plugin, headers, install):
    name = plugin["name"]
    provider = plugin["provider"]
    plugin_id = plugin["id"]
    if install:
        path = "./plugins/"
    else:
        path = "./plugins/update/"

    if provider == "modrinth":
        print("Downloading " + name + " from Modrinth...")
        params = {
            'loaders': '["paper"]'
        }
        versions = requests.get('https://api.modrinth.com/v2/project/' + plugin_id + "/version", params=params,
                                headers=headers, allow_redirects=True)
        versions = versions.json()
        expected_hash = versions[0]["files"][0]["hashes"]["sha512"]
        url = versions[0]["files"][0]["url"]
        filename = versions[0]["files"][0]["filename"]
        if plugin_version_exists(filename):
            print("No updates")
            return
        filename = path + filename
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)

        new_hash = hasher(filename, 512)

        if not new_hash == str(expected_hash):
            print("Bad hash, incorrect or unexpected file. Please Manually check the file.")

    elif provider == "github":
        print("Downloading " + name + " from Github...")
        response = requests.get("https://api.github.com/repos/" + plugin_id + "/releases", headers=headers,
                                allow_redirects=True)
        releases = response.json()
        release = releases[0]  # Is a dictionary
        newest_version = release["name"]
        print(newest_version)
        filename = newest_version + "-" + release["assets"][0]["name"]
        if plugin_version_exists(filename):
            print("No updates")
            return
        filename = path + filename
        download_url = release["assets"][0]["browser_download_url"]

        new_file = requests.get(download_url)
        with open(filename, 'wb') as f:
            f.write(new_file.content)
    elif provider == "spigot":
        print("Downloading " + name + " from Spigot...")
        date = requests.get("https://api.spiget.org/v2/resources/" + plugin_id, headers=headers,
                            allow_redirects=True).json()["updateDate"]
        filename = name + "-" + str(date) + ".jar"
        if plugin_version_exists(filename):
            print("No updates")
            return
        filename = path + filename
        response = requests.get("https://api.spiget.org/v2/resources/" + plugin_id + "/download", headers=headers,
                                allow_redirects=True)
        with open(filename, 'wb') as f:
            f.write(response.content)
    elif provider == "geyser":
        print("Downloading " + name + " from the GeyserMC website...")
        version = requests.get("https://download.geysermc.org/v2/projects/" + plugin_id, headers=headers, allow_redirects=True).json()["versions"][-1]
        filename = name + "-" + version + ".jar"
        if plugin_version_exists(filename):
            print("No updates")
            return
        filename = path + filename
        response = requests.get(
            "https://download.geysermc.org/v2/projects/" + plugin_id + "/versions/latest/builds/latest/downloads/spigot",
            headers=headers, allow_redirects=True)
        with open(filename, 'wb') as f:
            f.write(response.content)
    elif provider == "hangar":
        print("Downloading " + name + " from Hangar...")
        response = requests.get('https://hangar.papermc.io/api/v1/projects/' + plugin_id + "/versions", headers=headers,
                                allow_redirects=True)
        response = response.json()

        url = response["result"][0]["downloads"]["PAPER"]["downloadUrl"]
        filename = response["result"][0]["downloads"]["PAPER"]["fileInfo"]["name"]
        if plugin_version_exists(filename):
            print("No updates")
            return
        filename = path + filename
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)
