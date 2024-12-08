# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

"""Plane base app."""

import os

from datalayer_core.application import DatalayerApp, base_aliases, base_flags
from traitlets import Unicode

from .. import __version__


datalayer_plane_aliases = dict(base_aliases)
datalayer_plane_aliases["cloud"] = "PlaneBaseApp.cloud"

datalayer_plane_flags = dict(base_flags)


class PlaneBaseApp(DatalayerApp):
    """An base application for Plane."""

    version = __version__

    aliases = datalayer_plane_aliases
    flags = datalayer_plane_flags

    cloud = Unicode(
        "ovh",
        config=True,
        help="The cloud to use.",
    )


    def start(self):
        super(PlaneBaseApp, self).start()
        if os.environ.get("KUBECONFIG", None) is None:
            from clouder.apps.ctx import get_default_kubeconfig_path
            default_kubeconfig_path = get_default_kubeconfig_path()
            if default_kubeconfig_path:
                os.environ["KUBECONFIG"] = default_kubeconfig_path
