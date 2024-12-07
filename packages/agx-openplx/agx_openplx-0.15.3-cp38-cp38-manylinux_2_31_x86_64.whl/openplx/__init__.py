# pylint: disable=invalid-name
"""
__init__ module for OpenPLX package
"""
import os
import sys
import traceback
# Use agx_env if available
import importlib.util
if importlib.util.find_spec("agx_env"):
    import agx_env # pylint: disable=unused-import
__AGXVERSION__ = "2.39.0.1"
__version__ = "0.15.3"

try:
    import agx
    if agx.__version__ != __AGXVERSION__:
        print(f"This version of agx-openplx is compiled for AGX {__AGXVERSION__} and may crash with your {agx.__version__} version, "+
              "update agx-openplx or AGX to make sure the versions are suited for eachother")
except Exception as e: # pylint: disable=broad-exception-caught
    traceback.print_exc()
    print("Failed finding AGX Dynamics, have you run setup_env?")
    sys.exit(255)

if "DEBUG_AGXOPENPLX" in os.environ:
    print("#### Using Debug build ####")
    try:
        # pylint: disable=relative-beyond-top-level, wildcard-import, unused-import, no-name-in-module
        from .debug.api import *
        from .debug import Core
        from .debug import Math
        from .debug import Physics
        from .debug import Simulation
        # pylint: enable=relative-beyond-top-level, wildcard-import, unused-import, no-name-in-module
    except Exception as e: # pylint: disable=broad-exception-caught
        traceback.print_exc()
        print("Failed finding OpenPLX modules or libraries, did you set PYTHONPATH correctly? "+
              "Should point to where OpenPLX directory with binaries are located.")
        print("Also, make sure you are using the same Python version the libraries were built for.")
        sys.exit(255)
else:
    try:
        # pylint: disable=relative-beyond-top-level, wildcard-import, unused-import, no-name-in-module
        from .api import *
        from . import Core
        from . import Math
        from . import Physics
        from . import Simulation
        # pylint: enable=relative-beyond-top-level, wildcard-import, unused-import, no-name-in-module
    except Exception as e: # pylint: disable=broad-exception-caught
        traceback.print_exc()
        print("Failed finding OpenPLX modules or libraries, did you set PYTHONPATH correctly? "+
              "Should point to where OpenPLX directory with binaries are located.")
        print("Also, make sure you are using the same Python version the libraries were built for.")
        sys.exit(255)
