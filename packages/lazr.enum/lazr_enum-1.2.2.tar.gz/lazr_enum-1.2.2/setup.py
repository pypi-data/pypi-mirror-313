#!/usr/bin/env python

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

from setuptools import setup, find_packages


# generic helpers primarily for the long_description
def generate(*docname_or_string):
    marker = '.. pypi description ends here'
    res = []
    for value in docname_or_string:
        if value.endswith('.rst'):
            with open(value) as f:
                value = f.read()
            idx = value.find(marker)
            if idx >= 0:
                value = value[:idx]
        res.append(value)
        if not value.endswith('\n'):
            res.append('')
    return '\n'.join(res)
# end generic helpers


tests_require = [
    'zope.testrunner',
    ]

setup(
    name='lazr.enum',
    version='1.2.2',
    namespace_packages=['lazr'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    maintainer='LAZR Developers',
    maintainer_email='lazr-developers@lists.launchpad.net',
    description=open('README.rst').readline().strip(),
    long_description=generate(
        'src/lazr/enum/docs/index.rst',
        'NEWS.rst'),
    license='LGPL v3',
    install_requires=[
        'importlib-metadata; python_version < "3.8"',
        'setuptools',
        'six',
        'zope.interface>=3.6.0',
        'zope.schema',
        ],
    url='https://launchpad.net/lazr.enum',
    project_urls={
        "Source": "https://code.launchpad.net/lazr.enum",
        "Issue Tracker": "https://bugs.launchpad.net/lazr.enum",
        "Documentation": "https://lazrenum.readthedocs.io/en/latest/",
    },
    download_url='https://launchpad.net/lazr.enum/+download',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",  # noqa: E501
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        ],
    tests_require=tests_require,
    extras_require=dict(
        proxy=['zope.security'],
        docs=['Sphinx'],
        test=tests_require,
    ),
    test_suite='lazr.enum.tests',
    )
