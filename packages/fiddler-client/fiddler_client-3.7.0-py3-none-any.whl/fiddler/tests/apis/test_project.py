import json
from copy import deepcopy
from datetime import datetime
from http import HTTPStatus
from uuid import UUID

import pytest
import responses
from pytest_mock import MockerFixture
from responses import matchers

from fiddler import __version__
from fiddler.entities.project import Project
from fiddler.exceptions import Conflict, NotFound
from fiddler.tests.constants import ORG_ID, ORG_NAME, PROJECT_ID, PROJECT_NAME, URL

API_RESPONSE_200 = {
    'data': {
        'id': PROJECT_ID,
        'name': PROJECT_NAME,
        'organization': {
            'id': ORG_ID,
            'name': ORG_NAME,
        },
        'created_at': '2023-11-22 16:50:57.705784',
        'updated_at': '2023-11-22 16:50:57.705784',
    }
}

API_RESPONSE_409 = {
    'error': {
        'code': 409,
        'message': 'Project already exists',
        'errors': [
            {
                'reason': 'Conflict',
                'message': 'Project already exists',
                'help': '',
            }
        ],
    }
}

API_RESPONSE_404 = {
    'error': {
        'code': 404,
        'message': 'Project not found for the given identifier',
        'errors': [
            {
                'reason': 'ObjectNotFound',
                'message': 'Project not found for the given identifier',
                'help': '',
            }
        ],
    }
}

API_RESPONSE_FROM_NAME = {
    'data': {
        'page_size': 100,
        'total': 1,
        'item_count': 1,
        'page_count': 1,
        'page_index': 1,
        'offset': 0,
        'items': [API_RESPONSE_200['data']],
    }
}

LIST_API_RESPONSE = {
    'data': {
        'page_size': 100,
        'total': 2,
        'item_count': 2,
        'page_count': 1,
        'page_index': 1,
        'offset': 0,
        'items': [
            API_RESPONSE_200['data'],
            {
                'id': '2531bfd9-2ca2-4a7b-bb5a-136c8da09ca1',
                'name': 'project2',
                'organization': {
                    'id': ORG_ID,
                    'name': ORG_NAME,
                },
                'created_at': '2023-11-22 16:50:57.705784',
                'updated_at': '2023-11-22 16:50:57.705784',
            },
        ],
    }
}


@responses.activate
def test_add_project_success() -> None:
    responses.post(
        url=f'{URL}/v3/projects',
        json=API_RESPONSE_200,
    )
    project = Project(name=PROJECT_NAME).create()
    assert isinstance(project, Project)
    assert project.id == UUID(PROJECT_ID)
    assert project.name == PROJECT_NAME
    assert project.created_at == datetime.fromisoformat(
        API_RESPONSE_200['data']['created_at']
    )
    assert project.updated_at == datetime.fromisoformat(
        API_RESPONSE_200['data']['updated_at']
    )

    assert json.loads(responses.calls[0].request.body) == {'name': PROJECT_NAME}


@responses.activate
def test_add_project_conflict() -> None:
    responses.post(
        url=f'{URL}/v3/projects', json=API_RESPONSE_409, status=HTTPStatus.CONFLICT
    )

    with pytest.raises(Conflict):
        Project(name=PROJECT_NAME).create()


@responses.activate
def test_get_project_success() -> None:
    responses.get(
        url=f'{URL}/v3/projects/{PROJECT_ID}',
        json=API_RESPONSE_200,
    )
    project = Project.get(id_=PROJECT_ID)
    assert isinstance(project, Project)


