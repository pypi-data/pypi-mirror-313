#!/usr/bin/env python3
"""
Command line utility that validates OpenPLX files and prints the result to stdout.
"""
import os
import signal
import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, SUPPRESS
import agxOSG
import agxSDK
import agx
from openplxbundles import bundle_path
from openplx import load_from_file, OptParams, __version__, set_log_level
from openplx.versionaction import VersionAction

def parse_args():
    parser = ArgumentParser(description="View OpenPLX models", formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("openplxfile", help="the .openplx file to load")
    parser.add_argument("--bundle-path", help="list of path to bundle dependencies if any. Overrides environment variable OPENPLX_BUNDLE_PATH.",
                        metavar="<bundle_path>", default=bundle_path())
    parser.add_argument("--debug-render-frames", action='store_true', help="enable rendering of frames for mate connectors and rigid bodies.")
    parser.add_argument("--loglevel", choices=["trace", "debug", "info", "warn", "error", "critical", "off"], help="Set log level", default="warn")
    parser.add_argument("--modelname", help="The model to load (defaults to last model in file)", metavar="<name>", default=None)
    parser.add_argument("--version", help="Show version", action=VersionAction, nargs=0, default=SUPPRESS)
    return parser.parse_args()

class AllowCtrlBreakListener(agxOSG.ExampleApplicationListener): # pylint: disable=too-few-public-methods
    pass

def validate():

    args = parse_args()
    set_log_level(args.loglevel)

    _ = agx.init()
    simulation = agxSDK.Simulation()

    opt_params = OptParams()
    if args.modelname is not None:
        opt_params = opt_params.with_model_name(args.modelname)

    result = load_from_file(simulation, args.openplxfile, args.bundle_path, opt_params)

    if len(result.errors()) == 0:
        sys.exit(0)
    else:
        sys.exit(255)

def handler(_signum, _frame):
    os._exit(0)

def run():
    signal.signal(signal.SIGINT, handler)
    validate()

if __name__ == '__main__':
    run()
