from datetime import datetime
from uuid import UUID

import pytest
import simplejson

from fiddler.libs.json_encoder import RequestClientJSONEncoder


def test_json_encoder_uuid():
    data = {'uuid_field': UUID('6ea7243e-0bf7-4323-ba1b-9f788b4a9257')}
    with pytest.raises(TypeError):
        simplejson.dumps(data)

    assert simplejson.dumps(data, cls=RequestClientJSONEncoder) == simplejson.dumps(
        {'uuid_field': '6ea7243e-0bf7-4323-ba1b-9f788b4a9257'}
    )


def test_json_encoder_datetime():
    data = {'datetime_field': datetime(2024, 1, 30, 11, 1, 46)}
    with pytest.raises(TypeError):
        simplejson.dumps(data)

    assert simplejson.dumps(data, cls=RequestClientJSONEncoder) == simplejson.dumps(
        {'datetime_field': '2024-01-30 11:01:46'},
    )
