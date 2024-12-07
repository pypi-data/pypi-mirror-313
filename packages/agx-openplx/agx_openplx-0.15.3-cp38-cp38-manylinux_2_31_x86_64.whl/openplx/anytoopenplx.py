#!/usr/bin/env python3
"""
Command line utility that helps converting supported formats to OpenPLX files.
"""
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, SUPPRESS
from pathlib import Path
import agx
from openplx import register_plugins, parseWithPlugin, __version__, set_log_level
from openplx.Core import OpenPlxContext, getRegisteredPlugins, StringVector
from openplx.versionaction import VersionAction


def parse_args():
    parser = ArgumentParser(description="Convert any (supported) file to .openplx", formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("inputfile", metavar="<non-openplx-file>", help="the non-openplx file to convert")
    # Next to will be added in the future, at which time agxtoopenplx will be obsolete
    # parser.add_argument("--root-system-name", metavar="<root system name>", help="Override the name of the root system model")
    # parser.add_argument("--export-folder", metavar="<export folder>", help="Where to write exported trimesh:es", default="./")
    parser.add_argument("--loglevel", choices=["trace", "debug", "info", "warn", "error", "critical", "off"], help="Set log level", default="info")
    parser.add_argument("--version", help="Show version", action=VersionAction, nargs=0, default=SUPPRESS)
    parser.add_argument("--realprecision", help="Set precision of generated real values", type=int, default=6)
    return parser.parse_known_args()

def run():
    init = agx.AutoInit()  # pylint: disable=W0612 # Unused variable 'init'
    args, _ = parse_args()
    set_log_level(args.loglevel)
    context = OpenPlxContext(StringVector())
    register_plugins(context, None)
    plugins = getRegisteredPlugins(context)

    extension_plugin_map = {ext: plugin for plugin in plugins for ext in plugin.extensions()}
    extension = Path(args.inputfile).suffix
    if extension not in extension_plugin_map:
        print(f"No matching plugin found for {args.inputfile}, does not end in one of {list(extension_plugin_map.keys())}")
        return
    matching_plugin = extension_plugin_map[extension]
    matching_plugin.setPrecision(args.realprecision)
    openplx_string = parseWithPlugin(matching_plugin, args.inputfile)

    print(openplx_string)

if __name__ == '__main__':
    run()
