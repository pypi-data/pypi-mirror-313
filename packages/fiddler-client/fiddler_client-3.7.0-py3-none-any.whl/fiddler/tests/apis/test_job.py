from http import HTTPStatus

import pytest
import responses

from fiddler.entities.job import Job
from fiddler.exceptions import NotFound
from fiddler.tests.constants import JOB_ID, JOB_NAME, URL

API_RESPONSE_200 = {
    'api_version': '3.0',
    'kind': 'NORMAL',
    'data': {
        'name': JOB_NAME,
        'info': {
            'resource_type': 'MODEL',
            'resource_name': 'bank_churn',
            'project_name': 'bank_churn',
        },
        'id': JOB_ID,
        'status': 'SUCCESS',
        'progress': 100,
        'error_message': None,
        'error_reason': None,
        'extras': {
            'e36d1cf2-766f-4705-8269-b6f93bf1ca14': {
                'status': 'SUCCESS',
                'result': {'result': 'Success'},
                'error_message': None,
            }
        },
    },
}

API_RESPONSE_404 = {
    'error': {
        'code': 404,
        'message': 'Job not found for the given identifier',
        'errors': [
            {
                'reason': 'ObjectNotFound',
                'message': 'Job not found for the given identifier',
                'help': '',
            }
        ],
    }
}


@responses.activate
def test_get_job_success() -> None:
    responses.get(
        url=f'{URL}/v3/jobs/{JOB_ID}',
        json=API_RESPONSE_200,
    )

    job = Job.get(id_=JOB_ID)
    assert isinstance(job, Job)


@responses.activate
def test_get_job_not_found() -> None:
    responses.get(
        url=f'{URL}/v3/jobs/{JOB_ID}',
        json=API_RESPONSE_404,
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(NotFound):
        Job.get(id_=JOB_ID)


@responses.activate
def test_get_watch_job_success() -> None:
    responses.get(
        url=f'{URL}/v3/jobs/{JOB_ID}',
        json=API_RESPONSE_200,
    )

    job = Job.get(id_=JOB_ID)
    job_watch = job.watch()
    assert isinstance(list(job_watch)[0], Job)
