# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

import warnings

from pathlib import Path

from datalayer_core.application import NoStart

from ._base import PlaneBaseApp


SSH_FOLDER = Path.home() / ".ssh"


class KubernetesListApp(PlaneBaseApp):
    """An application to list the kubernetes clusters."""

    description = """
      An application to list the kubernetes clusters
    """

    def start(self):
        """Start the app."""
        if len(self.extra_args) > 1:  # pragma: no cover
            warnings.warn("Too many arguments were provided.")
            self.exit(1)
        for file in SSH_FOLDER.iterdir():
            if file.name.endswith(".pub"):
                print(file.name.replace(".pub", ""))


class PlaneKubernetesApp(PlaneBaseApp):
    """An application for the kubernetes clusters."""

    description = """
      Manage the kubernetes clusters
    """

    subcommands = {
        "list": (KubernetesListApp, KubernetesListApp.description.splitlines()[0]),
    }

    def start(self):
        try:
            super().start()
            self.log.info(f"One of `{'`, `'.join(PlaneKubernetesApp.subcommands.keys())}` must be specified.")
            self.exit(1)
        except NoStart:
            pass
        self.exit(0)
