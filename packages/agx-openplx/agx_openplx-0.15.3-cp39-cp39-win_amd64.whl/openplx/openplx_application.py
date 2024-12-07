"""
Base class for OpenPLX applications
"""
import os
import sys
import signal

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, Action, SUPPRESS
import agxOSG
from openplxbundles import bundle_path

# Import useful utilities to access the current simulation, graphics root and application
from agxPythonModules.utils.environment import init_app, simulation, application, root

from openplx import InputSignalQueue, OutputSignalQueue, InputSignalListener, OutputSignalListener, OsgClickAdapter
from openplx import load_from_file, OptParams, addVisuals, addDeformableVisualUpdaters, __version__, set_log_level, add_file_changed_listener
from openplx.versionaction import VersionAction

def dummy_build_scene():
    pass

class AgxHelpAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        sys.argv.append("--usage")
        OpenPlxApplication(dummy_build_scene).start_agx()
        sys.exit(0)

class AllowCtrlBreakListener(agxOSG.ExampleApplicationListener): # pylint: disable=too-few-public-methods
    pass

class OpenPlxApplication:

    def __init__(self, build_scene, build_scene_file=None):
        """
        AGX needs to know the build scene function and which file
        If build_scene_file is None then it is inferred from the build_scene function.
        """
        self.build_scene = build_scene
        self.build_scene_file = sys.modules[self.build_scene.__module__].__file__ if build_scene_file is None else build_scene_file

    @staticmethod
    def setup_args_parser(openplxfile = None):
        parser = ArgumentParser(description="View OpenPLX models", formatter_class=ArgumentDefaultsHelpFormatter)
        if openplxfile is None:
            parser.add_argument("openplxfile", help="the .openplx file to load")
        parser.add_argument("[AGX flags ...]", help="any additional AGX flags", default="", nargs="?")
        parser.add_argument(
            "--bundle-path",
            help="list of path to bundle dependencies if any. Overrides environment variable OPENPLX_BUNDLE_PATH.",
            metavar="<bundle_path>",
            default=bundle_path(),
        )
        parser.add_argument("--click-addr", type=str, help="Address for Click to listen on, e.g. ipc:///tmp/click.ipc", default="tcp://*:5555")
        parser.add_argument("--debug-render-frames", action="store_true", help="enable rendering of frames for mate connectors and rigid bodies.")
        parser.add_argument("--enable-click", help="Enable sending and receiving signals as Click Messages", action="store_true", default=SUPPRESS)
        parser.add_argument("--loglevel",
                            choices=["trace", "debug", "info", "warn", "error", "critical", "off"],
                            help="Set log level",
                            default="info")
        parser.add_argument("--modelname", help="The model to load (defaults to last model in file)", metavar="<name>", default=None)
        parser.add_argument("--reload-on-update", help="Reload scene automatically when source is updated", action="store_true", default=SUPPRESS)
        parser.add_argument("--agxhelp", help="Show AGX specific help", action=AgxHelpAction, nargs=0, default=SUPPRESS)
        parser.add_argument("--version", help="Show version", action=VersionAction, nargs=0, default=SUPPRESS)
        return parser

    @staticmethod
    def prepare_scene(openplxfile = None):
        args, extra_args = OpenPlxApplication.setup_args_parser(openplxfile).parse_known_args()
        set_log_level(args.loglevel)
        if extra_args:
            print(f"Passing these args to AGX: {(' ').join(extra_args)}")

        opt_params = OptParams()
        if args.modelname is not None:
            opt_params = opt_params.with_model_name(args.modelname)

        result = load_from_file(simulation(), args.openplxfile if openplxfile is None else openplxfile, args.bundle_path, opt_params)

        assembly = result.assembly()
        openplx_scene = result.scene()

        # Add signal listeners so that signals are picked up from inputs
        input_queue = InputSignalQueue.create()
        output_queue = OutputSignalQueue.create()
        input_signal_listener = InputSignalListener(assembly, input_queue)
        output_signal_listener = OutputSignalListener(assembly, openplx_scene, output_queue)

        simulation().add(input_signal_listener, InputSignalListener.RECOMMENDED_PRIO)
        simulation().add(output_signal_listener, OutputSignalListener.RECOMMENDED_PRIO)

        # Add click listeners unless this is scene-reload, in that case we want to keep our listeners
        # Note that we use globals() since this whole file is reloaded on scene-reload by AGX, so no local globals are kept
        if "click_adapter" not in globals():
            globals()["click_adapter"] = OsgClickAdapter()
            application().addListener(AllowCtrlBreakListener())

            if "reload_on_update" in args:
                print(f"Will reload scene when {args.openplxfile} is updated")
                add_file_changed_listener(application(), args.openplxfile)

        if "enable_click" in args:
            click_adapter = globals()["click_adapter"]
            click_adapter.add_listeners(application(), simulation(), args.click_addr, openplx_scene,
                                        input_queue, output_queue, output_signal_listener)

        if not addVisuals(result, root(), args.debug_render_frames):
            application().setEnableDebugRenderer(True)
        simulation().add(assembly.get())
        addDeformableVisualUpdaters(result, root())
        return openplx_scene, input_queue, output_queue

    @staticmethod
    def ctrl_break_handler(_signum, _frame):
        # Unfortunately os._exit(0) doesn't cut it on Windows, so we're doing the kill to make sure we exit on Windows as well.
        if os.name == "nt":
            os.kill(os.getpid(), 9)
        else:
            application().stop()

    @staticmethod
    def on_shutdown(_):
        if os.name == "nt":
            os.kill(os.getpid(), 9)
        else:
            os._exit(0)

    def start_agx(self):
        # Tell AGX where build_scene is located
        sys.argv[0] = self.build_scene_file
        # Use __main__ otherwise AGX will just skip the init
        # pylint: disable=unused-variable
        init = init_app(name="__main__", scenes=[(self.build_scene, "1")], autoStepping=True, onShutdown=self.on_shutdown)
        # pylint: enable=unused-variable

    def run(self):
        signal.signal(signal.SIGINT, self.ctrl_break_handler)
        self.setup_args_parser("").parse_known_args()
        self.start_agx()
