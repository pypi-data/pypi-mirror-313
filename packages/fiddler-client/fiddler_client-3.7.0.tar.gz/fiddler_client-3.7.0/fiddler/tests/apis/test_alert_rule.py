import json
import uuid
from copy import deepcopy
from http import HTTPStatus
from uuid import UUID

import pytest
import responses
from pydantic.v1 import ValidationError

from fiddler.constants.alert_rule import AlertCondition, BinSize, CompareTo, Priority
from fiddler.entities.alert_rule import AlertRule
from fiddler.exceptions import NotFound
from fiddler.schemas.alert_rule import NotificationConfig
from fiddler.tests.apis.test_baseline import (
    API_RESPONSE_200 as BASELINE_API_RESPONSE_200,
)
from fiddler.tests.apis.test_model import API_RESPONSE_200 as MODEL_API_RESPONSE_200
from fiddler.tests.constants import (
    ALERT_RULE_ID,
    BASELINE_ID,
    BASELINE_NAME,
    MODEL_ID,
    MODEL_NAME,
    PROJECT_ID,
    PROJECT_NAME,
    TEST_EMAILS,
    TEST_PAGERDUTY_SERVICES,
    TEST_PAGERDUTY_SEVERITY,
    TEST_WEBHOOKS,
    URL,
)

API_RESPONSE_200 = {
    'data': {
        'id': ALERT_RULE_ID,
        'model': {'id': MODEL_ID, 'name': MODEL_NAME, 'version': 'v1'},
        'project': {'id': PROJECT_ID, 'name': PROJECT_NAME},
        'organization': {
            'id': 'e03d6f02-6efa-4eb1-b828-7ea9d2a083d0',
            'name': 'scale154',
        },
        'baseline': None,
        'segment': None,
        'version': 'rule_v3',
        'name': 'skdfvbj',
        'priority': 'HIGH',
        'feature_names': ['gender'],
        'bin_size': 'Hour',
        'compare_to': 'raw_value',
        'condition': 'greater',
        'warning_threshold': 1.0,
        'evaluation_delay': 10,
        'critical_threshold': 2.0,
        'updated_at': '2024-04-17T12:42:15.672909+00:00',
        'enable_notification': True,
        'compare_bin_delta': 0,
        'created_at': '2024-04-17T12:42:15.672909+00:00',
        'created_by': {
            'id': '287949c2-13f8-49fc-a559-55b2e6f36e9b',
            'full_name': 'Fiddler Administrator',
            'email': 'admin@fiddler.ai',
        },
        'updated_by': {
            'id': '287949c2-13f8-49fc-a559-55b2e6f36e9b',
            'full_name': 'Fiddler Administrator',
            'email': 'admin@fiddler.ai',
        },
        'metric': {
            'id': 'null_violation_percentage',
            'display_name': '% Missing Value Violation',
            'type': 'data_integrity',
            'type_display_name': 'Data Integrity',
        },
    },
    'api_version': '3.0',
    'kind': 'NORMAL',
}

ALERT_NOTIFICATION_API_RESPONSE_200 = {
    'data': {
        'emails': [],
        'webhooks': [],
        'pagerduty_services': [],
        'pagerduty_severity': '',
    },
    'api_version': '3.0',
    'kind': 'NORMAL',
}

API_RESPONSE_404 = {
    'error': {
        'code': 404,
        'message': "AlertConfig({'uuid': 'ff9a897b-be5b-48e6-909f-13073a6d0fe8'}) not found",
        'errors': [
            {
                'reason': 'ObjectNotFound',
                'message': "AlertConfig({'uuid': 'ff9a897b-be5b-48e6-909f-13073a6d0fe8'}) not found",
                'help': '',
            }
        ],
    },
    'api_version': '2.0',
    'kind': 'ERROR',
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
                'id': '3431b746-d18f-4aed-99ea-2da8d5b46fb6',
                'model': {'id': MODEL_ID, 'name': MODEL_NAME, 'version': 'v1'},
                'project': {'id': PROJECT_ID, 'name': PROJECT_NAME},
                'organization': {
                    'id': 'e03d6f02-6efa-4eb1-b828-7ea9d2a083d0',
                    'name': 'scale154',
                },
                'baseline': {'id': BASELINE_ID, 'name': BASELINE_NAME},
                'segment': None,
                'version': 'rule_v3',
                'name': 'sfdvsefv',
                'priority': 'HIGH',
                'feature_names': ['numofproducts'],
                'bin_size': 'Hour',
                'compare_to': 'raw_value',
                'condition': 'greater',
                'warning_threshold': 1e-05,
                'critical_threshold': 0.001,
                'updated_at': '2024-04-17T12:43:23.871997+00:00',
                'enable_notification': True,
                'compare_bin_delta': 0,
                'evaluation_delay': 0,
                'created_at': '2024-04-17T12:43:23.871997+00:00',
                'created_by': {
                    'id': '287949c2-13f8-49fc-a559-55b2e6f36e9b',
                    'full_name': 'Fiddler Administrator',
                    'email': 'admin@fiddler.ai',
                },
                'updated_by': {
                    'id': '287949c2-13f8-49fc-a559-55b2e6f36e9b',
                    'full_name': 'Fiddler Administrator',
                    'email': 'admin@fiddler.ai',
                },
                'metric': {
                    'id': 'jsd',
                    'display_name': 'Jensen-Shannon Distance',
                    'type': 'drift',
                    'type_display_name': 'Data Drift',
                },
            },
        ],
    }
}

