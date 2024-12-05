import threading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser
    from django.http import HttpRequest, HttpResponse


_thread_local = threading.local()


def get_context() -> dict:
    return _thread_local.__dict__.setdefault("ognajd_context", {})


def discard_context():
    _thread_local.__dict__["ognajd_context"] = {}


def set_context(author: "AbstractUser" = None, author_name: str = ""):
    ctx = get_context()

    ctx["author"] = author

    if not author_name and author:
        author_name = str(author)

    ctx["author_name"] = author_name


class OgnajdContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: "HttpRequest") -> "HttpResponse":
        set_context(request.user)

        response = self.get_response(request)

        discard_context()

        return response
