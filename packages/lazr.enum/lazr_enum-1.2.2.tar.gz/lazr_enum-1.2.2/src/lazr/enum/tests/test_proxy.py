# Copyright 2009 Canonical Ltd.  All rights reserved.
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
"Tests that depend on zope.security."

__all__ = [
    'test_suite',
    ]

import doctest
import unittest


def test_proxy_isinstance():
    """
    Proxies such as the zope.security proxy can mask whether an object is an
    instance of a class.  ``proxy_isinstance`` allows you to ask whether a
    proxied object is an instance of another class.

    >>> from lazr.enum import proxy_isinstance

    >>> class C1(object):
    ...     pass

    >>> c = C1()
    >>> proxy_isinstance(c, C1)
    True

    >>> from zope.security.checker import ProxyFactory
    >>> isinstance(ProxyFactory(c), C1)
    False
    >>> proxy_isinstance(ProxyFactory(c), C1)
    True

    >>> class C2(C1):
    ...     pass

    >>> c = C2()
    >>> proxy_isinstance(ProxyFactory(c), C1)
    True
    """


# this differs from the usual name we use for tests, which makes it possible
# for us to only run these tests with the buildout's ./bin/test_proxy command,
# since the tests depend on zope.security, while the package itself does not.
def test_suite():
    return unittest.TestSuite(
        doctest.DocTestSuite())
