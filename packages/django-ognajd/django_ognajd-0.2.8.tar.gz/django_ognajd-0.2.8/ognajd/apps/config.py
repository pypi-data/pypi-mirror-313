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
from functools import partial

from django.apps import AppConfig
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core import serializers

from ognajd.src.exceptions import NoDiff
from ognajd.middleware.context import get_context


class OgnajdConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ognajd"

    def prepare_versioning(self, model):
        if not getattr(model.VersioningMeta, "enable", True):
            # VersioningMeta exists but not enabled, no versioning required
            return

        if getattr(model.VersioningMeta, "managed_serializer", False):
            serializer_fn = model.objects.serialize
        else:
            serializer_fn = partial(serializers.serialize, format="json")

        @receiver(post_save, sender=model)
        def receiver_func(sender, instance, created, **kwargs):
            if getattr(instance, "ognajd_ignore_version", False):
                setattr(instance, "ognajd_ignore_version", False)
                return

            dump = json.loads(serializer_fn(queryset=[instance]))[0]["fields"]
            ctx = get_context()
            author = ctx.get("author", None)
            if not getattr(author, "is_authenticated", False):
                author = None

            try:
                self.version_model_placeholder["version"].objects.create(
                    ref=instance,
                    dump=dump,
                    author=author,
                    author_name=ctx.get("author_name", ""),
                )
            except NoDiff:
                pass

        setattr(
            self.version_attr_placeholder,
            f"create_{model._meta.app_label}_{model.__name__}_version",
            types.MethodType(receiver_func, self.version_attr_placeholder),
        )

    def ready(self):
        from ..models import VersionAttrPlaceholder, make_class, VersionModelPlacepolder

        self.version_model_placeholder = VersionModelPlacepolder
        self.version_attr_placeholder = VersionAttrPlaceholder

        versioned_models = [
            model
            for app in self.apps.app_configs.values()
            for model in app.models.values()
            if hasattr(model, "VersioningMeta")
            and getattr(model._meta, "proxy", False) is False
        ]

        for versioned_model in versioned_models:
            self.prepare_versioning(versioned_model)

        make_class()

        self.import_models()
