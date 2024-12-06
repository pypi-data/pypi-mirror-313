import json
from copy import deepcopy
from datetime import datetime
from http import HTTPStatus
from uuid import UUID

import pytest
import responses

from fiddler.entities.webhook import Webhook
from fiddler.exceptions import Conflict, NotFound
from fiddler.tests.constants import (
    ORG_NAME,
    URL,
    WEBHOOK_ID,
    WEBHOOK_NAME,
    WEBHOOK_PROVIDER,
    WEBHOOK_URL,
)

API_RESPONSE_200 = {
    'data': {
        'id': WEBHOOK_ID,
        'name': WEBHOOK_NAME,
        'url': WEBHOOK_URL,
        'provider': WEBHOOK_PROVIDER,
        'created_at': '2023-12-18T10:23:51.232768+00:00',
        'updated_at': '2023-12-18T10:23:51.232768+00:00',
        'organization_name': ORG_NAME,
    },
    'api_version': '2.0',
    'kind': 'NORMAL',
}

API_RESPONSE_404 = {
    'error': {
        'code': 404,
        'message': "WebhookConfig({'uuid': '128e4df4-91a8-8d61-d9e2-222eecb829f2'}) not found",
        'errors': [
            {
                'reason': 'ObjectNotFound',
                'message': "WebhookConfig({'uuid': '128e4df4-91a8-8d61-d9e2-222eecb829f2'}) not found",
                'help': '',
            }
        ],
    },
    'api_version': '2.0',
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
        'items': [
            {
                # Note(JP): the schema does not define `uuid` but only `id`,
                # and `id` is of type UUID. Should we allow for additional
                # properties?
                'id': WEBHOOK_ID,
                'name': WEBHOOK_NAME,
                'url': WEBHOOK_URL,
                'provider': WEBHOOK_PROVIDER,
                'created_at': '2024-04-30T13:38:08.408013+00:00',
                'updated_at': '2024-04-30T13:38:08.408013+00:00',
                'organization_name': ORG_NAME,
            }
        ],
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
                'id': WEBHOOK_ID,
                'name': 'test_webhook_config_name2',
                'url': WEBHOOK_URL,
                'provider': WEBHOOK_PROVIDER,
                'created_at': '2023-12-18T10:23:51.232768+00:00',
                'updated_at': '2023-12-18T10:23:51.232768+00:00',
                'organization_name': ORG_NAME,
            },
        ],
    }
}

