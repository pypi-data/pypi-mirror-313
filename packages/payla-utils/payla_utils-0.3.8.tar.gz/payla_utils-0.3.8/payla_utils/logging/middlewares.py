import uuid
from collections.abc import Callable

import structlog
from django.http import HttpRequest, HttpResponse

from payla_utils.settings import payla_utils_settings

logger = structlog.get_logger(__name__)


def get_request_header(request, header_key, meta_key):
    if hasattr(request, "headers"):
        return request.headers.get(header_key)

    return request.META.get(meta_key)


class RequestMiddleware:
    """``RequestMiddleware`` adds request metadata to ``structlog``'s logger context automatically.
    Make sure to add it after AuthenticationMiddleware in your MIDDLEWARE setting to have the request.user available.
    >>> MIDDLEWARE = [
    ...     # ...
    ...     'payla_utils.middlewares.RequestMiddleware',
    ... ]
    """

    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response
        self._raised_exception = False

    def __call__(self, request: HttpRequest) -> HttpResponse:
        from ipware import get_client_ip

        request_id_header = payla_utils_settings.REQUEST_ID_HEADER or "X-Request-ID"

        request_id = get_request_header(
            request, request_id_header.lower(), f"HTTP_{request_id_header.upper().replace('-', '_')}"
        ) or str(uuid.uuid4())

        structlog.contextvars.bind_contextvars(request_id=request_id)
        self.bind_user_id(request)

        ip, _ = get_client_ip(request)
        structlog.contextvars.bind_contextvars(ip=ip)

        # add request host, method, and path
        structlog.contextvars.bind_contextvars(
            request_host=request.get_host(),
            request_method=request.method,
            request_path=request.path,
        )

        response = self.get_response(request)

        self.bind_user_id(request)

        structlog.contextvars.clear_contextvars()
        return response

    @staticmethod
    def bind_user_id(request: HttpRequest) -> None:
        if hasattr(request, "user") and request.user is not None:
            user_id = None
            if hasattr(request.user, "pk"):
                user_id = request.user.pk
                if isinstance(user_id, uuid.UUID):
                    user_id = str(user_id)
            structlog.contextvars.bind_contextvars(user_id=user_id)
