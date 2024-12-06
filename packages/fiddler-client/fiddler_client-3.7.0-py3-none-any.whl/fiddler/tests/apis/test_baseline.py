from copy import deepcopy
from http import HTTPStatus
from uuid import UUID

import pytest
import responses
from responses import matchers

from fiddler.constants.baseline import BaselineType
from fiddler.entities.baseline import Baseline
from fiddler.exceptions import Conflict, NotFound
from fiddler.tests.constants import (
    BASELINE_ID,
    BASELINE_NAME,
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
        'id': BASELINE_ID,
        'name': BASELINE_NAME,
        'type': 'STATIC',
        'start_time': None,
        'end_time': None,
        'offset_delta': None,
        'window_bin_size': None,
        'row_count': 20000,
        'model': {
            'id': MODEL_ID,
            'name': MODEL_NAME,
        },
        'project': {'id': PROJECT_ID, 'name': PROJECT_NAME},
        'organization': {
            'id': ORG_ID,
            'name': ORG_NAME,
        },
        'environment': {
            'id': DATASET_ID,
            'name': DATASET_NAME,
            'type': 'PRE_PRODUCTION',
        },
        'created_at': '2023-10-05T18:46:40.526590+00:00',
        'updated_at': '2023-10-05T18:46:40.526590+00:00',
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
                'id': 'af05646f-0cef-4638-84c9-0d195df2575f',
                'name': 'test_baseline_2',
                'type': 'STATIC',
                'start_time': None,
                'end_time': None,
                'offset_delta': None,
                'window_bin_size': None,
                'row_count': 20000,
                'model': {
                    'id': MODEL_ID,
                    'name': MODEL_NAME,
                },
                'project': {'id': PROJECT_ID, 'name': PROJECT_NAME},
                'organization': {
                    'id': ORG_ID,
                    'name': ORG_NAME,
                },
                'environment': {
                    'id': DATASET_ID,
                    'name': DATASET_NAME,
                    'type': 'PRE_PRODUCTION',
                },
                'created_at': '2023-10-05T18:46:40.526590+00:00',
                'updated_at': '2023-10-05T18:46:40.526590+00:00',
            },
        ],
    }
}

API_RESPONSE_404 = {
    'error': {
        'code': 404,
        'message': 'Baseline not found for the given identifier',
        'errors': [
            {
                'reason': 'ObjectNotFound',
                'message': 'Baseline not found for the given identifier',
                'help': '',
            }
        ],
    }
}

API_RESPONSE_409 = {
    'error': {
        'code': 409,
        'message': 'Baseline already exists',
        'errors': [
            {
                'reason': 'Conflict',
                'message': 'Baseline already exists',
                'help': '',
            }
        ],
    }
}


@responses.activate
def test_get_baseline_success() -> None:
    responses.get(
        url=f'{URL}/v3/baselines/{BASELINE_ID}',
        json=API_RESPONSE_200,
    )

    baseline = Baseline.get(id_=BASELINE_ID)

    assert isinstance(baseline, Baseline)


@responses.activate
def test_get_baseline_not_found() -> None:
    responses.get(
        url=f'{URL}/v3/baselines/{BASELINE_ID}',
        json=API_RESPONSE_404,
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(NotFound):
        Baseline.get(id_=BASELINE_ID)


@responses.activate
def test_baseline_from_name() -> None:
    params = {
        'filter': '{"condition": "AND", "rules": [{"field": "name", "operator": "equal", "value": "test_baseline"}, {"field": "model_id", "operator": "equal", "value": "4531bfd9-2ca2-4a7b-bb5a-136c8da09ca2"}]}'
    }

    responses.get(
        url=f'{URL}/v3/baselines',
        json=API_RESPONSE_FROM_NAME,
        match=[matchers.query_param_matcher(params)],
    )
    baseline = Baseline.from_name(
        name=BASELINE_NAME,
        model_id=MODEL_ID,
    )
    assert isinstance(baseline, Baseline)


@responses.activate
def test_baseline_from_name_not_found() -> None:
    resp = deepcopy(API_RESPONSE_FROM_NAME)
    resp['data']['total'] = 0
    resp['data']['item_count'] = 0
    resp['data']['items'] = []

    params = {
        'filter': '{"condition": "AND", "rules": [{"field": "name", "operator": "equal", "value": "test_baseline"}, {"field": "model_id", "operator": "equal", "value": "4531bfd9-2ca2-4a7b-bb5a-136c8da09ca2"}]}'
    }

    responses.get(
        url=f'{URL}/v3/baselines',
        json=resp,
        match=[matchers.query_param_matcher(params)],
    )
    with pytest.raises(NotFound):
        Baseline.from_name(
            name=BASELINE_NAME,
            model_id=MODEL_ID,
        )


@responses.activate
def test_baseline_list_success() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}/baselines',
        json=LIST_API_RESPONSE,
    )
    for baseline in Baseline.list(model_id=MODEL_ID):
        assert isinstance(baseline, Baseline)


@responses.activate
def test_baseline_list_empty() -> None:
    resp = deepcopy(API_RESPONSE_FROM_NAME)
    resp['data']['total'] = 0
    resp['data']['item_count'] = 0
    resp['data']['items'] = []

    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}/baselines',
        json=resp,
    )
    assert len(list(Baseline.list(model_id=MODEL_ID))) == 0


@responses.activate
def test_add_baseline_success() -> None:
    responses.post(
        url=f'{URL}/v3/baselines',
        json=API_RESPONSE_200,
    )
    baseline = Baseline(
        name=BASELINE_NAME,
        model_id=MODEL_ID,
        environment='PRE_PRODUCTION',
        dataset_id=DATASET_ID,
        type_=BaselineType.STATIC,
    ).create()

    assert isinstance(baseline, Baseline)
    assert baseline.id == UUID(BASELINE_ID)
    assert baseline.name == BASELINE_NAME


@responses.activate
def test_add_baseline_conflict() -> None:
    responses.post(
        url=f'{URL}/v3/baselines', json=API_RESPONSE_409, status=HTTPStatus.CONFLICT
    )

    with pytest.raises(Conflict):
        Baseline(
            name=BASELINE_NAME,
            model_id=MODEL_ID,
            environment='PRE_PRODUCTION',
            dataset_id=DATASET_ID,
            type_=BaselineType.STATIC,
        ).create()


@responses.activate
def test_delete_baseline() -> None:
    responses.get(
        url=f'{URL}/v3/baselines/{BASELINE_ID}',
        json=API_RESPONSE_200,
    )
    baseline = Baseline.get(id_=BASELINE_ID)

    responses.delete(
        url=f'{URL}/v3/baselines/{BASELINE_ID}',
    )

    baseline.delete()


@responses.activate
def test_delete_baseline_not_found() -> None:
    responses.get(
        url=f'{URL}/v3/baselines/{BASELINE_ID}',
        json=API_RESPONSE_200,
    )
    baseline = Baseline.get(id_=BASELINE_ID)

    responses.delete(
        url=f'{URL}/v3/baselines/{BASELINE_ID}',
        json=API_RESPONSE_404,
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(NotFound):
        baseline.delete()
