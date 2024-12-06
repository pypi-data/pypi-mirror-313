from __future__ import annotations

import logging
import time
from typing import Iterator
from uuid import UUID

import requests

from fiddler.configs import JOB_POLL_INTERVAL, JOB_WAIT_TIMEOUT
from fiddler.constants.job import JobStatus
from fiddler.decorators import handle_api_error
from fiddler.entities.base import BaseEntity
from fiddler.exceptions import AsyncJobFailed
from fiddler.schemas.job import JobResp


logger = logging.getLogger(__name__)


class Job(BaseEntity):  # pylint: disable=too-many-instance-attributes
    def __init__(self) -> None:
        """Construct a job instance"""
        self.name: str | None = None
        self.status: str | None = None
        self.progress: float | None = None
        self.info: dict | None = None
        self.error_message: str | None = None
        self.error_reason: str | None = None
        self.extras: dict | None = None

        self.id: UUID | None = None

        # Deserialized response object
        self._resp: JobResp | None = None

    @classmethod
    def _from_dict(cls, data: dict) -> Job:
        """Build entity object from the given dictionary"""

        # Deserialize the response
        resp_obj = JobResp(**data)

        # Initialize
        instance = cls()

        # Add remaining fields
        fields = [
            'id',
            'name',
            'progress',
            'status',
            'info',
            'error_message',
            'error_reason',
            'extras',
        ]
        for field in fields:
            setattr(instance, field, getattr(resp_obj, field, None))

        instance._resp = resp_obj

        return instance

    def _refresh(self, data: dict) -> None:
        """Refresh the fields of this instance from the given response dictionary"""
        # Deserialize the response
        resp_obj = JobResp(**data)

        # Add remaining fields
        fields = [
            'id',
            'name',
            'progress',
            'status',
            'info',
            'error_message',
            'error_reason',
            'extras',
        ]
        for field in fields:
            setattr(self, field, getattr(resp_obj, field, None))

        self._resp = resp_obj

    @staticmethod
    def _get_url(id_: UUID | str | None = None) -> str:
        """Get job resource/item url"""
        url = '/v3/jobs'
        return url if not id_ else f'{url}/{id_}'

    @classmethod
    @handle_api_error
    def get(cls, id_: UUID | str, verbose: bool = False) -> Job:
        """
        Get the job instance using job id

        :param id_: Unique identifier of the job
        :param verbose: flag to get extra details about the tasks executed
        :return: single job object for the input params
        """
        response = cls._client().get(
            url=cls._get_url(id_=id_), params={'verbose': verbose}
        )
        return cls._from_response(response=response)

    def watch(
        self, interval: int = JOB_POLL_INTERVAL, timeout: int = JOB_WAIT_TIMEOUT
    ) -> Iterator[Job]:
        """
        Watch job status at given interval and yield job object

        :param interval: Interval in seconds between polling for job status
        :param timeout: Timeout in seconds for iterator to stop.
        :return: Iterator of job objects
        """
        assert self.id is not None
        deadline = time.monotonic() + timeout

        while True:
            if time.monotonic() > deadline:
                raise TimeoutError(f'Deadline exceeded while watching job {self.id}')

            try:
                # This can raise requests.HTTPError to represent non-2xx
                # responses.
                response = self._client().get(
                    url=self._get_url(id_=self.id),
                    # Short-ish TCP connect timeout, to stay responsive in
                    # terms of logging. The HTTP response latency for GET
                    # /jobs/<id> is expected to be less than couple of seconds
                    # (i.e., 30 s includes lots of  leeway).
                    timeout=(5, 30),
                    # Inject `retry="off"` to disable the centralized retry
                    # machinery: ask for being confronted with the details
                    # (throw exceptions my way, so I an do my own "responsive"
                    # type of retrying). Otherwise, we'd give up control.
                    retry='off',
                )
                self._refresh_from_response(response)

            except requests.exceptions.HTTPError as exc:
                # Note(JP): got a non-2xx HTTP response. The main purpose of
                # this handler is to keep going after having received a 5xx
                # response. In this case of GETting job status even some 404s
                # might be worth retrying. That is, it's fine to give up only
                # after reaching the deadline even if we collect some 4xx
                # responses along the way. Noteworthy: Receiving a 5xx response
                # here is not an error, it's an expected scenario to be
                # accounted for.
                logger.info(
                    'watch: ignore unexpected response %s (URL: %s, response body prefix: %s...)',
                    exc.response,
                    exc.request.url,
                    exc.response.text[:120],
                )
                continue

            except requests.exceptions.RequestException:
                # This error is in the hierarchy _above_ `HTTPError`, and in
                # this setup catches all errors that are _not_ a bad response:
                # DNS error, TCP connect timeout, err during sending request,
                # err during receiving response. Rely on the error detail to
                # have already been logged.
                continue

            yield self

            if self.status in [
                JobStatus.SUCCESS,
                JobStatus.FAILURE,
                JobStatus.REVOKED,
            ]:
                return

            time.sleep(interval)

    def wait(
        self, interval: int = JOB_POLL_INTERVAL, timeout: int = JOB_WAIT_TIMEOUT
    ) -> None:
        """
        Wait for job to complete either with success or failure status

        :param interval: Interval in seconds between polling for job status
        :param timeout: Timeout in seconds for iterator to stop.
        """
        log_prefix = f'{self.name}[{self.id}]'

        for job in self.watch(interval=interval, timeout=timeout):
            logger.info(
                '%s: %s, progress: %.1f%%',
                log_prefix,
                job.status,
                job.progress,
            )

            if job.status == JobStatus.SUCCESS:
                logger.info('%s: successfully completed', log_prefix)
            elif job.status == JobStatus.FAILURE:
                raise AsyncJobFailed(
                    f'{log_prefix} failed with {job.error_reason or "Exception"}: '
                    f'{job.error_message}'
                )
