import argparse
import json
import os


from .paper import download
from .flags import make_script
from .updatePlugins import update_plugins
from .install_plugin import install_plugin
from .vars import BASE_DIR, CURRENT_DIR


# import updatePlugins
def create():
    print("Creating the server...")
    info = download()
    print(info)
    filename = info[0]
    version = info[1]
    memory_limit = int(input("Enter the amount of memory the server should have, in GB: "))
    make_script(memory_limit, filename)
    with open(BASE_DIR + "/static/base.json", "r") as read_file:
        data = json.load(read_file)
    data["memory"] = memory_limit
    data["version"] = version
    with open("server.json", "w") as write_file:
        json.dump(data, write_file, indent=4)
    with open("eula.txt", "w") as eula_file:
        eula_file.write("eula=true")


def update():
    print("Updating server file...")
    with open("server.json", "r") as read_file:
        server_info = json.load(read_file)
    print("Current version: " + server_info["version"])
    info = download()
    filename = info[0]
    version = info[1]
    memory_limit = server_info["memory"]
    make_script(memory_limit, filename)
    server_info["version"] = version
    with open("server.json", "w") as write_file:
        json.dump(server_info, write_file, indent=4)


def plugin_update():
    print("Updating server plugins...")
    update_plugins(False)


def install():
    name = input("Enter the plugin's name: ")
    provider = input("Enter the plugin's provider: (github, modrinth, hangar, spigot, or geyser): ")
    identifier = input("Enter the plugin's id, slug, or github repo: ")
    if not os.path.exists("./plugins/update"):
        os.makedirs("./plugins/update")
    install_plugin(name, provider, identifier)


def update_full():
    update()
    plugin_update()


def initialize():
    update_plugins(True)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title="subcommands", help='help with subcommands', required=True)

parser_create = subparsers.add_parser("create",
                                      help="download a server for the first time and make a config and a startup file")
parser_create.set_defaults(func=create)

parser_update = subparsers.add_parser("update", help="update the papermc jar file and the startup script")
parser_update.set_defaults(func=update)

parser_plugin_update = subparsers.add_parser("update-plugins",
                                             help="update all currently installed plugins from their IDs in the config file")
parser_plugin_update.set_defaults(func=plugin_update)

parser_install = subparsers.add_parser("install", help="download the specified plugin and install it in the server")
parser_install.set_defaults(func=install)

parser_update_full = subparsers.add_parser("update-full",
                                           help="run update and then update-plugins in one command")
parser_update_full.set_defaults(func=update_full)

parser_update_full = subparsers.add_parser("initialize",
                                           help="initialize all plugins from the config file (to facilitate easy server transplanting)")
parser_update_full.set_defaults(func=initialize)


def main():
    print("Running in: " + CURRENT_DIR)
    args = parser.parse_args()
    args.func()
