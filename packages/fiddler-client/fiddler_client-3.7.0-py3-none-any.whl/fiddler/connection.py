from __future__ import annotations

import logging
from functools import cached_property
from uuid import UUID

import fiddler.utils.logger
from fiddler.configs import MIN_SERVER_VERSION
from fiddler.constants.common import (
    CLIENT_NAME,
    FIDDLER_CLIENT_NAME_HEADER,
    FIDDLER_CLIENT_VERSION_HEADER,
)
from fiddler.decorators import handle_api_error
from fiddler.exceptions import IncompatibleClient
from fiddler.libs.http_client import RequestClient
from fiddler.schemas.server_info import ServerInfo, Version
from fiddler.utils.version import match_semver
from fiddler.version import __version__

log = logging.getLogger(__name__)


class Connection:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        url: str,
        token: str,
        proxies: dict | None = None,
        timeout: float | tuple[float, float] | None = None,
        verify: bool = True,
        validate: bool = True,
    ) -> None:
        """
        Initiate connection.

        :param url:
            The base URL to your Fiddler platform.
        :param token:
            An authentication token, obtained via the Fiddler UI.
        :param proxies:
            A dictionary mapping protocol to the URL of the proxy.
        :param timeout:
            Allows for overriding default HTTP request timeout settings.
            Applies to all HTTP requests emitted with this connection object.
            Can be a float or two floats, also see
            https://requests.readthedocs.io/en/latest/user/advanced/#timeouts
        :param verify:
            Can be used to disable server's TLS certificate verification.
            Certificate verification is enabled by default.
        :param validate:
            Whether to validate the server/client version compatibility. Some
            features might not work as expected if this is turned off.
        """

        self.url = url
        self.token = token
        self.proxies = proxies
        self.timeout = timeout
        self.verify = verify

        if not url:
            raise ValueError('`url` is empty')

        if not token:
            raise ValueError('`token` is empty')

        self.request_headers = {
            'Authorization': f'Bearer {token}',
            FIDDLER_CLIENT_NAME_HEADER: CLIENT_NAME,
            FIDDLER_CLIENT_VERSION_HEADER: __version__,
        }

        if validate:
            self._check_server_version()
            self._check_version_compatibility()

    @cached_property
    def client(self) -> RequestClient:
        """Request client instance"""
        return RequestClient(
            base_url=self.url,
            headers=self.request_headers,
            proxies=self.proxies,
            verify=self.verify,
        )

    @cached_property
    def server_info(self) -> ServerInfo:
        """Server info instance"""
        return self._get_server_info()

    @cached_property
    def server_version(self) -> Version:
        """Server semver version"""
        return self.server_info.server_version

    @cached_property
    def organization_name(self) -> str:
        """Organization name"""
        return self.server_info.organization.name

    @cached_property
    def organization_id(self) -> UUID:
        """Organization id"""
        return self.server_info.organization.id

    @handle_api_error
    def _get_server_info(self) -> ServerInfo:
        """Get server info"""

        # Tight-ish timeout.
        response = self.client.get(url='/v3/server-info', timeout=(5, 15))

        return ServerInfo(**response.json().get('data'))

    @handle_api_error
    def _check_version_compatibility(self) -> None:
        """Check whether Client version is compatible with Fiddler Platform version"""

        self.client.get(
            url='/v3/version-compatibility',
            params={
                'client_version': __version__,
                'client_name': CLIENT_NAME,
            },
            timeout=(5, 15),
        )

    def _check_server_version(self) -> None:
        """Check whether Fiddler Platform version is compatible with Client version"""
        if match_semver(self.server_version, f'>={MIN_SERVER_VERSION}'):
            return

        raise IncompatibleClient(server_version=str(self.server_version))


