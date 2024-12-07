"""
A module for helping out with argparse version printing
"""
from argparse import Action
import sys
from openplx import __version__

class VersionAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(__version__)
        sys.exit(0)
