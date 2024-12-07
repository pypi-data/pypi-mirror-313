#!/usr/bin/env python3
"""
Command line utility that loads OpenPLX files and loads them into an AGX Simulation
"""
from openplx.openplx_application import OpenPlxApplication

def openplx_view_build_scene():
    OpenPlxApplication.prepare_scene()

def run():
    OpenPlxApplication(openplx_view_build_scene).run()

if __name__ == "__main__":
    run()