class ConnectionMixin:
    @classmethod
    def _conn(cls) -> Connection:
        """Fiddler connection instance"""
        from fiddler import conn  # pylint: disable=import-outside-toplevel

        assert conn is not None
        return conn

    @classmethod
    def _client(cls) -> RequestClient:
        """Request client instance"""
        return cls._conn().client

    @property
    def organization_name(self) -> str:
        """Organization name property"""
        return self._conn().server_info.organization.name

    @property
    def organization_id(self) -> UUID:
        """Organization id property"""
        return self._conn().server_info.organization.id

    @classmethod
    def get_organization_name(cls) -> str:
        """Organization name"""
        return cls._conn().server_info.organization.name

    @classmethod
    def get_organization_id(cls) -> UUID:
        """Organization id"""
        return cls._conn().server_info.organization.id


def init(  # pylint: disable=too-many-arguments
    url: str,
    token: str,
    proxies: dict | None = None,
    timeout: float | tuple[float, float] | None = None,
    verify: bool = True,
    validate: bool = True,
    auto_attach_log_handler: bool = True,
) -> None:
    """
    Initialize the client.

    :param url:
        The base URL to your Fiddler platform.
    :param token:
        An authentication token, obtained via the Fiddler UI (can be found on
        the Credentials tab of the Settings page).
    :param proxies:
        A dictionary mapping protocol to the URL of the proxy.
    :param timeout:
        Allows for overriding default HTTP request timeout settings. Applies to
        all HTTP requests emitted by this client. Can be a float or two floats,
        also see
        https://requests.readthedocs.io/en/latest/user/advanced/#timeouts. This
        client library tries to implement meaningful default timeout settings.
        If you find yourself having to set this parameter to address a problem
        please also contact the Fiddler customer support.
    :param verify:
        Can be used to disable server's TLS certificate verification.
        Certificate verification is enabled by default.
    :param validate:
        Whether to validate the server/client version compatibility. Some
        features might not work as expected if this is turned off.
    :param auto_attach_log_handler:
        Defaults to `True`. Can be used to disable the mechanism by which this
        library may attach a stream handler for emitting log messages to stderr
        (see below for further details).


    The Fiddler client library will see HTTP API calls fail due to for example
    transient networking issues, temporary backend problems, or as of rate
    limiting errors. These kinds of failures are retryable. It is a sensible
    choice to retry any affected API call after a short waiting period.
    Therefore, this client library implements an automatic retry strategy. Most
    HTTP requests are retried for up to certain amount of time.

    You can take control of this maximum retry duration by setting the
    environment variable `FIDDLER_CLIENT_RETRY_MAX_DURATION_SECONDS` to a
    numeric value. It currently defaults to 300 seconds which allows for
    auto-healing smaller outages.

    Note that this client library logs HTTP interaction (and retrying details)
    on INFO level via Python's standard library logging module under the
    'fiddler' namespace.

    If you do not configure a root logger in your Python interpreter context
    (done via e.g. `logging.basicConfig()`) then this library automatically
    attaches a handler for its log messages to be emitted on `stderr`. This
    behavior can be disabled by setting `auto_attach_log_handler=False`. For
    fine-grained control, consider configuring handlers and formatters
    yourself.

    The Fiddler client library has AWS SageMaker partner application
    authentication support. To enable that, install the SageMaker Python SDK
    (`sagemaker` on PyPI). Then, before calling `fiddler.init()` set the
    environment variable AWS_PARTNER_APP_AUTH to 'true' and also set
    AWS_PARTNER_APP_ARN/AWS_PARTNER_APP_URL to meaningful values.
    """
    from fiddler import _set_conn  # pylint: disable=import-outside-toplevel

    # If this library is imported into an interpreter that has a root logger
    # configured (with handler(s) attached) then just propagate log messages
    # into that hierarchy, and do not attach a handler to the 'fiddler' logger.
    if not logging.getLogger().handlers and auto_attach_log_handler:
        fiddler.utils.logger._attach_handler()
        log.info(
            'attached stderr handler to logger: auto_attach_log_handler=True, and root logger not configured'
        )

    # Singleton object in Python interpreter.
    conn = Connection(
        url=url,
        token=token,
        proxies=proxies,
        timeout=timeout,
        verify=verify,
        validate=validate,
    )

    _set_conn(conn_=conn)
