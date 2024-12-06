# Copyright 2004-2009 Canonical Ltd.  All rights reserved.
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


__all__ = [
    'IEnumeratedType',
    ]

from zope.interface import Attribute, Interface


class IEnumeratedType(Interface):
    """Defines the attributes that EnumeratedTypes have."""
    name = Attribute(
        "The name of the EnumeratedType is the same as the name of the class.")
    description = Attribute(
        "The description is the docstring of the EnumeratedType class.")
    sort_order = Attribute(
        "A tuple of Item names that is used to determine the ordering of the "
        "Items.")
    items = Attribute(
        "An instance of `EnumItems` which allows access to the enumerated "
        "types items by either name of database value if the items are "
        "DBItems.")
