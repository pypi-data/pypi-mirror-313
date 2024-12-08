# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

from . import __version__

from pathlib import Path

from traitlets import Bool, Unicode

from .apps import (PlaneKubernetesApp,
                   PlaneRunSbinApp, PlaneRunShellApp)

from datalayer_core.application import DatalayerApp, NoStart, base_aliases, base_flags

HERE = Path(__file__).parent


datalayer_plane_aliases = dict(base_aliases)
datalayer_plane_aliases["cloud"] = "PlaneApp.cloud"

datalayer_plane_flags = dict(base_flags)
datalayer_plane_flags["dev-build"] = (
    {"PlaneApp": {"dev_build": True}},
    "Build in development mode.",
)
datalayer_plane_flags["no-minimize"] = (
    {"PlaneApp": {"minimize": False}},
    "Do not minimize a production build.",
)


class PlaneApp(DatalayerApp):
    name = "datalayer_plane"
    description = """
    Import or export a JupyterLab workspace or list all the JupyterLab workspaces

    You can use the "config" sub-commands.
    """
    version = __version__

    aliases = datalayer_plane_aliases
    flags = datalayer_plane_flags

    cloud = Unicode("ovh", config=True, help="")

    minimize = Bool(
        True,
        config=True,
        help="",
    )

    subcommands = {
        "k8s": (PlaneKubernetesApp, PlaneKubernetesApp.description.splitlines()[0]),
        "sh": (PlaneRunShellApp, PlaneRunShellApp.description.splitlines()[0]),
    }

    def initialize(self, argv=None):
        """Subclass because the ExtensionApp.initialize() method does not take arguments"""
        super().initialize()

    def start(self):
        super(PlaneApp, self).start()
        plane_sbin = PlaneRunSbinApp()
        plane_sbin.start()


# -----------------------------------------------------------------------------
# Main entry point
# -----------------------------------------------------------------------------

main = launch_new_instance = PlaneApp.launch_instance

if __name__ == "__main__":
    main()
