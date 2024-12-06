# Copyright 2012 Canonical Ltd.  All rights reserved.
#
# This file is part of lazr.enum
#
# lazr.enum is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# lazr.enum is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with lazr.enum.  If not, see <http://www.gnu.org/licenses/>.


__all__ = [
    'EnumJSONDecoder',
    'EnumJSONEncoder',
    ]

import json
from lazr.enum import (
    BaseItem,
    enumerated_type_registry,
    )


class EnumJSONEncoder(json.JSONEncoder):
    """A JSON encoder that understands enum objects.

    Objects are serialized using their type and enum name.
    """
    def default(self, obj):
        if isinstance(obj, BaseItem):
            return {
                'type': obj.enum.name,
                'name': obj.name}
        return json.JSONEncoder.default(self, obj)


class EnumJSONDecoder():
    """A decoder can reconstruct enums from a JSON dict.

    Objects are reconstructed using their type and enum name.
    """
    @classmethod
    def from_dict(cls, class_, values):
        type_name = values['type']
        item_name = values['name']
        return enumerated_type_registry[type_name].items[item_name]