LIST_API_RESPONSE_EMPTY = {
    'data': {
        'page_size': 100,
        'total': 2,
        'item_count': 2,
        'page_count': 1,
        'page_index': 1,
        'offset': 0,
        'items': [],
    }
}


@responses.activate
def test_get_alert_rule_success() -> None:
    responses.get(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}',
        json=API_RESPONSE_200,
    )

    alert_rule = AlertRule.get(id_=ALERT_RULE_ID)

    assert isinstance(alert_rule, AlertRule)


@responses.activate
def test_get_alert_rule_not_found() -> None:
    responses.get(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}',
        json=API_RESPONSE_404,
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(NotFound):
        AlertRule.get(id_=ALERT_RULE_ID)


@responses.activate
def test_alert_rule_list_success() -> None:
    responses.get(
        url=f'{URL}/v3/alert-rules',
        json=LIST_API_RESPONSE,
    )
    for rule in AlertRule.list(model_id=MODEL_ID):
        assert isinstance(rule, AlertRule)


@responses.activate
def test_alert_rule_list_empty() -> None:
    responses.get(
        url=f'{URL}/v3/alert-rules',
        json=LIST_API_RESPONSE_EMPTY,
    )

    assert len(list(AlertRule.list(model_id=MODEL_ID))) == 0


@responses.activate
def test_delete_alert_rule() -> None:
    responses.get(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}',
        json=API_RESPONSE_200,
    )
    rule = AlertRule.get(id_=ALERT_RULE_ID)

    responses.delete(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}',
    )

    rule.delete()


@responses.activate
def test_delete_alert_rule_not_found() -> None:
    responses.get(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}',
        json=API_RESPONSE_200,
    )
    rule = AlertRule.get(id_=ALERT_RULE_ID)

    responses.delete(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}',
        json=API_RESPONSE_404,
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(NotFound):
        rule.delete()


@responses.activate
def test_add_alert_rule_success() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )
    responses.get(
        url=f'{URL}/v3/baselines/{BASELINE_ID}',
        json=BASELINE_API_RESPONSE_200,
    )
    responses.post(
        url=f'{URL}/v3/alert-rules',
        json=API_RESPONSE_200,
    )
    alert_rule = AlertRule(
        name='alert_name',
        model_id=MODEL_ID,
        metric_id='drift',
        priority=Priority.HIGH,
        compare_to=CompareTo.RAW_VALUE,
        condition=AlertCondition.GREATER,
        bin_size=BinSize.HOUR,
        critical_threshold=0.5,
        warning_threshold=0.1,
        columns=['gender', 'creditscore'],
        evaluation_delay=10,
    ).create()

    assert isinstance(alert_rule, AlertRule)
    assert alert_rule.id == UUID(ALERT_RULE_ID)
    assert alert_rule.model.id == UUID(MODEL_ID)
    assert alert_rule.project_id == UUID(PROJECT_ID)
    assert alert_rule.evaluation_delay == 10


@responses.activate
def test_enable_notifications() -> None:
    responses.get(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}',
        json=API_RESPONSE_200,
    )

    alert_rule = AlertRule.get(id_=ALERT_RULE_ID)

    resp = responses.patch(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}',
        json=API_RESPONSE_200,
    )
    alert_rule.enable_notifications()
    assert json.loads(resp.calls[0].request.body) == {'enable_notification': True}


@responses.activate
def test_disable_notifications() -> None:
    responses.get(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}',
        json=API_RESPONSE_200,
    )

    alert_rule = AlertRule.get(id_=ALERT_RULE_ID)

    API_RESPONSE_200['enable_notification'] = False

    resp = responses.patch(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}',
        json=API_RESPONSE_200,
    )

    alert_rule.disable_notifications()
    assert json.loads(resp.calls[0].request.body) == {'enable_notification': False}


