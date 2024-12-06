# ******************************************************************************
#  ognajD — Django app which handles ORM objects' versions.                    *
#  Copyright (C) 2021-2021 omelched                                            *
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

import json
import types
import uuid
import hashlib
import inspect
from functools import cached_property

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import jsondiff as jd

from ..src.exceptions import VersioningError, NoDiff


class Version(models.Model):
    """Abstract class to prototype VersionModel.

    His child will be defined at runtime in OgnajdConfig.ready().
    """

    class Meta:
        abstract = True

    id = models.UUIDField(
        primary_key=True,
        null=False,
        blank=False,
        default=uuid.uuid4,
        verbose_name=_("UUID"),
        editable=False,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name=_("Author"),
        null=True,
        blank=False,
        related_name="versions",
    )
    author_name = models.CharField(
        max_length=128,
        verbose_name=_("Author name"),
        null=False,
        blank=True,
        default="",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name=_("Content type"),
    )
    object_id = models.CharField(
        max_length=36,
        null=False,
        blank=False,
        verbose_name=_("Object id"),
    )
    ref = GenericForeignKey("content_type", "object_id")
    index = models.IntegerField(
        null=False,
        blank=False,
        editable=True,
        default=0,
        verbose_name=_("Index"),
    )
    timestamp = models.DateTimeField(
        null=False,
        blank=False,
        editable=False,
        auto_now_add=True,
        verbose_name=_("Timestamp"),
    )
    dump = models.JSONField(
        null=False,
        blank=False,
        editable=False,
        verbose_name=_("Dump"),
    )
    hash = models.CharField(
        max_length=32,
        null=False,
        blank=False,
        verbose_name=_("Hash"),
    )

    objects = models.Manager()

    @cached_property
    def versioning_meta(self):
        """Returns versioning metadata for related model."""

        versioned_model = self.content_type.model_class()
        versioning_meta = getattr(versioned_model, "VersioningMeta", None)

        if not versioning_meta:
            raise VersioningError(
                f"VersioningMeta is not defined for model {versioned_model}, restart required"
            )

        return versioning_meta

    def get_version_dump(self) -> dict:
        """Form related object's dump in respect to instanced version.

        Method gets first diff (a.k.a initial dump) and patches all remaining prior to
        instanced version (inclusively). It must not be called at unsaved version
        instances.
        If related object configured to store dumps, not diffs — returns dump.

        :return: related object's dump
        :rtype: dict[Any]
        """

        # if model not saved — current version is unavailable
        if self._state.adding:
            raise VersioningError("get_dump() can not be called at unsaved instance")

        if not getattr(self.versioning_meta, "store_diff"):
            return self.dump

        # collect all diffs prior to instanced version
        diffs = tuple(
            VersionModelPlacepolder["version"]
            .objects.filter(
                content_type=self.content_type,
                object_id=self.object_id,
                index__lte=self.index,
            )
            .order_by("index")
            .values_list("dump", flat=True)
        )

        # initial dump
        dump = diffs[0]

        # if there is only one diff — return initial dump
        if len(diffs) < 2:
            return dump

        # patch dump for every diff consecutively
        for diff in diffs[1:]:
            dump = jd.patch(dump, diff, marshal=True)

        return dump

    def save(self, *args, **kwargs):
        latest_version: Version = (
            VersionModelPlacepolder["version"]
            .objects.filter(
                content_type=self.content_type,
                object_id=self.object_id,
            )
            .order_by("-index")
            .first()
        )
        self.hash = hashlib.md5(json.dumps(self.dump).encode("utf-8")).hexdigest()

        # If there is at least one version
        if latest_version:
            no_changes = self.hash == latest_version.hash

            # if there is no changes (a.k.a. equal hash)
            if no_changes:
                # and we do not need to save versions with no changes — abort saving
                if not getattr(self.versioning_meta, "save_empty_changes"):
                    raise NoDiff

            # If we need to store diff
            if getattr(self.versioning_meta, "store_diff"):
                # and there were no changes — do not run jsondiff.diff(...)
                if no_changes:
                    self.dump = {}
                else:
                    self.dump = jd.diff(
                        latest_version.get_version_dump(), self.dump, marshal=True
                    )

            # increment version index
            self.index = latest_version.index + 1

        super(Version, self).save(*args, **kwargs)


class VersionAttrPlaceholder:
    """Placeholder base class to store dynamic attributes.

    Attributes (mostly, methods), that will be generated at OgnajdConfig.ready() are
    bound to this class.
    """

    pass


VersionModelPlacepolder = {}


def make_class():
    class Meta:
        indexes = [
            models.Index(
                fields=(
                    "content_type_id",
                    "object_id",
                ),
            )
        ]

    def copy_placeholder_methods(ns):
        for name, method in [
            t
            for t in inspect.getmembers(
                VersionAttrPlaceholder, lambda m: inspect.ismethod(m)
            )
            if not t[0].startswith("_")
        ]:
            ns[name] = types.MethodType(method, Version)
        ns["__module__"] = __name__
        ns["__qualname__"] = "Version"
        ns["Meta"] = Meta

    VersionModelPlacepolder["version"] = types.new_class(
        "Version",
        bases=(Version,),
        exec_body=copy_placeholder_methods,
    )
