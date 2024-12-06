from __future__ import annotations

import os
import logging
import time
from copy import deepcopy
from typing import Any
from urllib.parse import urljoin

import requests
import simplejson
from requests.adapters import HTTPAdapter

import fiddler.libs.aws
from fiddler.exceptions import BaseError  # pylint: disable=redefined-builtin
from fiddler.libs.json_encoder import RequestClientJSONEncoder


log = logging.getLogger(__name__)

# A shortcut.
timer = time.monotonic


class RequestClient:
    def __init__(
        self,
        base_url: str,
        headers: dict[str, str],
        verify: bool = True,
        proxies: dict | None = None,
        timeout_override: float | tuple[float, float] | None = None,
    ) -> None:
        """
        HTTP client abstraction.

        For centralized logging and retrying and error handling.
        """

        # Note(JP): the retry mechanism keeps retrying an individual HTTP
        # request until a deadline is reached N seconds into the future after
        # starting the request.
        #
        # This retry mechanism is supposed to allow for  transparently
        # surviving micro outages, i.e. this time constant is meant to be O(1
        # min) up to O(1 h) depending on the use case. For example, a CI use
        # case (say, unattended nightly job) might reasonably want to retry for
        # a very long time, whereas in an interactive session or notebook the
        # retrying mechanism should probably give up after a minute or three.
        #
        # A default value being tuned for either extreme case is maybe not the
        # best. Therefore pick something inbetween (5 minutes). In CI, we can
        # then opt for increasing this. In my personal experience using client
        # libraries like the one that we use here I have always appreciated a
        # certain tendency of being optimized for _automated jobs_, i.e. CI
        # scenarios.
        self._retry_max_duration_seconds = 300.0
        self._retry_max_duration_from_env()

        # As documented, this can be overridden with an environment variable.
        # (once we like the interface we can also expose this with a function
        # argument).
        self._timeout_long_running_requests = (5, 100)
        self._timeout_override = timeout_override
        # Not yet in use.
        # self.timeout_short_running_requests = (5, 15)

        self.base_url = base_url
        self.proxies = proxies

        # Think: default headers, added to each request, if not overwritten
        # more locally.
        assert isinstance(headers, dict)
        self._default_headers = headers

        self.session = requests.Session()

        # Note(JP): this is doing conditional runtime modification for AWS
        # Hadron / SageMaker, depending on
        # - environment variables set by the user
        # - importability of the AWS sagemaker Python SDK TODO: type annotation
        # w/o having to import PartnerAppAuthProvider? This thing is either
        # None or an instantiated auth provider.
        # Previously we did this only once during import. We found that it's
        # better to have this functionality executed during `fiddler.init()`.
        aws_sm_auth_provider = fiddler.libs.aws.conditionally_init_aws_sm_auth()  # type: ignore

        # Note(JP): from the AWS SageMaker partner app guide.
        if aws_sm_auth_provider is not None:
            # Get callback class (`RequestsAuth` type`) from SM auth provider,
            # and decorate the `requests` session object with that. This is
            # enabling the magic of automatically mutating request headers.
            # Among others, this injects the SigV4 header.
            self.session.auth = aws_sm_auth_provider.get_auth()

        self.session.verify = verify
        adapter = HTTPAdapter(
            # Note(JP): what's the relevance of setting these?
            pool_connections=25,
            pool_maxsize=25,
        )

        # Does mounting the custom HTTP adapter revert the session.auth
        # change from above?
        self.session.mount(self.base_url, adapter)

    def _retry_max_duration_from_env(self) -> None:
        name = 'FIDDLER_CLIENT_RETRY_MAX_DURATION_SECONDS'
        v = os.environ.get(name, '')
        if v:
            try:
                dur = float(v.strip())
                log.info("applying environment variable '%s': %s", name, dur)
                self._retry_max_duration_seconds = dur
            except ValueError as exc:
                log.warning("ignore environment variable '%s': %s", name, exc)

    def _request_with_retry(
        self,
        *,
        method: str,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        data: dict | bytes | None = None,
        timeout: float | tuple[float, float] | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        """
        Emit HTTP request.

        Apply retry strategy, unless told not to.

        :param kwargs: passed on to requests.session.request()
        """
        headers_to_send = deepcopy(self._default_headers)

        # override/update headers coming from the calling method
        if headers:
            headers_to_send.update(headers)

        ct = headers_to_send.get('Content-Type')
        if isinstance(data, dict) and ct == 'application/json':
            # Note(JP): custom JSON-encoding -- after a bit of research, I
            # understand that we use simplejson mainly for its
            # `ignore_nan=True` behavior. Also see
            # https://bugs.python.org/issue40633 where we see how this was
            # _not_ added to stdlib json.dumps() yet. orjson also has this
            # capability. For stdlib JSON, this could be achieved with e.g.
            # https://stackoverflow.com/a/71389334 (or a modification thereof).
            # We do not strictly need simplejson here as a dependency: remove in
            # the future. But since we do have this custom serialization logic
            # here it's important to _not_ use the `json=` arg in the requests
            # lib, because under the hood this would use the stdlib JSON
            # encoder. This code path here is triggered when setting `data`
            # _and_ `headers={'Content-Type': 'application/json'}`,
            data = simplejson.dumps(
                data,
                ignore_nan=True,
                cls=RequestClientJSONEncoder,  # type: ignore
            )

        # `setdefault`: define a property in kwargs when the caller doesn't
        # specify it. verify: default to session config, but allow for
        # override.
        kwargs.setdefault('allow_redirects', True)
        kwargs.setdefault('verify', self.session.verify)

        # Parameters passed to session.request() with all parameters except for
        # method and URL.
        kwargs.update(
            {
                'params': params,
                'data': data,
                'headers': headers_to_send,
                'timeout': timeout,
                'proxies': self.proxies,
            }
        )

        return self._make_request_retry_until_deadline(
            method, urljoin(self.base_url, url), **kwargs
        )

    def _logpfx(self, method: str, url: str) -> str:
        return f'http: {url} {method} --'

    def _make_request_retry_until_deadline(
        self, method: str, url: str, **kwargs: Any
    ) -> requests.Response:
        """
        Return `requests.Response` object when the request was sent out and
        responded to with an HTTP response with a 2xx status code.

        Implement a retry loop with deadline control.

        Raise an exception derived from `requests.exceptions.RequestException`
        to indicate a non-retryable error, such as various 4xx responses.

        Raise `fiddler.exceptions.BaseError` (from last exception) when
        reaching the deadline (it might also raise a minute early, or even be
        briefly exceed the deadline depending on how robust timeout control
        is).
        """
        logpfx = self._logpfx(method, url)

        t0 = timer()
        deadline = t0 + self._retry_max_duration_seconds
        cycle: int = 0

        log.debug('%s try', logpfx)

        while timer() < deadline:
            cycle += 1

            # Inject a copy of `kwargs` so that the consuming function can
            # perform mutations at will without affecting subsequent retries.
            result = self._make_request_retry_guts(
                method,
                url,
                cycle,
                **deepcopy(kwargs),
            )

            if isinstance(result, requests.Response):
                if cycle > 1:
                    log.info(
                        '%s success after %.2f s (%s attempts)',
                        logpfx,
                        timer() - t0,
                        cycle,
                    )
                return result

            # Rename, for clarity. This exception was considered retryable, but
            # we may have to throw it below upon approaching the deadline.
            last_exception = result

            # Desired behavior: rather fast first retry attempt; followed by
            # slow exponential growth, and an upper bound: 0.66, 1.33, 2.66,
            # 5.33, 10.66, 21.33, 42.66, 60, 60, .... (seconds)
            wait_s = min((2**cycle) / 3.0, 60)
            deadline_in_s = deadline - timer()
            abort = (timer() + wait_s) > deadline  # would next wait exceed deadline?

            # Dynamically build up this log msg. Clumsy, but it's nice to have
            # all that detail about the intent captured correctly, especially
            # when debugging something unusual.
            msg = f'{logpfx} attempt {cycle} failed, '
            if deadline_in_s < 0:
                msg += f'deadline exceeded by {deadline_in_s/-60.0:.1f} min, '
            else:
                msg += f'deadline in {deadline_in_s/60.0:.1f} min, '

            if abort:
                msg += 'abort retrying'
            else:
                msg += f'retry in {wait_s:.2f} s'

            log.info(msg)

            if abort:
                break

            time.sleep(wait_s)

        # Give up after retrying. Structurally emit error detail of last seen
        # (retryable) exception (`raise from`), but also log the last error
        # message as part of the new exception message.
        raise BaseError(
            f'{method} {url}: giving up after {cycle} attempt(s) / {timer() - t0:.2f} s'
            + f', last error: {last_exception}'
        ) from last_exception

    def _make_request_retry_guts(
        self, method: str, url: str, attempt: int, **kwargs: Any
    ) -> requests.Response | requests.RequestException:
        """
        Return `requests.Response` object when the request was sent out and
        responded to with an HTTP response that does not throw upon
        `resp.raise_for_status()` (a 2xx status code).

        Return an exception object to indicate a _retryable_ error to the
        caller. The caller will then retry.

        Raise an exception derived from `requests.exceptions.RequestException`
        to indicate a non-retryable error, such as various 4xx responses.

        `attempt`: first attempt: 1, we're retrying for this to be >= 2.

        Deconstruct `kwargs` with every call, i.e. a caller should inject a new
        copy upon repeated invocation.
        """
        logpfx = self._logpfx(method, url)

        # Populate the `timeout` arg that is going to be passed into
        # the requests API. Docs:
        # https://requests.readthedocs.io/en/latest/user/advanced/#timeouts

        # By design, `kwargs['timeout']` always exists and it may be `None`
        # indicating default handling. Be a little defensive here w.r.t
        # KeyError.
        if kwargs.get('timeout', None) is None:
            # This code path means: the client call does not specify a timeout
            # via explicit param (which can be done via e.g.
            # `client.get(url="/v3/server-info", timeout=(5, 15))`. Make a
            # smart default choice depending on endpoint/method (TODO: this
            # logic below needs to be built):
            kwargs['timeout'] = self._timeout_long_running_requests

        # This is documented to take precedence, allowing for code calling into
        # this client to override our pretentious smartness.
        if self._timeout_override is not None:
            kwargs['timeout'] = self._timeout_override

        # Magic argument passed down to here. Can be set to "off".
        retry_strategy = kwargs.pop('retry', 'default')

        # Prepare request before sending it. That allows for e.g. inspecting
        # the request size before sending. Explicitly pass all allowed
        # parameters as documented at
        # https://requests.readthedocs.io/en/latest/api/#lower-level-classes:
        # requests.Request(method=None, url=None, headers=None, files=None,
        # data=None, params=None, auth=None, cookies=None, hooks=None,
        # json=None). That is, deconstruct `kwargs` so that only those
        # arguments in `kwargs` remain that can further below passed into
        # request.send().

        headers = kwargs.pop('headers')  # this is always set in kwargs!
        if attempt > 1:
            # Let the backend know that this an automatically emitted retry (it
            # can use this to do a little more strict conflict detection).
            # Semantically, the number here should really mean retry, i.e.
            # the second attempt is the first retry.
            headers['X-Fiddler-Client-Retry'] = str(attempt - 1)

        # Use session.prepared_request() so that session.auth and adapter's
        # mounted on session apply.
        req = self.session.prepare_request(
            requests.Request(
                method=method,
                url=url,
                headers=headers,
                files=kwargs.pop('files', None),
                data=kwargs.pop('data', None),
                params=kwargs.pop('params', None),
                auth=kwargs.pop('auth', None),
                cookies=kwargs.pop('cookies', None),
                hooks=kwargs.pop('hooks', None),
                json=kwargs.pop('json', None),
            )
        )

        reqsize_bytes = 0 if req.body is None else len(req.body)
        reqsize_str = f'{reqsize_bytes/(1024.0**2):.3f} MB'
        if reqsize_bytes < 10000:
            reqsize_str = f'{reqsize_bytes} B'

        log.info(
            '%s emit req (%s, timeout: %s)',
            logpfx,
            reqsize_str,
            kwargs['timeout'],
        )

        log.debug('request headers: %s', req.headers)

        t0 = timer()
        try:
            # Here, we want to have a tight TCP connect() timeout and a
            # meaningful TCP recv timeout, also a meaningful global
            # request-response cycle timeout (accounting for the ~expected HTTP
            # request processing time in the API implementation, plus leeway).
            # Here's an example of session.send() args:
            # https://github.com/psf/requests/blob/v2.32.3/src/requests/sessions.py#L265
            resp = self.session.send(req, **kwargs)
        except requests.exceptions.RequestException as exc:
            if retry_strategy == 'off':
                log.info('%s error after %.1f s: %s', logpfx, timer() - t0, exc)
                # Do not retry, let the caller deal with this exception.
                raise

            # Note(JP): we did not get a response. We might not even have sent
            # the request. An error happened before sending the request, while
            # sending the request, while waiting for response, or while
            # receiving the response. High probability for this being a
            # transient problem. A few examples for errors handled here:
            #
            # - DNS resolution error
            # - TCP connect() timeout
            # - Connection refused during TCP connect()
            # - Timeout while waiting for the other end to start sending the
            #   HTTP response (after having sent the request).
            # - RECV timeout between trying to receive two response bytes.
            #
            # Note(JP): do this, regardless of the type of request that we
            # sent. I know we've expressed concerns about idempotency here and
            # there. But I believe that it will be a big step forward to have
            # more or less *easy-to-reason-about* retrying in the client and to
            # maybe risk a rare idempotency problem and debug it and fix it in
            # the backend.

            # Convention: returning the exception tells the caller to retry.
            log.info(
                '%s retryable error after %.1f s: %s',
                logpfx,
                timer() - t0,
                exc,
            )
            return exc

        # Got an HTTP response. In the scope below, `resp` reflects that.

        # This property is documented as bytes, should always exist.
        respsize_bytes = len(resp.content)
        respsize_str = f'{respsize_bytes/(1024.0**2):.3f} MB'
        if respsize_bytes < 10000:
            respsize_str = f'{respsize_bytes} B'

        log.info(
            '%s resp code: %s, took %.3f s, resp/req body size: (%s, %s)',
            logpfx,
            resp.status_code,
            timer() - t0,
            respsize_str,
            reqsize_str,
        )

        try:
            resp.raise_for_status()

            # The criterion for a good-looking response. Ideally we check for
            # the _precisely_ expected status code, but can do that later.
            return resp
        except requests.HTTPError as exc:
            # Decide whether or not this is a retryable based on the response
            # details. Put into a log message before leaving this function.
            treat_retryable = self._is_retryable_resp(resp)

            # Log body prefix: sometimes this is critical for debuggability.
            log.warning(
                '%s error response with code %s%s, body bytes: <%s%s>',
                logpfx,
                resp.status_code,
                ' (treat retryable)' if treat_retryable else ' (not retryable)',
                resp.text[:500],
                '...' if len(resp.text) > 500 else '',
            )

            if retry_strategy == 'off':
                raise

            if treat_retryable:
                return exc

            # Otherwise let this (valuable) requests.HTTPError object bubble up
            # to calling code. This is the expected code path for most 4xx
            # error responses. Before that, for facilitating debugging, log
            # request details.
            log.info(
                'bad request details:\nheaders:\n%s\nbody[:200]:  "%s"',
                req.headers,
                repr(req.body[:200]) if req.body else '',
            )
            raise

    def _is_retryable_resp(self, resp: requests.Response) -> bool:
        """
        Do we (want to) consider this response as retryable, based on the
        status code alone?
        """
        if resp.status_code == 429:
            # Canonical way to signal "back off, retry soon".
            return True

        if resp.status_code == 501:
            # Note(JP): this means  "not implemented" or "not supported". Per
            # HTTP spec, this is still meant to be retryable (in the spirit of
            # all 5xx errors). In our context, however, we seem to use it to
            # indicate some permanent (non-retryable) errors. Do not retry
            # those for now, in general. We should move away from emitting 501
            # from the backend.
            return False

        # Retry any 5xx response, later maybe fine-tune this by specific status
        # code. Certain 500 Internal Server Error are probably permanent, but
        # it's worth retrying them, too.
        if str(resp.status_code).startswith('5'):
            return True

        return False

    def get(
        self,
        *,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        timeout: float | tuple[float, float] | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        return self._request_with_retry(
            method='GET',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    def delete(
        self,
        *,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        timeout: int | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        return self._request_with_retry(
            method='DELETE',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    def post(
        self,
        *,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        timeout: int | None = None,
        data: dict | bytes | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        return self._request_with_retry(
            method='POST',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            data=data,
            **kwargs,
        )

    def put(
        self,
        *,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        timeout: int | None = None,
        data: dict | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        return self._request_with_retry(
            method='PUT',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            data=data,
            **kwargs,
        )

    def patch(
        self,
        *,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        timeout: int | None = None,
        data: dict | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        return self._request_with_retry(
            method='PATCH',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            data=data,
            **kwargs,
        )
