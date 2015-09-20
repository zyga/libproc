# encoding: utf-8
#
# This file is part of libproc.
#
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

"""
Low-level bindings to libproc.dylib.

This module exposes only one function, proc_info(). Please refer to the
documentation directory for explanation on how to use it correctly.

.. note::
    That the only low-level binding is the `proc_info()` function itself. All
    of the other functions are pure-python wrappers around it that don't
    require the caller to handle ctypes.
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import ctypes
import ctypes.util
import os
import sys
import unittest

__version__ = '0.2'
__all__ = (
    'proc_info',
    'PROC_CALLNUM_LISTPIDS',
    'PROC_CALLNUM_PIDINFO',
    'PROC_CALLNUM_PIDFDINFO',
    'PROC_CALLNUM_KERNMSGBUF',
    'PROC_CALLNUM_SETCONTROL',
    'PROC_CALLNUM_PIDFILEPORTINFO',
    'PROC_ALL_PIDS',
    'PROC_PGRP_ONLY',
    'PROC_TTY_ONLY',
    'PROC_UID_ONLY',
    'PROC_RUID_ONLY',
    'PROC_PPID_ONLY',
    # Pure-python wrappers:
    'get_all_pids',
    'get_pids_for_uid',
    'get_pids_for_ruid',
    'get_pids_for_ppid',
    'get_pids_for_pgrp',
    'get_pids_for_tty',
)


if sys.platform != 'darwin':
    # NOTE: This mainly is here so that readthedocs can import
    # and build the documentation of this module.
    def __proc_info(callnum, pid, flavor, arg, buffer, buf_size):
        """Fake function available on non-darwin systems."""
        raise NotImplementedError("__proc_info() is only supported on OS X")
else:
    def __proc_info_errcheck(result, func, arguments):
        """Error checker for __proc_info()."""
        proc_errno = ctypes.get_errno()
        if proc_errno != 0:
            raise OSError(proc_errno, os.strerror(proc_errno))
        return result
    # This is the libproc.dylib library.  It is also linked into libc and
    # libSystem. If you already hold a reference to either of those, you can
    # use that as well.
    _libproc_path = ctypes.util.find_library("libproc.dylib")
    _libproc = ctypes.CDLL(_libproc_path, use_errno=True)
    __proc_info = _libproc['__proc_info']
    __proc_info.restype = ctypes.c_int
    __proc_info.argtypes = [
        ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint64,
        ctypes.c_void_p, ctypes.c_int]
    __proc_info.errcheck = __proc_info_errcheck

#: The proc_info() low-level system call.
#:
#: The python3-style signature of proc_info() is::
#:
#:     __proc_info(
#:          callnum: ctypes.c_int,
#:          pid: ctypes.c_int,
#:          flavor: ctypes.c_int,
#:          arg: ctypes.c_uint64,
#:          buffer: ctypes.c_void_p,
#:          buf_size: ctypes.c_int
#:     ) -> ctypes.c_int
#:
#: There is also an error checker that raises :class:`python:OSError` if
#: the underlying call fails. This is easy to do if the buffer is handled
#: incorrectly or *callnum* or *pid* are invalid.
#:
#: This function uses multiplexing on *callnum* to invoke distinct kernel
#: functions. Please look at the *PROC_CALLNUM_xxx* family of constants
#: for details.
proc_info = __proc_info

# NOTE: Those are found in xnu source code in proc_info_internal()
#: Value of __proc_info(callnum, ...), returns a list of PIDs.
PROC_CALLNUM_LISTPIDS = 1
#: Undocumented.
PROC_CALLNUM_PIDINFO = 2
#: Undocumented.
PROC_CALLNUM_PIDFDINFO = 3
#: Undocumented.
PROC_CALLNUM_KERNMSGBUF = 4
#: Undocumented.
PROC_CALLNUM_SETCONTROL = 5
#: Undocumented.
PROC_CALLNUM_PIDFILEPORTINFO = 6


# NOTE: Those can be found in <sys/proc_info.h>
#: When called with callnum 1, return all processes
PROC_ALL_PIDS = 1
#: When called with callnum 1, return all processes in a given group
PROC_PGRP_ONLY = 2
#: When called with callnum 1, return all processes attached to a given tty
PROC_TTY_ONLY = 3
#: When called with callnum 1, return all processes with the given UID
PROC_UID_ONLY = 4
#: When called with callnum 1, return all processes with the given RUID
PROC_RUID_ONLY = 5
#: When called with callnum 1, return all processes with the given PPID
PROC_PPID_ONLY = 6

_size_of_c_int = ctypes.sizeof(ctypes.c_int)


def _get_pids(filter_type, filter_arg):
    """
    Get a list of PIDs (process IDs) with specific libproc filter.

    :param filter_type:
        One of :data:`PROC_ALL_PIDS`, :data:`PROC_PGRP_ONLY`,
        :data:`PROC_TTY_ONLY`, :data:`PROC_UID_ONLY`
        :data:`PROC_RUID_ONLY` or :data:`PROC_PPID_ONLY`. This argument
        describes the type of filtering to apply.
    :param filter_arg:
        The specific process property filter value to look for. For
        :data:`PROC_ALL_PIDS` this value is ignored.
    """
    buf_size = proc_info(
        PROC_CALLNUM_LISTPIDS, filter_type, filter_arg, 0, None, 0)
    pid_list = (ctypes.c_int * (buf_size // _size_of_c_int))()
    assert ctypes.sizeof(pid_list) == buf_size
    retval = proc_info(
        PROC_CALLNUM_LISTPIDS, filter_type, filter_arg, 0, pid_list, buf_size)
    return pid_list[:retval // _size_of_c_int]


def get_all_pids():
    """
    Get a list of all process IDs.

    :returns:
        A list of all the process IDs on this system.
    :raises OSError:
        If the underlying system call fails.
    """
    return _get_pids(PROC_ALL_PIDS, 0)


def get_pids_for_uid(uid):
    """
    Get a list of PIDs (process IDs) with the specific user ID.

    :param uid:
        The UID to look for.
    :returns:
        A list of matching PIDs.
    :raises OSError:
        If the underlying system call fails.
    """
    return _get_pids(PROC_UID_ONLY, uid)


def get_pids_for_ruid(ruid):
    """
    Get a list of PIDs (process IDs) with the specific real user ID.

    :param ruid:
        The RUID to look for.
    :returns:
        A list of matching PIDs.
    :raises OSError:
        If the underlying system call fails.
    """
    return _get_pids(PROC_RUID_ONLY, ruid)


def get_pids_for_ppid(ppid):
    """
    Get a list of PIDs (process IDs) with the specific parent PID.

    :param ppid:
        The parent process ID to look for.
    :returns:
        A list of matching PIDs.
    :raises OSError:
        If the underlying system call fails.
    """
    return _get_pids(PROC_PPID_ONLY, ppid)


def get_pids_for_pgrp(pgrp):
    """
    Get a list of PIDs (process IDs) with the specific process group.

    :param pgrp:
        The process group ID to look for.
    :returns:
        A list of matching PIDs.
    :raises OSError:
        If the underlying system call fails.
    """
    return _get_pids(PROC_PGRP_ONLY, pgrp)


def get_pids_for_tty(tty):
    """
    Get a list of PIDs (process IDs) with the specific TTY.

    :param tty:
        The TTY to look for.
    :returns:
        A list of matching PIDs.
    :raises OSError:
        If the underlying system call fails.
    """
    return _get_pids(PROC_TTY_ONLY, tty)


class TestSmoke(unittest.TestCase):

    """Smoke tests for the higher-level functions."""

    def setUp(self):
        """Common set-up code."""
        self.uid = os.getuid()
        self.pid = os.getpid()
        self.ppid = os.getppid()

    def test_get_all_pids(self):
        """Smoke test for get_all_pids()."""
        pids = get_all_pids()
        self.assertNotEqual(pids, [])
        self.assertIn(self.pid, pids)

    def test_get_pids_for_uid(self):
        """Smoke test for get_pids_for_uid()."""
        pids = get_pids_for_uid(self.uid)
        self.assertNotEqual(pids, [])
        self.assertIn(self.pid, pids)

    def test_get_pids_for_ruid(self):
        """Smoke test for get_pids_for_ruid()."""
        pids = get_pids_for_ruid(self.uid)
        self.assertNotEqual(pids, [])
        self.assertIn(self.pid, pids)

    def test_get_pids_for_ppid(self):
        """Smoke test for get_pids_for_ppid()."""
        pids = get_pids_for_ppid(self.ppid)
        self.assertNotEqual(pids, [])
        self.assertIn(self.pid, pids)

    def test_get_pids_for_pgrp(self):
        """Smoke test for get_pids_for_pgrp()."""
        # Move this process to a dedicated process group
        os.setpgid(0, self.pid)
        pids = get_pids_for_pgrp(self.pid)
        self.assertNotEqual(pids, [])
        self.assertIn(self.pid, pids)


if __name__ == '__main__':
    import unittest
    unittest.main()