@responses.activate
def test_get_project_not_found() -> None:
    responses.get(
        url=f'{URL}/v3/projects/{PROJECT_ID}',
        json=API_RESPONSE_404,
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(NotFound):
        Project.get(id_=PROJECT_ID)


@responses.activate
def test_project_from_name_success() -> None:
    params = {
        'filter': '{"condition": "AND", "rules": [{"field": "name", "operator": "equal", "value": "bank_churn"}]}'
    }
    responses.get(
        url=f'{URL}/v3/projects',
        json=API_RESPONSE_FROM_NAME,
        match=[matchers.query_param_matcher(params)],
    )
    project = Project.from_name(name=PROJECT_NAME)
    assert isinstance(project, Project)


@responses.activate
def test_project_from_name_not_found() -> None:
    resp = deepcopy(API_RESPONSE_FROM_NAME)
    resp['data']['total'] = 0
    resp['data']['item_count'] = 0
    resp['data']['items'] = []

    params = {
        'filter': '{"condition": "AND", "rules": [{"field": "name", "operator": "equal", "value": "bank_churn"}]}'
    }
    responses.get(
        url=f'{URL}/v3/projects',
        json=resp,
        match=[matchers.query_param_matcher(params)],
    )

    with pytest.raises(NotFound):
        Project.from_name(name=PROJECT_NAME)


@responses.activate
def test_project_list_success() -> None:
    responses.get(
        url=f'{URL}/v3/projects',
        json=LIST_API_RESPONSE,
    )
    for project in Project.list():
        assert isinstance(project, Project)


@responses.activate
def test_project_list_empty() -> None:
    resp = deepcopy(API_RESPONSE_FROM_NAME)
    resp['data']['total'] = 0
    resp['data']['item_count'] = 0
    resp['data']['items'] = []

    responses.get(
        url=f'{URL}/v3/projects',
        json=resp,
    )
    assert len(list(Project.list())) == 0


@responses.activate
def test_delete_project_success() -> None:
    responses.delete(
        url=f'{URL}/v2/projects/{ORG_NAME}:{PROJECT_NAME}',
        json={},
    )
    project = Project(name=PROJECT_NAME)
    project.id = PROJECT_ID

    project.delete()


@responses.activate
def test_delete_project_not_found() -> None:
    responses.delete(
        url=f'{URL}/v2/projects/{ORG_NAME}:{PROJECT_NAME}',
        json=API_RESPONSE_404,
        status=HTTPStatus.NOT_FOUND,
    )
    project = Project(name=PROJECT_NAME)
    project.id = UUID(PROJECT_ID)

    with pytest.raises(NotFound):
        project.delete()


def test_models_property(mocker: MockerFixture) -> None:
    mock_fn = mocker.patch('fiddler.entities.model.Model.list')

    project = Project(name=PROJECT_NAME)
    project.id = UUID(PROJECT_ID)

    _ = list(project.models)

    mock_fn.assert_called_with(project_id=project.id)


@responses.activate
def test_get_or_create_project() -> None:
    # When project doesn't exist
    resp = deepcopy(API_RESPONSE_FROM_NAME)
    resp['data']['total'] = 0
    resp['data']['item_count'] = 0
    resp['data']['items'] = []

    params = {
        'filter': '{"condition": "AND", "rules": [{"field": "name", "operator": "equal", "value": "bank_churn"}]}'
    }
    headers_get = {
        'Authorization': 'Bearer footoken',
        'X-Fiddler-Client-Name': 'python-sdk',
        'X-Fiddler-Client-Version': __version__,
    }

    # Find project by name
    responses.get(
        url=f'{URL}/v3/projects',
        json=resp,
        match=[
            matchers.query_param_matcher(params),
            matchers.header_matcher(headers_get),
        ],
    )

    # POST call to create
    responses.post(
        url=f'{URL}/v3/projects',
        json=API_RESPONSE_200,
        match=[matchers.header_matcher({'Content-Type': 'application/json'})],
    )

    # This call will create the project
    project = Project.get_or_create(name=PROJECT_NAME)
    assert project.id == UUID(PROJECT_ID)

    # When project exists
    responses.replace(
        method_or_response=responses.GET,
        url=f'{URL}/v3/projects',
        json=API_RESPONSE_FROM_NAME,
        match=[
            matchers.query_param_matcher(params),
            matchers.header_matcher(headers_get),
        ],
    )

    # This will fetch the project by name
    project = Project.get_or_create(name=PROJECT_NAME)
    assert project.id == UUID(PROJECT_ID)
