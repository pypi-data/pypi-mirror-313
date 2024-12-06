# Copyright 2009-2019 Canonical Ltd.  All rights reserved.
#
# This file is part of lazr.enum
#
# lazr.enum is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# lazr.enum is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with lazr.enum.  If not, see <http://www.gnu.org/licenses/>.

"""Test harness for doctests."""


__all__ = [
    'load_tests',
    ]

import atexit
import doctest
import os

import pkg_resources


DOCTEST_FLAGS = (
    doctest.ELLIPSIS |
    doctest.NORMALIZE_WHITESPACE |
    doctest.REPORT_NDIFF)


def setUp(test):
    pass


def find_doctests(suffix):
    """Find doctests matching a certain suffix."""
    doctest_files = []
    if pkg_resources.resource_exists('lazr.enum', 'docs'):
        for name in pkg_resources.resource_listdir('lazr.enum', 'docs'):
            if name.endswith(suffix):
                doctest_files.append(
                    os.path.abspath(
                        pkg_resources.resource_filename(
                            'lazr.enum', 'docs/%s' % name)))
    return doctest_files


def load_tests(loader, tests, pattern):
    """Load all the doctests."""
    atexit.register(pkg_resources.cleanup_resources)
    tests.addTest(doctest.DocFileSuite(
        *find_doctests('.rst'),
        module_relative=False, setUp=setUp, optionflags=DOCTEST_FLAGS))
    return tests