@responses.activate
def test_set_notifications_email() -> None:
    responses.get(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}',
        json=API_RESPONSE_200,
    )

    alert_rule = AlertRule.get(id_=ALERT_RULE_ID)
    notification_resp = deepcopy(ALERT_NOTIFICATION_API_RESPONSE_200)
    notification_resp['data']['emails'] = TEST_EMAILS
    resp = responses.patch(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}/notification',
        json=notification_resp,
    )
    notifications = alert_rule.set_notification_config(
        emails=TEST_EMAILS,
    )
    assert json.loads(resp.calls[0].request.body) == {
        'emails': TEST_EMAILS,
    }
    assert notifications == notification_resp['data']

    # Removing the emails from the notification config
    notification_resp['data']['emails'] = []
    resp = responses.patch(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}/notification',
        json=notification_resp,
    )
    notifications = alert_rule.set_notification_config(
        emails=[],
    )
    assert json.loads(resp.calls[0].request.body) == {
        'emails': [],
    }
    assert notifications == notification_resp['data']


@responses.activate
def test_set_notifications_pagerduty() -> None:
    responses.get(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}',
        json=API_RESPONSE_200,
    )

    alert_rule = AlertRule.get(id_=ALERT_RULE_ID)
    notification_resp = deepcopy(ALERT_NOTIFICATION_API_RESPONSE_200)
    notification_resp['data']['pagerduty_services'] = TEST_PAGERDUTY_SERVICES
    notification_resp['data']['pagerduty_severity'] = TEST_PAGERDUTY_SEVERITY
    resp = responses.patch(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}/notification',
        json=notification_resp,
    )
    notifications = alert_rule.set_notification_config(
        pagerduty_services=TEST_PAGERDUTY_SERVICES,
        pagerduty_severity=TEST_PAGERDUTY_SEVERITY,
    )

    assert json.loads(resp.calls[0].request.body) == {
        'pagerduty_services': TEST_PAGERDUTY_SERVICES,
        'pagerduty_severity': TEST_PAGERDUTY_SEVERITY,
    }
    assert notifications == notification_resp['data']

    # Removing the webhooks from the notification config
    notification_resp['data']['pagerduty_services'] = []
    notification_resp['data']['pagerduty_severity'] = ''
    resp = responses.patch(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}/notification',
        json=notification_resp,
    )
    notifications = alert_rule.set_notification_config(
        pagerduty_services=[],
        pagerduty_severity='',
    )
    assert json.loads(resp.calls[0].request.body) == {
        'pagerduty_services': [],
        'pagerduty_severity': '',
    }
    assert notifications == notification_resp['data']


@responses.activate
def test_set_notifications_webhooks() -> None:
    responses.get(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}',
        json=API_RESPONSE_200,
    )

    alert_rule = AlertRule.get(id_=ALERT_RULE_ID)
    notification_resp = deepcopy(ALERT_NOTIFICATION_API_RESPONSE_200)
    notification_resp['data']['webhooks'] = TEST_WEBHOOKS
    resp = responses.patch(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}/notification',
        json=notification_resp,
    )
    notifications = alert_rule.set_notification_config(
        webhooks=TEST_WEBHOOKS,
    )

    notification_resp['data']['webhooks'] = [
        uuid.UUID(webhook_uuid)
        for webhook_uuid in notification_resp['data']['webhooks']
    ]
    assert json.loads(resp.calls[0].request.body) == {
        'webhooks': TEST_WEBHOOKS,
    }
    assert notifications == notification_resp['data']

    # Removing the webhooks from the notification config
    notification_resp['data']['webhooks'] = []
    resp = responses.patch(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}/notification',
        json=notification_resp,
    )
    notifications = alert_rule.set_notification_config(
        webhooks=[],
    )
    assert json.loads(resp.calls[0].request.body) == {
        'webhooks': [],
    }
    assert notifications == notification_resp['data']


@responses.activate
def test_set_notifications_invalid_input() -> None:
    responses.get(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}',
        json=API_RESPONSE_200,
    )

    alert_rule = AlertRule.get(id_=ALERT_RULE_ID)

    with pytest.raises(ValidationError):
        alert_rule.set_notification_config(
            emails=TEST_EMAILS[0],
            webhooks=TEST_WEBHOOKS,
        )


@responses.activate
def test_get_notifications() -> None:
    responses.get(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}',
        json=API_RESPONSE_200,
    )

    alert_rule = AlertRule.get(id_=ALERT_RULE_ID)
    responses.get(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}/notification',
        json=ALERT_NOTIFICATION_API_RESPONSE_200,
    )
    notifications = alert_rule.get_notification_config()
    assert notifications == NotificationConfig(
        **ALERT_NOTIFICATION_API_RESPONSE_200['data']
    )
