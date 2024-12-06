from copy import deepcopy
from http import HTTPStatus

import pytest
import responses
from responses import matchers

from fiddler.entities.dataset import Dataset
from fiddler.exceptions import NotFound
from fiddler.tests.constants import (
    DATASET_ID,
    DATASET_NAME,
    MODEL_ID,
    MODEL_NAME,
    ORG_ID,
    ORG_NAME,
    PROJECT_ID,
    PROJECT_NAME,
    URL,
)

API_RESPONSE_200 = {
    'data': {
        'id': DATASET_ID,
        'name': DATASET_NAME,
        'type': 'PRE_PRODUCTION',
        'row_count': 10000,
        'model': {'id': MODEL_ID, 'name': MODEL_NAME},
        'project': {'id': PROJECT_ID, 'name': PROJECT_NAME},
        'organization': {'id': ORG_ID, 'name': ORG_NAME},
        'created_at': '2023-09-19T13:27:03.684345+00:00',
        'updated_at': '2023-09-19T13:27:03.684345+00:00',
    },
    'api_version': '3.0',
    'kind': 'NORMAL',
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
                'name': 'dataset2',
                'type': 'PRE_PRODUCTION',
                'row_count': 10000,
                'model': {'id': MODEL_ID, 'name': MODEL_NAME},
                'project': {'id': PROJECT_ID, 'name': PROJECT_NAME},
                'organization': {'id': ORG_ID, 'name': ORG_NAME},
                'created_at': '2023-09-19T13:27:03.684345+00:00',
                'updated_at': '2023-09-19T13:27:03.684345+00:00',
            },
        ],
    }
}

API_RESPONSE_404 = {
    'error': {
        'code': 404,
        'message': 'Environment not found for the given identifier',
        'errors': [
            {
                'reason': 'ObjectNotFound',
                'message': 'Environment not found for the given identifier',
                'help': '',
            }
        ],
    }
}


@responses.activate
def test_get_dataset_success() -> None:
    responses.get(
        url=f'{URL}/v3/environments/{DATASET_ID}',
        json=API_RESPONSE_200,
    )

    dataset = Dataset.get(id_=DATASET_ID)
    assert isinstance(dataset, Dataset)


@responses.activate
def test_get_dataset_not_found() -> None:
    responses.get(
        url=f'{URL}/v3/environments/{DATASET_ID}',
        json=API_RESPONSE_404,
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(NotFound):
        Dataset.get(id_=DATASET_ID)


@responses.activate
def test_dataset_from_name() -> None:
    params = {
        'filter': '{"condition": "AND", "rules": [{"field": "name", "operator": "equal", "value": "dataset3"}, {"field": "model_id", "operator": "equal", "value": "4531bfd9-2ca2-4a7b-bb5a-136c8da09ca2"}]}'
    }
    responses.get(
        url=f'{URL}/v3/environments',
        json=API_RESPONSE_FROM_NAME,
        match=[matchers.query_param_matcher(params)],
    )
    dataset = Dataset.from_name(name=DATASET_NAME, model_id=MODEL_ID)
    assert isinstance(dataset, Dataset)


@responses.activate
def test_dataset_from_name_not_found() -> None:
    resp = deepcopy(API_RESPONSE_FROM_NAME)
    resp['data']['total'] = 0
    resp['data']['item_count'] = 0
    resp['data']['items'] = []

    params = {
        'filter': '{"condition": "AND", "rules": [{"field": "name", "operator": "equal", "value": "dataset3"}, {"field": "model_id", "operator": "equal", "value": "4531bfd9-2ca2-4a7b-bb5a-136c8da09ca2"}]}'
    }
    responses.get(
        url=f'{URL}/v3/environments',
        json=resp,
        match=[matchers.query_param_matcher(params)],
    )
    with pytest.raises(NotFound):
        Dataset.from_name(
            name=DATASET_NAME,
            model_id=MODEL_ID,
        )


@responses.activate
def test_dataset_list_success() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}/environments',
        json=LIST_API_RESPONSE,
    )
    for dataset in Dataset.list(model_id=MODEL_ID):
        assert isinstance(dataset, Dataset)


@responses.activate
def test_dataset_list_empty() -> None:
    resp = deepcopy(API_RESPONSE_FROM_NAME)
    resp['data']['total'] = 0
    resp['data']['item_count'] = 0
    resp['data']['items'] = []

    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}/environments',
        json=resp,
    )
    assert len(list(Dataset.list(model_id=MODEL_ID))) == 0
