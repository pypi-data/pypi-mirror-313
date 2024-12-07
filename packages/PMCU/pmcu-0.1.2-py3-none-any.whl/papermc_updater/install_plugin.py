from .providers import download
from .vars import HEADERS
import json


def install_plugin(name, provider, identifier):
    with open("server.json", "r") as read_file:
        server_info = json.load(read_file)
    plugin = {"name": name, "provider": provider, "id": identifier}
    if plugin in server_info["plugins"]:
        print("You may not install multiple copies of the same plugin!")
        return
    server_info["plugins"].append(plugin)
    with open("server.json", "w") as write_file:
        json.dump(server_info, write_file, indent=4)
    download(plugin, HEADERS, True)