API_RESPONSE_EMPTY_LIST = {
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

API_RESPONSE_409 = {
    'error': {
        'code': 409,
        'message': f'A webhook integration with the provided name ({WEBHOOK_NAME}) \
                    already exists. Webhook names must be unique.',
        'errors': [
            {
                'reason': 'Conflict',
                'message': f'A webhook integration with the provided name \
                        ({WEBHOOK_NAME}) already exists. Webhook names must be unique.',
                'help': '',
            }
        ],
    }
}


@responses.activate
def test_get_webhook_success() -> None:
    responses.get(
        url=f'{URL}/v2/webhooks/{WEBHOOK_ID}',
        json=API_RESPONSE_200,
    )
    webhook = Webhook.get(id_=WEBHOOK_ID)
    assert isinstance(webhook, Webhook)


@responses.activate
def test_get_webhook_not_found() -> None:
    webhook_id = '128e4df4-91a8-8d61-d9e2-222eecb829f2'
    responses.get(
        url=f'{URL}/v2/webhooks/{webhook_id}',
        json=API_RESPONSE_404,
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(NotFound):
        Webhook.get(id_=webhook_id)


@responses.activate
def test_webhook_from_name_success() -> None:
    params = {
        'filter': '{"condition": "AND", "rules": [{"field": "name", "operator": "equal", "value": "test_webhook_config_name"}]}'
    }
    responses.get(
        url=f'{URL}/v2/webhooks',
        json=API_RESPONSE_FROM_NAME,
        match=[responses.matchers.query_param_matcher(params)],
    )
    webhook = Webhook.from_name(name=WEBHOOK_NAME)
    assert isinstance(webhook, Webhook)


@responses.activate
def test_webhook_from_name_not_found() -> None:
    resp = deepcopy(API_RESPONSE_FROM_NAME)
    resp['data']['total'] = 0
    resp['data']['item_count'] = 0
    resp['data']['items'] = []

    params = {
        'filter': '{"condition": "AND", "rules": [{"field": "name", "operator": "equal", "value": "test_webhook_config_name"}]}'
    }
    responses.get(
        url=f'{URL}/v2/webhooks',
        json=resp,
        match=[responses.matchers.query_param_matcher(params)],
    )

    with pytest.raises(NotFound):
        Webhook.from_name(name=WEBHOOK_NAME)


@responses.activate
def test_webhook_list_success() -> None:
    responses.get(
        url=f'{URL}/v2/webhooks',
        json=LIST_API_RESPONSE,
    )
    for webhook in Webhook.list():
        assert isinstance(webhook, Webhook)


@responses.activate
def test_webhook_list_empty() -> None:
    resp = API_RESPONSE_EMPTY_LIST

    responses.get(
        url=f'{URL}/v2/webhooks',
        json=resp,
    )
    assert len(list(Webhook.list())) == 0


@responses.activate
def test_add_webhook_success() -> None:
    responses.post(
        url=f'{URL}/v2/webhooks',
        json=API_RESPONSE_200,
    )
    webhook = Webhook(
        name=WEBHOOK_NAME, url=WEBHOOK_URL, provider=WEBHOOK_PROVIDER
    ).create()
    assert isinstance(webhook, Webhook)
    assert webhook.id == UUID(WEBHOOK_ID)
    assert webhook.name == WEBHOOK_NAME
    assert webhook.created_at == datetime.fromisoformat(
        API_RESPONSE_200['data']['created_at']
    )
    assert webhook.updated_at == datetime.fromisoformat(
        API_RESPONSE_200['data']['updated_at']
    )

    assert json.loads(responses.calls[0].request.body) == {
        'name': WEBHOOK_NAME,
        'url': WEBHOOK_URL,
        'provider': WEBHOOK_PROVIDER,
    }


@responses.activate
def test_add_webhook_conflict() -> None:
    responses.post(
        url=f'{URL}/v2/webhooks', json=API_RESPONSE_409, status=HTTPStatus.CONFLICT
    )

    with pytest.raises(Conflict):
        Webhook(
            name=WEBHOOK_NAME,
            url=WEBHOOK_URL,
            provider=WEBHOOK_PROVIDER,
        ).create()


@responses.activate
def test_update_webhook_success(mocker) -> None:
    responses.get(
        url=f'{URL}/v2/webhooks/{WEBHOOK_ID}',
        json=API_RESPONSE_200,
    )
    webhook = Webhook.get(id_=WEBHOOK_ID)

    mocker.patch.dict(API_RESPONSE_200['data'], {'name': 'test1'})
    responses.patch(
        url=f'{URL}/v2/webhooks/{WEBHOOK_ID}',
        json=API_RESPONSE_200,
    )
    webhook.name = 'test1'

    webhook.update()
    assert isinstance(webhook, Webhook)
    assert webhook.name == 'test1'


@responses.activate
def test_update_webhook_not_found() -> None:
    responses.get(
        url=f'{URL}/v2/webhooks/{WEBHOOK_ID}',
        json=API_RESPONSE_200,
    )

    responses.patch(
        url=f'{URL}/v2/webhooks/{WEBHOOK_ID}',
        json=API_RESPONSE_404,
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(NotFound):
        webhook = Webhook.get(id_=WEBHOOK_ID)
        webhook.update()


@responses.activate
def test_delete_webhook() -> None:
    responses.get(
        url=f'{URL}/v2/webhooks/{WEBHOOK_ID}',
        json=API_RESPONSE_200,
    )
    webhook = Webhook.get(id_=WEBHOOK_ID)

    responses.delete(
        url=f'{URL}/v2/webhooks/{WEBHOOK_ID}',
        json={},
    )
    response = webhook.delete()
    assert response is None


@responses.activate
def test_delete_webhook_not_found() -> None:
    responses.get(
        url=f'{URL}/v2/webhooks/{WEBHOOK_ID}',
        json=API_RESPONSE_200,
    )
    webhook = Webhook.get(id_=WEBHOOK_ID)

    responses.delete(
        url=f'{URL}/v2/webhooks/{WEBHOOK_ID}',
        json=API_RESPONSE_404,
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(NotFound):
        webhook.delete()
