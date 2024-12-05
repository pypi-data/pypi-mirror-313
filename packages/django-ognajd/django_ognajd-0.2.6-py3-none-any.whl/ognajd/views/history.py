from typing import Any

from django.views.generic.detail import DetailView
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
import jsondiff as jd

from ognajd.models import Version, VersionModelPlacepolder


_USER_MODEL = get_user_model()


class HistoryView(DetailView):
    """
    Render a "history" view of an object.
    """

    template_name_suffix = "_history"
    context_history_key = "history"

    def get_history(self):
        version_model: Version = VersionModelPlacepolder["version"]
        versions = (
            version_model.objects.filter(
                content_type=ContentType.objects.get_for_model(self.model),
                object_id=self.object.pk,
            )
            .order_by("index")
            .values(
                "index",
                "author_id",
                "author_name",
                "timestamp",
                "dump",
            )
        )
        if not versions:
            return []

        authors_cache = {
            user.pk: user
            for user in _USER_MODEL.objects.filter(
                pk__in=[version["author_id"] for version in versions]
            )
        }

        history = []
        current = {}

        for version in versions:
            current = jd.patch(current, version["dump"], marshal=True)
            history.append(
                {
                    "index": version["index"],
                    "author": authors_cache.get(version["author_id"], None),
                    "author_name": version["author_name"],
                    "timestamp": version["timestamp"],
                    "state": current,
                    "diff": version["dump"],
                }
            )

        return history

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx[self.context_history_key] = self.get_history()

        return ctx
