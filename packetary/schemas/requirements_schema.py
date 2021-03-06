# -*- coding: utf-8 -*-

#    Copyright 2016 Mirantis, Inc.
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

REQUIREMENTS_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "anyOf": [
        {"required": ["packages"]},
        {"required": ["repositories"]},
        {"required": ["mandatory"]}
    ],
    "properties": {
        "repositories": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name"],
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "excludes": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "patternProperties": {
                                r"[a-z][\w_]*": {
                                    "type": "string"
                                }
                            }
                        }
                    }
                }
            }
        },
        "packages": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name"],
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "versions": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "pattern": "^([<>]=?|=)\s+.+$"
                        }
                    }
                }
            }
        },
        "mandatory": {
            "enum": ["exact", "newest"]
        }
    }
}
