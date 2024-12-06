from http import HTTPStatus

import pytest
import responses

from fiddler.entities.job import Job
from fiddler.entities.model_deployment import ModelDeployment
from fiddler.exceptions import NotFound
from fiddler.tests.constants import (
    JOB_ID,
    JOB_NAME,
    MODEL_DEPLOYMENT_ID,
    MODEL_ID,
    MODEL_NAME,
    ORG_ID,
    ORG_NAME,
    PROJECT_ID,
    PROJECT_NAME,
    URL,
    USER_EMAIL,
    USER_ID,
    USER_NAME,
)

API_RESPONSE_200 = {
    'data': {
        'id': MODEL_DEPLOYMENT_ID,
        'model': {'id': MODEL_ID, 'name': MODEL_NAME},
        'project': {
            'id': PROJECT_ID,
            'name': PROJECT_NAME,
        },
        'organization': {
            'id': ORG_ID,
            'name': ORG_NAME,
        },
        'artifact_type': 'SURROGATE',
        'deployment_type': 'BASE_CONTAINER',
        'active': True,
        'image_uri': '',
        'replicas': 1,
        'cpu': 300,
        'memory': 100,
        'created_at': '2023-11-22 16:50:57.705784',
        'updated_at': '2023-11-22 16:50:57.705784',
        'created_by': {
            'id': USER_ID,
            'full_name': USER_NAME,
            'email': USER_EMAIL,
        },
        'updated_by': {
            'id': USER_ID,
            'full_name': USER_NAME,
            'email': USER_EMAIL,
        },
        'job': {'id': JOB_ID, 'name': 'Deploy artifact model - manual'},
    },
}

API_RESPONSE_404 = {
    'error': {
        'code': 404,
        'message': 'Model deployment not found for the given identifier',
        'errors': [
            {
                'reason': 'ObjectNotFound',
                'message': 'Model deployment not found for the given identifier',
                'help': '',
            }
        ],
    }
}

JOB_API_RESPONSE_200 = {
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


@responses.activate
def test_update_model_deployment_success() -> None:
    model_deployment = ModelDeployment(model_id=MODEL_ID)

    responses.patch(
        url=f'{URL}/v3/models/{MODEL_ID}/deployment',
        json=API_RESPONSE_200,
    )
    model_deployment.cpu = 300
    model_deployment.active = True

    responses.get(
        url=f'{URL}/v3/jobs/{JOB_ID}',
        json=JOB_API_RESPONSE_200,
    )
    job = model_deployment.update()
    assert isinstance(model_deployment, ModelDeployment)
    assert isinstance(job, Job)
    assert model_deployment.cpu == 300
    assert model_deployment.active


@responses.activate
def test_update_model_deployment_not_found() -> None:
    responses.patch(
        url=f'{URL}/v3/models/{MODEL_ID}/deployment',
        json=API_RESPONSE_404,
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(NotFound):
        model_deployment = ModelDeployment(model_id=MODEL_ID)
        model_deployment.update()
