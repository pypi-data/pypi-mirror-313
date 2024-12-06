# ******************************************************************************
#  ognajD — Django app which handles ORM objects' versions.                    *
#  Copyright (C) 2021 omelched                                                 *
#                                                                              *
#  This file is part of ognjaD.                                                *
#                                                                              *
#  ognjaD is free software: you can redistribute it and/or modify              *
#  it under the terms of the GNU Affero General Public License as published    *
#  by the Free Software Foundation, either version 3 of the License, or        *
#  (at your option) any later version.                                         *
#                                                                              *
#  ognjaD is distributed in the hope that it will be useful,                   *
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              *
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               *
#  GNU Affero General Public License for more details.                         *
#                                                                              *
#  You should have received a copy of the GNU Affero General Public License    *
#  along with ognjaD.  If not, see <https://www.gnu.org/licenses/>.            *
# ******************************************************************************

import inspect

from django.contrib.contenttypes.admin import GenericTabularInline

from ...models.version import VersionModelPlacepolder


class VersionedModelTabularInline(GenericTabularInline):
    model = VersionModelPlacepolder['version']

    ct_field = 'content_type'
    ct_fk_field = 'object_id'

    extra = 0
    ordering = ['index']
    classes = ['collapse']
    fieldsets = (
        (
            'Header 1', {
                'fields': ('index', 'timestamp')
            }
        ),
        (
            'Header 2', {
                'fields': ('get_version_dump',)
            }
        )
    )
    readonly_fields = ('index', 'timestamp', 'get_version_dump', 'id')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
