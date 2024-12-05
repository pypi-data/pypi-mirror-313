from functools import wraps

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http.request import split_domain_port
from django.http.response import Http404

from payla_utils.settings import payla_utils_settings


def only_internal_access(view_func):
    """
    Decorator for views that checks that the endpoint is only accessible via the direct IP Address.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        domain, __ = split_domain_port(request.get_host())
        server_ip = payla_utils_settings.SERVER_IP
        if not server_ip:
            raise Exception('SERVER_IP is required in order to use only_internal_access decorator')
        if domain == server_ip:
            return view_func(request, *args, **kwargs)
        raise Http404('Not found')

    return _wrapped_view


def staff_member_required_or_local_dev(
    view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url="admin:login"
):
    """
    Same as staff member required but allows local development
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if settings.ENVIRONMENT == "local.dev":
            return view_func(request, *args, **kwargs)
        return staff_member_required(redirect_field_name=redirect_field_name, login_url=login_url)(view_func)(
            request, *args, **kwargs
        )

    return _wrapped_view
