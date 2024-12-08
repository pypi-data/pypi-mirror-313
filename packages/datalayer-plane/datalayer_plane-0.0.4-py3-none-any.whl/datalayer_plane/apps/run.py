# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

"""Plane run application."""

import sys

from ..util.utils import run_sbin, run_shell
from ._base import PlaneBaseApp


class PlaneRunShellApp(PlaneBaseApp):
    """A shell application for Plane."""

    description = """
      Run predefined shell scripts.
    """

    def start(self):
        super().start()
        args = sys.argv
        if len(args) > 2:
            cmd = "-".join(args[2:])
            cmd_args = args[0:2] + [cmd]
            run_shell(cmd_args)
        else:
            self.log.error("You must provide a shell script to run.")


class PlaneRunSbinApp(PlaneBaseApp):
    """A shell application for Plane."""

    description = """
      Run predefined shell scripts.
    """

    def __init__(self):
        super().__init__()

    def start(self):
        super().start()
        args = ["shell"]
        if len(sys.argv) == 1:
            sys.argv.append("about")
        args = args + sys.argv
#        cmd = "-".join(args[2:])
#        cmd_args = args[0:2] + [cmd]
        cmd_args = args[0:2] + args[2:]
        run_sbin(cmd_args)
