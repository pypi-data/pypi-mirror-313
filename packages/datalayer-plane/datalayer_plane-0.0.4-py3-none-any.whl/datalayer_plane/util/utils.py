# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

import subprocess

from pathlib import Path

HERE_FOLDER = Path(__file__).parent


def run_shell(args):
    """Run a shell command."""

    subprocess.run(args[2:])


def run_sbin(args):
    """Run a sbin command."""

    args[2] = args[2] + ".sh"

    cmd = ["bash", str(HERE_FOLDER / ".." / "sbin" / "plane.sh")]
    cmd.extend(args[2:])

    subprocess.run(cmd)


def run_sbin_direct(args):
    """Run directly a sbin command."""

    args[2] = ["", "", ] + args[2] + ".sh"

    run_sbin(args)
