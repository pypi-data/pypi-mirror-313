from http import HTTPStatus
from uuid import UUID

import pytest
import responses
from responses import matchers

from fiddler.entities.custom_expression import Segment
from fiddler.exceptions import Conflict, NotFound
from fiddler.tests.constants import (
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

SEGMENT_ID = '7057867c-6dd8-4915-89f2-a5f253dd4a3a'
SEGMENT_NAME = 'age < 50'

API_RESPONSE_200 = {
    'data': {
        'id': SEGMENT_ID,
        'name': SEGMENT_NAME,
        'definition': "\"Age\" < 50",
        'description': 'Age less than 50',
        'project': {
            'id': PROJECT_ID,
            'name': PROJECT_NAME,
        },
        'organization': {
            'id': ORG_ID,
            'name': ORG_NAME,
        },
        'model': {
            'id': MODEL_ID,
            'name': MODEL_NAME,
        },
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
        'created_at': '2024-02-13T07:56:04.275549+00:00',
        'updated_at': '2024-02-13T07:56:04.275549+00:00',
    },
    'api_version': '3.0',
    'kind': 'NORMAL',
}

API_RESPONSE_404 = {
    'error': {
        'code': 404,
        'message': 'Segment not found',
        'errors': [
            {
                'reason': 'ObjectNotFound',
                'message': 'Segment not found',
                'help': '',
            }
        ],
    },
    'api_version': '3.0',
    'kind': 'ERROR',
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

EMPTY_LIST_API_RESPONSE = {
    'data': {
        'page_size': 100,
        'total': 0,
        'item_count': 0,
        'page_count': 1,
        'page_index': 1,
        'offset': 0,
        'items': [],
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
                'id': 'a509c450-c00b-4b5c-9a96-89c43e287e5a',
                'name': 'age < 40',
                'definition': "\"Age\" < 40",
                'description': 'Age less than 40',
                'project': {
                    'id': PROJECT_ID,
                    'name': PROJECT_NAME,
                },
                'organization': {
                    'id': ORG_ID,
                    'name': ORG_NAME,
                },
                'model': {
                    'id': MODEL_ID,
                    'name': MODEL_NAME,
                },
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
                'created_at': '2024-02-13T07:56:04.275549+00:00',
                'updated_at': '2024-02-13T07:56:04.275549+00:00',
            },
        ],
    }
}

API_RESPONSE_409 = {
    'error': {
        'code': 409,
        'message': 'Segment with the same name already exists for this model',
        'errors': [
            {
                'reason': 'Conflict',
                'message': 'Segment with the same name already exists for this model',
                'help': '',
            }
        ],
    },
    'api_version': '3.0',
    'kind': 'ERROR',
}


@responses.activate
def test_get_segment() -> None:
    responses.get(
        url=f'{URL}/v3/segments/{SEGMENT_ID}',
        json=API_RESPONSE_200,
    )

    segment = Segment.get(id_=SEGMENT_ID)
    assert isinstance(segment, Segment)
    assert segment.model.id == UUID(MODEL_ID)
    assert segment.project.id == UUID(PROJECT_ID)


@responses.activate
def test_get_segment_not_found() -> None:
    responses.get(
        url=f'{URL}/v3/segments/{SEGMENT_ID}',
        json=API_RESPONSE_404,
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(NotFound):
        Segment.get(id_=SEGMENT_ID)


@responses.activate
def test_segment_from_name() -> None:
    params = {
        'filter': '{"condition": "AND", "rules": [{"field": "name", "operator": "equal", "value": "age < 50"}, {"field": "model_id", "operator": "equal", "value": "4531bfd9-2ca2-4a7b-bb5a-136c8da09ca2"}]}'
    }

    responses.get(
        url=f'{URL}/v3/segments',
        json=API_RESPONSE_FROM_NAME,
        match=[matchers.query_param_matcher(params)],
    )
    segment = Segment.from_name(name=SEGMENT_NAME, model_id=MODEL_ID)
    assert isinstance(segment, Segment)


@responses.activate
def test_segment_from_name_not_found() -> None:
    params = {
        'filter': '{"condition": "AND", "rules": [{"field": "name", "operator": "equal", "value": "age < 50"}, {"field": "model_id", "operator": "equal", "value": "4531bfd9-2ca2-4a7b-bb5a-136c8da09ca2"}]}'
    }
    responses.get(
        url=f'{URL}/v3/segments',
        json=EMPTY_LIST_API_RESPONSE,
        match=[matchers.query_param_matcher(params)],
    )
    with pytest.raises(NotFound):
        Segment.from_name(name=SEGMENT_NAME, model_id=MODEL_ID)


@responses.activate
def test_segment_list_empty() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}/segments',
        json=EMPTY_LIST_API_RESPONSE,
    )

    assert len(list(Segment.list(model_id=MODEL_ID))) == 0


@responses.activate
def test_segment_list_success() -> None:
    params = {
        'limit': 50,
        'offset': 0,
    }

    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}/segments',
        json=LIST_API_RESPONSE,
        match=[matchers.query_param_matcher(params)],
    )

    for segment in Segment.list(model_id=MODEL_ID):
        assert isinstance(segment, Segment)


@responses.activate
def test_segment_create() -> None:
    responses.post(
        url=f'{URL}/v3/segments',
        json=API_RESPONSE_200,
    )

    segment = Segment(
        name=SEGMENT_NAME,
        model_id=MODEL_ID,
        definition="average(\"Age\")",
        description='average age',
    ).create()

    assert isinstance(segment, Segment)
    assert segment.id == UUID(SEGMENT_ID)
    assert segment.name == SEGMENT_NAME
    assert segment.model_id


@responses.activate
def test_segment_create_conflict() -> None:
    responses.post(
        url=f'{URL}/v3/segments',
        json=API_RESPONSE_409,
        status=HTTPStatus.CONFLICT,
    )

    with pytest.raises(Conflict):
        Segment(
            name=SEGMENT_NAME,
            model_id=MODEL_ID,
            definition="average(\"Age\")",
            description='average age',
        ).create()


@responses.activate
def test_delete_segment() -> None:
    responses.get(
        url=f'{URL}/v3/segments/{SEGMENT_ID}',
        json=API_RESPONSE_200,
    )
    segment = Segment.get(id_=SEGMENT_ID)

    responses.delete(
        url=f'{URL}/v3/segments/{SEGMENT_ID}',
    )

    segment.delete()


@responses.activate
def test_delete_segment_not_found() -> None:
    responses.get(
        url=f'{URL}/v3/segments/{SEGMENT_ID}',
        json=API_RESPONSE_200,
    )

    segment = Segment.get(id_=SEGMENT_ID)

    responses.delete(
        url=f'{URL}/v3/segments/{SEGMENT_ID}',
        json=API_RESPONSE_404,
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(NotFound):
        segment.delete()
