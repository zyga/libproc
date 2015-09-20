===================================
Low-level bindings to libproc.dylib
===================================

Introduction
============

This module contains descriptions and wrappers around interesting parts of the
libproc.dylib shared library. This library exposes internal kernel data about
processes of OS X. It was developed and tested on OS X 10.7.5, using i386
architecture.

Many aspects were traced manually from xnu source code as this library is
severely undocumented.

Low-level API
=============

The entire action of this library revolves around the function
``__proc_info()`` which is a simple wrapper around a system call. The signature
of the function is as follows (Internal private prototype taken from
``libproc.c``)::

    int
    __proc_info(
      int callnum,    // One of _PROC_CALLNUM_xxx constants below.
      int pid,        // Varies per callnum, see below.
      int flavor,     // Ditto.
      uint64_t arg,   // Ditto, sometimes unused.
      void *buffer,   // Output buffer.
      int buffersize  // Size of output buffer.
    );

The only low level API is ``__proc_info()`` itself.

The behavior of this function depends on the first argument, *callnum*, which
is typical of many kernel interfaces. Unfortunately distinct values of
*callnum* do not have any official names (in the source code they are simply
hard-coded constants. I have used a convention *_PROC_CALLNUM_xxx* where *xxx*
is derived from the name of the kernel function multiplexed by that value.

The values I have made are::

    PROC_CALLNUM_LISTPIDS = 1
    PROC_CALLNUM_PIDINFO = 2
    PROC_CALLNUM_PIDFDINFO = 3
    PROC_CALLNUM_KERNMSGBUF = 4
    PROC_CALLNUM_SETCONTROL = 5
    PROC_CALLNUM_PIDFILEPORTINFO = 6

You can verify them by looking at ``proc_info_internal()`` in the xnu source
code: ``xnu/bsd/kern/proc_info.c``.

Whenever this function is called with NULL value for *buffer*, it will compute
and return the correct size of the buffer to pass. Looking at the source code
of the system call it makes some conservative estimates but I suspect it is
still racy (a fork bomb might make the value invalid between the first and
second calls).

Callnum 1
---------

.. note::
    This *callnum* has a liproc-only alias of *PROC_CALLNUM_LISTPIDS*

When *callnum* is :data:`~libproc.PROC_CALLNUM_LISTPIDS` then the function
obtains a list of process identifiers that match some criteria.

The remaining arguments have the following meaning:

*pid*:
    Contains the type of process list to obtain. The possible values are one of
    *PROC_xxx* constants listed below.

    :data:`~libproc.PROC_ALL_PIDS`:
        Return the full process table.
    :data:`~libproc.PROC_PGRP_ONLY`:
        Return a list of processes that have a given process group ID
    :data:`~libproc.PROC_TTY_ONLY`:
        Return a list of processes that are attached to a given TTY
    :data:`~libproc.PROC_UID_ONLY`:
        Return a list of processes that have a given user ID.
    :data:`~libproc.PROC_RUID_ONLY`:
        Return a list of processes that have a given real user ID.
    :data:`~libproc.PROC_PPID_ONLY`:
        Return a list of processes that are children of a given process.

*flavor*:
    Contains the optional filtering argument for the processes that are
    returned. The value passed here is compared against the desired property of
    each process. The only exception is *PROC_ALL_PIDS* where no filtering
    takes place.

*arg*:
    This parameter is unused.

*buffer*:
    This parameter is the pointer to the output buffer. The buffer is an
    array of :class:`python:ctypes.c_int` of appropriate size (as determined
    by the size of the process table).

    As a convention, you can pass a None value (which maps to a *NULL* pointer)
    to ask the kernel for the size of the buffer. Correct buffer size in bytes
    is then returned by the call.

*buf_size*:
    Size of the buffer, in bytes.

The return value is either the number of bytes needed or the number of bytes
written to the buffer (see the discussion of *buffer* argument above).

Callnum 2
---------

.. note::
    This *callnum* has a liproc-only alias of *PROC_CALLNUM_PIDINFO*

This *callnum* is currently undocumented.

Callnum 3 
---------

.. note::
    This *callnum* has a liproc-only alias of *PROC_CALLNUM_PIDFDINFO*

This *callnum* is currently undocumented.

Callnum 4
---------

.. note::
    This *callnum* has a liproc-only alias of *PROC_CALLNUM_KERNMSGBUF*

This *callnum* is currently undocumented.

Callnum 5
---------

.. note::
    This *callnum* has a liproc-only alias of *PROC_CALLNUM_SETCONTROL*

This *callnum* is currently undocumented.

Callnum 6
---------

.. note::
    This *callnum* has a liproc-only alias of *PROC_CALLNUM_PIDFILEPORTINFO*

This *callnum* is currently undocumented.

Higher-level APIs
=================

This library contains a number of higher-level functions that call
``__proc_info()`` with appropriate arguments, handle buffer allocation and
return friendly pythonic values.

You can find them below:

Callnum 1
---------

The following wrappers exist for this *callnum*:

- :func:`~libproc.get_all_pids()`.
- :func:`~libproc.get_pids_for_uid()`.
- :func:`~libproc.get_pids_for_ruid()`.
- :func:`~libproc.get_pids_for_ppid()`.
- :func:`~libproc.get_pids_for_pgrp()`.
- :func:`~libproc.get_pids_for_tty()`.
