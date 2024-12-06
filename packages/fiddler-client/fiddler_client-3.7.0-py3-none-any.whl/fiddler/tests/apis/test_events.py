from pathlib import Path
from uuid import uuid4
import re

import numpy as np
import pandas as pd
import responses
import requests

from fiddler.constants.dataset import EnvType
from fiddler.entities.job import Job
from fiddler.entities.model import Model
from fiddler.tests.apis.test_files import SINGLE_UPLOAD_200_RESPONSE
from fiddler.tests.apis.test_model import API_RESPONSE_200 as MODEL_API_RESPONSE_200
from fiddler.tests.constants import JOB_ID, MODEL_ID, URL

FILE_PUBLISH_202_API_RESPONSE = {
    'data': {
        'source_type': 'FILE',
        'job': {'id': JOB_ID, 'name': 'Upload dataset'},
    },
    'api_version': '3.0',
    'kind': 'NORMAL',
}

PUBLISH_JOB_RESPONSE = {
    'data': {
        'id': 'e5784edf-2361-43e1-b67f-3dec90039d9b',
        'name': 'Publish events',
        'info': {
            'env_name': 'production',
            'env_type': 'PRODUCTION',
            'model_name': 'bank_churn',
            'model_uuid': 'd30bc065-a2ca-461e-bdcc-56d47c85d2a3',
            'project_name': 'test_project_5',
            'resource_name': 'bank_churn',
            'resource_type': 'EVENT',
            '__tracker_info': {
                'progress': 0,
                'error_reason': None,
                'error_message': None,
            },
        },
        'status': 'PENDING',
        'progress': 0,
        'error_message': None,
        'error_reason': None,
    },
    'api_version': '3.0',
    'kind': 'NORMAL',
}

df = pd.DataFrame(np.random.randint(0, 100, size=(10, 4)), columns=list('ABCD'))

STREAM_PUBLISH_202_API_RESPONSE = {
    'data': {
        'source_type': 'EVENTS',
        'event_ids': [str(uuid4()) for i in range(df.shape[0])],
    },
    'api_version': '3.0',
    'kind': 'NORMAL',
}

BASE_TEST_DIR = Path(__file__).resolve().parent.parent
FILE_PATH = BASE_TEST_DIR / 'artifact_test_dir' / 'model.yaml'


@responses.activate
def test_publish_file() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    responses.post(
        url=f'{URL}/v3/files/upload',
        json=SINGLE_UPLOAD_200_RESPONSE,
    )
    responses.get(
        url=f'{URL}/v3/jobs/{JOB_ID}',
        json=PUBLISH_JOB_RESPONSE,
    )

    responses.post(
        url=f'{URL}/v3/events',
        json=FILE_PUBLISH_202_API_RESPONSE,
    )
    publish_response = model.publish(
        source=FILE_PATH, environment=EnvType.PRE_PRODUCTION, dataset_name='dataset_1'
    )

    assert isinstance(publish_response, Job)

    FILE_PUBLISH_202_API_RESPONSE['data']['job']['name'] = 'Publish events'

    publish_response = model.publish(
        source=FILE_PATH, environment=EnvType.PRODUCTION, dataset_name='dataset_2'
    )

    assert isinstance(publish_response, Job)


@responses.activate
def test_publish_file_with_retry() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    # Note(JP): I want to make it really explicit that we inspect the request
    # body across retries, and that we require the main payload (file contents)
    # to be in the request body. This is a regression test, we one did not
    # persist the req body across retries:
    # https://github.com/fiddler-labs/fiddler/issues/9677
    def _custom_body_matcher(r: requests.PreparedRequest) -> tuple[bool, str]:
        needle = b'name: Iris Species Classification'
        if needle in r.body:
            return True, 'good'
        return False, f'not found in request body: {needle}, body: {r.body}'

    # Prepare three retryable error responses.
    for _ in range(3):
        responses.post(
            url=f'{URL}/v3/files/upload',
            status=500,
            body='dummy err to cover retrying logic',
            match=[
                responses.matchers.header_matcher(
                    {'Content-Type': re.compile(r'multipart/form-data;.*')}
                ),
                _custom_body_matcher,
            ],
        )

    # Let the fourth request emitted by the client be responded with with the
    # expected response, and verify once again that the request contains the
    # file payload.
    responses.post(
        url=f'{URL}/v3/files/upload',
        json=SINGLE_UPLOAD_200_RESPONSE,
        match=[
            responses.matchers.header_matcher(
                {'Content-Type': re.compile(r'multipart/form-data;.*')}
            ),
            _custom_body_matcher,
        ],
    )
    responses.get(
        url=f'{URL}/v3/jobs/{JOB_ID}',
        json=PUBLISH_JOB_RESPONSE,
    )

    responses.post(
        url=f'{URL}/v3/events',
        json=FILE_PUBLISH_202_API_RESPONSE,
    )
    publish_response = model.publish(
        source=FILE_PATH, environment=EnvType.PRE_PRODUCTION, dataset_name='dataset_1'
    )

    assert isinstance(publish_response, Job)


@responses.activate
def test_publish_df() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    responses.post(
        url=f'{URL}/v3/files/upload',
        json=SINGLE_UPLOAD_200_RESPONSE,
    )
    responses.get(
        url=f'{URL}/v3/jobs/{JOB_ID}',
        json=PUBLISH_JOB_RESPONSE,
    )

    responses.post(
        url=f'{URL}/v3/events',
        json=FILE_PUBLISH_202_API_RESPONSE,
    )
    publish_response = model.publish(
        source=df, environment=EnvType.PRE_PRODUCTION, dataset_name='dataset_1'
    )

    assert isinstance(publish_response, Job)

    FILE_PUBLISH_202_API_RESPONSE['data']['job']['name'] = 'Publish events'

    publish_response = model.publish(
        source=df,
        environment=EnvType.PRODUCTION,
    )

    assert isinstance(publish_response, Job)

    FILE_PUBLISH_202_API_RESPONSE['data']['job']['name'] = 'Publish events'


@responses.activate
def test_publish_stream() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    responses.post(
        url=f'{URL}/v3/events',
        json=STREAM_PUBLISH_202_API_RESPONSE,
    )

    publish_response = model.publish(
        source=df.to_dict('records'),
        environment=EnvType.PRODUCTION,
    )

    assert isinstance(publish_response, list)
    assert len(publish_response) == df.shape[0]


@responses.activate
def test_publish_update() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    responses.post(
        url=f'{URL}/v3/files/upload',
        json=SINGLE_UPLOAD_200_RESPONSE,
    )
    responses.get(
        url=f'{URL}/v3/jobs/{JOB_ID}',
        json=PUBLISH_JOB_RESPONSE,
    )

    responses.patch(
        url=f'{URL}/v3/events',
        json=FILE_PUBLISH_202_API_RESPONSE,
    )
    publish_response = model.publish(
        source=FILE_PATH,
        environment=EnvType.PRODUCTION,
        dataset_name='dataset_1',
        update=True,
    )

    assert isinstance(publish_response, Job)

    publish_response = model.publish(
        source=df, environment=EnvType.PRODUCTION, update=True
    )
    assert isinstance(publish_response, Job)
