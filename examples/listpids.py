#!/usr/bin/env python
# Copyright 2015 Zygmunt Krynicki.
# Written by:
#   Zygmunt Krynicki <me@zygoon.pl>
#
# libproc is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3,
# as published by the Free Software Foundation.
#
# libproc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with libproc.  If not, see <http://www.gnu.org/licenses/>.

"""Examples for obtaining list of PIDs."""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import os

try:
    import guacamole
except ImportError:
    raise SystemExit("Examples depend on the guacamole library")

import libproc


class cmd_all(guacamole.Command):

    """Display a list of all process IDs."""

    def invoked(self, ctx):
        """Invoke this command."""
        for pid in libproc.get_all_pids():
            print(pid)


class cmd_uid(guacamole.Command):

    """Display a list of PIDs with the specific user ID."""

    def register_arguments(self, parser):
        """Register command-specific arguments."""
        parser.add_argument(
            'uid', default=os.getuid(), type=int, nargs='?',
            help="user ID to look for (default: current)")

    def invoked(self, ctx):
        """Invoke this command."""
        for pid in libproc.get_pids_for_uid(ctx.args.uid):
            print(pid)


class cmd_ruid(guacamole.Command):

    """Display a list of PIDs with the specific real user ID."""

    def register_arguments(self, parser):
        """Register command-specific arguments."""
        parser.add_argument(
            'ruid', default=os.geteuid(), type=int, nargs='?',
            help="real user ID to look for (default: current)")

    def invoked(self, ctx):
        """Invoke this command."""
        for pid in libproc.get_pids_for_ruid(ctx.args.ruid):
            print(pid)


class cmd_ppid(guacamole.Command):

    """Display a list of PIDs with the specific parent PID."""

    def register_arguments(self, parser):
        """Register command-specific arguments."""
        parser.add_argument(
            'ppid', default=os.getppid(), type=int, nargs='?',
            help="parent process to look for (default:current)")

    def invoked(self, ctx):
        """Invoke this command."""
        for pid in libproc.get_pids_for_ppid(ctx.args.ppid):
            print(pid)


class cmd_pgrp(guacamole.Command):

    """Display a list of PIDs with the specific process group."""

    def register_arguments(self, parser):
        """Register command-specific arguments."""
        parser.add_argument(
            'pgrp', default=os.getpgid(0), type=int, nargs='?',
            help="process group to look for (default: current)")

    def invoked(self, ctx):
        """Invoke this command."""
        for pid in libproc.get_pids_for_pgrp(ctx.args.pgrp):
            print(pid)


class cmd_tty(guacamole.Command):

    """Display a list of PIDs with the specific TTY."""

    def register_arguments(self, parser):
        """Register command-specific arguments."""
        parser.add_argument(
            'tty', type=int, help="TTY to look for")

    def invoked(self, ctx):
        """Invoke this command."""
        # NOTE: I don't really know how to use this!
        for pid in libproc.get_pids_for_tty(ctx.args.tty):
            print(pid)


class cmd_listpids(guacamole.Command):

    """
    Versatile PID (process ID) listing tool.

    This application demonstrates the usage of the libproc library.
    Specifically, this tool focuses on listing processes. Each sub-command
    shows a list of PIDs that match some search criteria.
    """

    sub_commands = (
        ('all', cmd_all),
        ('uid', cmd_uid),
        ('ruid', cmd_ruid),
        ('ppid', cmd_ppid),
        ('pgrp', cmd_pgrp),
        ('tty', cmd_tty),
    )


if __name__ == '__main__':
    cmd_listpids().main()
