#!/usr/bin/env python
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

"""setup for libproc."""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


setup(
    name='libproc',
    version='0.2',
    description='Low-level bindings to libproc.dylib',
    long_description=readme + '\n\n' + history,
    author='Zygmunt Krynicki',
    author_email='me@zygoon.pl',
    url='https://github.com/zyga/libproc',
    py_modules=['libproc'],
    test_suite='libproc',
    include_package_data=False,
    license="LGPLv3",
    zip_safe=True,
    keywords='libproc.dylib libproc proc bindings',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        ('License :: OSI Approved :: GNU Lesser General Public License v3'
         ' (LGPLv3)'),
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
