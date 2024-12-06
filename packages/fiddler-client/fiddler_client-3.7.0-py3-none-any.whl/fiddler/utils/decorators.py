from functools import wraps
from typing import Any, Callable, no_type_check  # noqa: F401

from fiddler import Connection
from fiddler.exceptions import IncompatibleClient
from fiddler.utils.version import match_semver


def check_version(version_expr: str) -> Callable:
    """
    Check version_expr against server version before making an API call

    Usage:
        @check_version(version_expr=">=23.1.0")
        @handle_api_error_response
        def get_model_deployment(...):
            ...

    Add this decorator on top of other decorators to make sure version check happens
    before doing any other work.

    :param version_expr: Supported version to match with. Read more at VersionInfo.match
    :return: Decorator function
    """

    @no_type_check
    def decorator(func) -> Callable:
        @wraps(func)
        def wrapper(self, *args: Any, **kwargs: Any) -> Any:
            server_version = (
                self._conn().server_version
                if not isinstance(self, Connection)
                else self.server_version
            )

            if not match_semver(server_version, version_expr):
                raise IncompatibleClient(
                    server_version=server_version,
                    message=f'{func.__name__} method is supported with server version '
                    f'{version_expr}, but the current server version is '
                    f'{server_version}',
                )

            return func(self, *args, **kwargs)

        return wrapper

    return decorator
