import json
from .providers import download
from .vars import HEADERS
import os


def update_plugins(init):
    print("Grabbing server info...")

    with open("server.json", "r") as read_file:
        server_info = json.load(read_file)

    plugins = server_info["plugins"]
    if not os.path.exists("./plugins/update"):
        os.makedirs("./plugins/update")
    if plugins:
        for x in plugins:
            download(x, HEADERS, init)
    else:
        print(
            "No plugins are available to be updated. Either you have no installed plugins or the plugins haven't been properly added to server.json.")
