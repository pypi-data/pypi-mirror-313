from datetime import datetime

import responses

from fiddler.entities.alert_record import AlertRecord
from fiddler.tests.constants import ALERT_RULE_ID, URL

ALERT_RECORD_LIST_RESPONSE = {
    'data': {
        'page_size': 100,
        'total': 2,
        'item_count': 2,
        'page_count': 1,
        'page_index': 1,
        'offset': 0,
        'items': [
            {
                'id': 26410,
                'uuid': 'b520da6b-c01c-4375-bde6-2560cd972485',
                'alert_config_uuid': ALERT_RULE_ID,
                'alert_run_start_time': 1703255503133,
                'alert_time_bucket': 1703116800000,
                'baseline_time_bucket': None,
                'baseline_value': None,
                'is_alert': True,
                'severity': 'CRITICAL',
                'failure_reason': 'NA',
                'message': '',
                'alert_value': 37.0,
                'feature_name': 'estimatedsalary',
                'alert_record_main_version': 1,
                'alert_record_sub_version': 2,
                'created_at': '2023-12-22T14:31:43.499697+00:00',
                'updated_at': '2023-12-22T14:31:43.499697+00:00',
            },
            {
                'id': 26418,
                'uuid': '6e55540c-9053-4af8-b20e-1728b1436f35',
                'alert_config_uuid': ALERT_RULE_ID,
                'alert_run_start_time': 1703259102527,
                'alert_time_bucket': 1703116800000,
                'baseline_time_bucket': None,
                'baseline_value': None,
                'is_alert': True,
                'severity': 'CRITICAL',
                'failure_reason': 'NA',
                'message': '',
                'alert_value': 37.0,
                'feature_name': 'estimatedsalary',
                'alert_record_main_version': 1,
                'alert_record_sub_version': 3,
                'created_at': '2023-12-22T15:31:42.698623+00:00',
                'updated_at': '2023-12-22T15:31:42.698623+00:00',
            },
        ],
    },
    'api_version': '2.0',
    'kind': 'PAGINATED',
}

ALERT_RECORD_EMPTY_LIST_RESPONSE = {
    'data': {
        'page_size': 100,
        'total': 0,
        'item_count': 0,
        'page_count': 1,
        'page_index': 1,
        'offset': 0,
        'items': [],
    },
    'api_version': '2.0',
    'kind': 'PAGINATED',
}


@responses.activate
def test_alert_record_list_success() -> None:
    responses.get(
        url=f'{URL}/v2/alert-configs/{ALERT_RULE_ID}/records',
        json=ALERT_RECORD_LIST_RESPONSE,
    )
    alert_records = AlertRecord.list(
        alert_rule_id=ALERT_RULE_ID,
        start_time=datetime(2023, 12, 18),
        end_time=datetime(2023, 12, 25),
    )
    for record in alert_records:
        assert isinstance(record, AlertRecord)


# this did copy the name of the test above, now I ignorantly appended a _2
@responses.activate
def test_alert_record_list_success_2() -> None:
    responses.get(
        url=f'{URL}/v2/alert-configs/{ALERT_RULE_ID}/records',
        json=ALERT_RECORD_EMPTY_LIST_RESPONSE,
    )
    alert_records = list(AlertRecord.list(alert_rule_id=ALERT_RULE_ID))

    assert len(alert_records) == 0
