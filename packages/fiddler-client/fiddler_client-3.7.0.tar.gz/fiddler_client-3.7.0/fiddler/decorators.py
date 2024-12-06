from functools import wraps
from http import HTTPStatus
import logging
from typing import Any, Callable, TypeVar, cast

import requests
import pydantic.v1

from fiddler.exceptions import ApiError, Conflict, HttpError, NotFound, Unsupported
from fiddler.schemas.response import ErrorResponse


logger = logging.getLogger(__name__)

_WrappedFuncType = TypeVar(  # pylint: disable=invalid-name
    '_WrappedFuncType', bound=Callable[..., Any]
)


# ignore: fiddler/decorators.py:19:1: C901 'handle_api_error' is too complex (11)
def handle_api_error(func: _WrappedFuncType) -> _WrappedFuncType:  # noqa: C901
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except requests.JSONDecodeError as e:
            # This often is premature use of `json()`. Calling code should
            # first check the response for the expected status code, and only
            # then attempt JSON-deserialization.
            raise HttpError(message=f'Invalid JSON response - {e.doc}')  # type: ignore
        except requests.HTTPError as http_exc:
            # Note(JP): when we're here it means we got an HTTP response.
            # That's how this exception is documented.

            status = http_exc.response.status_code
            # The logging levels 'critical' and 'error' are generally meant to
            # be used for terminal / fatal errors. Here, we handle many
            # transient (retryable) errors, and it's fair to log them not as
            # serious as actual errors. Therefore level WARNING and not ERROR.
            # Even INFO might make sense.
            logger.warning(
                '%s HTTP request to %s failed with %s - %s',
                http_exc.request.method,
                getattr(http_exc.request, 'url', 'unknown'),
                status,
                # Not entire response body in case we have a megabyte response.
                getattr(http_exc.response, 'content', 'missing')[:200],
            )

            # Now, map the error at hand to an exception to be thrown towards
            # the caller.

            if status == HTTPStatus.METHOD_NOT_ALLOWED:
                raise Unsupported()

            # Did we get structured error information? This might even
            # be wrapped in a 501 response for example.
            try:
                # https://github.com/fiddler-labs/fiddler/issues/9314
                error_resp = ErrorResponse(**http_exc.response.json())
            except pydantic.v1.ValidationError:
                # We couldn't turn the HTTP error response into an object
                # satisfying model='ErrorResponse'. Now, instead of exposing
                # this to users as a pydantic.ValidationError (which is kinda
                # useless to them) -- just re-raise requests.HTTPError, with
                # all its useful error detail -- it is likely to show the
                # actual problem.
                raise http_exc
            except requests.JSONDecodeError:
                # Re-raise requests.HTTPError, with all its useful error
                # detail.
                raise http_exc

            # This code path is only reachable if we could successfully
            # deserialize an ErrorResponse object from the HTTP response body.

            if status == HTTPStatus.CONFLICT:
                raise Conflict(error_resp.error)

            if status == HTTPStatus.NOT_FOUND:
                raise NotFound(error_resp.error)

            raise ApiError(error_resp.error)

    return cast(_WrappedFuncType, wrapper)
