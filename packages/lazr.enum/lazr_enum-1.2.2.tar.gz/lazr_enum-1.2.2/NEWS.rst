==================
NEWS for lazr.enum
==================

1.2.2 (2024-12-05)
==================

- Add support for Python 3.9, 3.10, 3.11, 3.12 and 3.13.
- Drop support for Python 3.7 and below
- Add basic pre-commit configuration.
- Publish documentation on Read the Docs.

1.2.1 (2021-09-13)
==================

- Adjust versioning strategy to avoid importing pkg_resources, which is slow
  in large environments.

1.2 (2019-11-24)
================

- Switch from buildout to tox.
- Add Python 3 support.

1.1.4 (2012-04-18)
==================

- Support for serialising enums to/from json (lp:984549)
- Items which are not in an enumerator always compare as False (lp:524259)
- Fix the licence statement in _enum.py to be LGPLv3 not LGPLv3+ (lp:526484)

1.1.3 (2011-04-20)
==================

- added case insensitivity to getting the term by the token value (lp:154556)

1.1.2 (2009-08-31)
==================

- removed unnecessary build dependencies

1.1.1 (2009-08-06)
==================

- Removed sys.path hack from setup.py.

1.1 (2009-06-08)
================

- Added `url` argument to the BaseItem and DBItem constructors.


1.0 (2009-03-24)
================

- Initial release on PyPI
