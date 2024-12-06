import json
import tempfile
from copy import deepcopy

import pandas as pd
import responses

from fiddler.entities.model import Model
from fiddler.tests.apis.test_files import FILE_ID
from fiddler.tests.constants import PROJECT_ID, URL, USER_EMAIL, USER_ID, USER_NAME

DF = df = pd.DataFrame(
    [
        {'col1': 1, 'col2': 'foo'},
        {'col1': 2, 'col2': 'bar'},
        {'col1': 3, 'col2': 'baz'},
    ]
)

FILE_UPLOAD_200_RESPONSE = {
    'api_version': '3.0',
    'data': {
        'created_at': '2023-11-22 16:50:57.705784',
        'updated_at': '2023-11-22 16:50:57.705784',
        'filename': 'data.parquet',
        'id': FILE_ID,
        'status': 'SUCCESSFUL',
        'type': 'PARQUET',
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
    },
    'kind': 'NORMAL',
}

API_RESPONSE_200 = {
    'api_version': '3.0',
    'kind': 'NORMAL',
    'data': {
        'schema': {
            'schema_version': 1,
            'columns': [
                {
                    'id': 'col1',
                    'name': 'col1',
                    'data_type': 'int',
                    'min': 1,
                    'max': 3,
                    'bins': [
                        1.0,
                        1.2,
                        1.4,
                        1.6,
                        1.8,
                        2.0,
                        2.2,
                        2.4000000000000004,
                        2.6,
                        2.8,
                        3.0,
                    ],
                },
                {
                    'id': 'col2',
                    'name': 'col2',
                    'data_type': 'category',
                    'categories': ['bar', 'baz', 'foo'],
                },
            ],
        },
        'spec': {
            'custom_features': [],
            'decisions': [],
            'inputs': [],
            'metadata': [],
            'outputs': [],
            'schema_version': 1,
            'targets': [],
        },
    },
}

API_REQUEST_BODY = {
    'rows': [
        {'col1': '3', 'col2': 'baz'},
        {'col1': '1', 'col2': 'foo'},
        {'col1': '2', 'col2': 'bar'},
    ]
}


@responses.activate
def test_generate_model_with_dataframe() -> None:
    responses.post(
        url=f'{URL}/v3/files/upload',
        json=FILE_UPLOAD_200_RESPONSE,
    )

    responses.post(
        url=f'{URL}/v3/model-factory',
        json=API_RESPONSE_200,
    )
    model = Model.from_data(source=DF, name='model1', project_id=PROJECT_ID)
    assert isinstance(model, Model)


@responses.activate
def test_generate_model_with_max_cardinality() -> None:
    responses.post(
        url=f'{URL}/v3/files/upload',
        json=FILE_UPLOAD_200_RESPONSE,
    )

    responses.post(
        url=f'{URL}/v3/model-factory',
        json=API_RESPONSE_200,
    )

    max_cardinality = 10
    model = Model.from_data(
        source=DF, name='model1', project_id=PROJECT_ID, max_cardinality=max_cardinality
    )
    assert isinstance(model, Model)

    request = responses.calls[1].request
    assert json.loads(request.body)['max_cardinality'] == max_cardinality


@responses.activate
def test_generate_model_with_csv_file() -> None:
    with tempfile.NamedTemporaryFile(suffix='.csv', mode='w') as temp_file:
        file_upload_response = deepcopy(FILE_UPLOAD_200_RESPONSE)
        file_upload_response['data']['filename'] = temp_file.name
        file_upload_response['data']['type'] = 'CSV'

        responses.post(
            url=f'{URL}/v3/files/upload',
            json=FILE_UPLOAD_200_RESPONSE,
        )

        responses.post(
            url=f'{URL}/v3/model-factory',
            json=API_RESPONSE_200,
        )

        DF.to_csv(temp_file.name, index=False)

        model = Model.from_data(
            source=temp_file.name, name='model1', project_id=PROJECT_ID
        )
        assert isinstance(model, Model)


@responses.activate
def test_generate_model_with_parquet_file() -> None:
    responses.post(
        url=f'{URL}/v3/generate-schema',
        json=API_RESPONSE_200,
    )

    with tempfile.NamedTemporaryFile(suffix='.parquet', mode='wb') as temp_file:
        DF.to_parquet(temp_file.name, index=False)

        file_upload_response = deepcopy(FILE_UPLOAD_200_RESPONSE)
        file_upload_response['data']['filename'] = temp_file.name

        responses.post(
            url=f'{URL}/v3/files/upload',
            json=FILE_UPLOAD_200_RESPONSE,
        )

        responses.post(
            url=f'{URL}/v3/model-factory',
            json=API_RESPONSE_200,
        )

        DF.to_csv(temp_file.name, index=False)

        version = 'v1.0'
        model = Model.from_data(
            source=temp_file.name,
            name='model1',
            version=version,
            project_id=PROJECT_ID,
        )
        assert isinstance(model, Model)
        assert model.version == version
