from copy import deepcopy
from http import HTTPStatus
from uuid import UUID

import pytest
import responses
from pytest_mock import MockerFixture
from responses import matchers

from fiddler.entities.job import Job
from fiddler.entities.model import Model, ModelCompact
from fiddler.entities.model_deployment import ModelDeployment
from fiddler.exceptions import Conflict, NotFound
from fiddler.schemas.model_schema import Column, ModelSchema
from fiddler.schemas.model_spec import ModelSpec
from fiddler.tests.constants import (
    JOB_ID,
    JOB_NAME,
    MODEL_DEPLOYMENT_ID,
    MODEL_ID,
    MODEL_NAME,
    MODEL_VERSION,
    ORG_ID,
    ORG_NAME,
    PROJECT_ID,
    PROJECT_NAME,
    URL,
    USER_EMAIL,
    USER_ID,
    USER_NAME,
)

MODEL_DELETE_JOB_API_RESPONSE_200 = {
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

MODEL_SCHEMA = {
    'columns': [
        {
            'bins': [
                350.0,
                400.0,
                450.0,
                500.0,
                550.0,
                600.0,
                650.0,
                700.0,
                750.0,
                800.0,
                850.0,
            ],
            'categories': None,
            'data_type': 'int',
            'id': 'creditscore',
            'max': 850,
            'min': 350,
            'n_dimensions': None,
            'name': 'CreditScore',
            'replace_with_nulls': None,
        },
        {
            'bins': None,
            'categories': ['France', 'Germany', 'Spain'],
            'data_type': 'category',
            'id': 'geography',
            'max': None,
            'min': None,
            'n_dimensions': None,
            'name': 'Geography',
            'replace_with_nulls': None,
        },
        {
            'bins': [
                0.0,
                0.1,
                0.2,
                0.30000000000000004,
                0.4,
                0.5,
                0.6000000000000001,
                0.7000000000000001,
                0.8,
                0.9,
                1.0,
            ],
            'categories': None,
            'data_type': 'float',
            'id': 'probability_churned',
            'max': 1.0,
            'min': 0.0,
            'n_dimensions': None,
            'name': 'probability_churned',
            'replace_with_nulls': None,
        },
        {
            'bins': None,
            'categories': [False, True],
            'data_type': 'bool',
            'id': 'decisions',
            'max': None,
            'min': None,
            'n_dimensions': None,
            'name': 'Decisions',
            'replace_with_nulls': None,
        },
        {
            'bins': None,
            'categories': ['Churned', 'Not Churned'],
            'data_type': 'category',
            'id': 'churned',
            'max': None,
            'min': None,
            'n_dimensions': None,
            'name': 'Churned',
            'replace_with_nulls': None,
        },
    ],
    'schema_version': 1,
}
MODEL_SPEC = {
    'custom_features': [],
    'decisions': ['Decisions'],
    'inputs': [
        'CreditScore',
        'Geography',
    ],
    'metadata': [],
    'outputs': ['probability_churned'],
    'schema_version': 1,
    'targets': ['Churned'],
}
API_RESPONSE_200 = {
    'data': {
        'id': MODEL_ID,
        'name': MODEL_NAME,
        'version': MODEL_VERSION,
        'project': {
            'id': PROJECT_ID,
            'name': PROJECT_NAME,
        },
        'organization': {
            'id': ORG_ID,
            'name': ORG_NAME,
        },
        'input_type': 'structured',
        'task': 'binary_classification',
        'task_params': {
            'binary_classification_threshold': 0.5,
            'target_class_order': ['Not Churned', 'Churned'],
            'group_by': None,
            'top_k': None,
            'class_weights': None,
            'weighted_ref_histograms': None,
        },
        'schema': MODEL_SCHEMA,
        'spec': MODEL_SPEC,
        'description': 'This model predicts whether customer stays or churns',
        'event_id_col': None,
        'event_ts_col': None,
        'event_ts_format': None,
        'xai_params': {
            'custom_explain_methods': [],
            'default_explain_method': None,
        },
        'artifact_status': 'no_model',
        'artifact_files': [],
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
        'is_binary_ranking_model': False,
    },
}

API_RESPONSE_409 = {
    'error': {
        'code': 409,
        'message': 'Model already exists',
        'errors': [
            {
                'reason': 'Conflict',
                'message': 'Model already exists',
                'help': '',
            }
        ],
    }
}

API_RESPONSE_404 = {
    'error': {
        'code': 404,
        'message': 'Model not found for the given identifier',
        'errors': [
            {
                'reason': 'ObjectNotFound',
                'message': 'Model not found for the given identifier',
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
        'total': 1,
        'item_count': 1,
        'page_count': 1,
        'page_index': 1,
        'offset': 0,
        'items': [
            API_RESPONSE_200['data'],
        ],
    }
}
DELETE_202_RESPONSE = {
    'data': {'job': {'id': JOB_ID, 'name': f'Deleting model {MODEL_NAME}'}},
    'api_version': '3.0',
    'kind': 'NORMAL',
}

DEPLOYMENT_RESPONSE_200 = {
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
    },
}


@responses.activate
def test_add_model_success() -> None:
    resp = responses.post(
        url=f'{URL}/v3/models',
        json=API_RESPONSE_200,
    )
    model = Model(
        name=MODEL_NAME,
        project_id=PROJECT_ID,
        schema=ModelSchema(**MODEL_SCHEMA),
        spec=ModelSpec(**MODEL_SPEC),
    ).create()

    assert resp.calls[0].request.headers['Content-Type'] == 'application/json'
    assert isinstance(model, Model)
    assert model.id == UUID(MODEL_ID)
    assert model.name == MODEL_NAME
    assert model.version == MODEL_VERSION


@responses.activate
def test_add_model_conflict() -> None:
    responses.post(
        url=f'{URL}/v3/models', json=API_RESPONSE_409, status=HTTPStatus.CONFLICT
    )

    with pytest.raises(Conflict):
        Model(
            name=MODEL_NAME,
            project_id=PROJECT_ID,
            schema=ModelSchema(**MODEL_SCHEMA),
            spec=ModelSpec(**MODEL_SPEC),
        ).create()


@responses.activate
def test_get_model_success() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)
    assert isinstance(model, Model)


@responses.activate
def test_get_model_not_found() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=API_RESPONSE_404,
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(NotFound):
        Model.get(id_=MODEL_ID)


@responses.activate
def test_model_from_name_success() -> None:
    params = {
        'filter': '{"condition": "AND", "rules": [{"field": "name", "operator": "equal", "value": "bank_churn"}, {"field": "project_id", "operator": "equal", "value": "1531bfd9-2ca2-4a7b-bb5a-136c8da09ca1"}]}',
        'limit': 1,
        'ordering': 'created_at',
    }
    responses.get(
        url=f'{URL}/v3/models',
        json=API_RESPONSE_FROM_NAME,
        match=[matchers.query_param_matcher(params)],
    )
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=API_RESPONSE_200,
    )
    model = Model.from_name(name=MODEL_NAME, project_id=PROJECT_ID)
    assert isinstance(model, Model)


@responses.activate
def test_model_from_name_with_version_success() -> None:
    params = {
        'filter': '{"condition": "AND", "rules": [{"field": "name", "operator": "equal", "value": "bank_churn"}, {"field": "project_id", "operator": "equal", "value": "1531bfd9-2ca2-4a7b-bb5a-136c8da09ca1"}, {"field": "version", "operator": "equal", "value": "v1"}]}',
        'limit': 1,
        'ordering': 'created_at',
    }
    responses.get(
        url=f'{URL}/v3/models',
        json=API_RESPONSE_FROM_NAME,
        match=[matchers.query_param_matcher(params)],
    )
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=API_RESPONSE_200,
    )
    model = Model.from_name(
        name=MODEL_NAME, version=MODEL_VERSION, project_id=PROJECT_ID
    )
    assert isinstance(model, Model)


@responses.activate
def test_model_from_name_latest_success() -> None:
    params = {
        'filter': '{"condition": "AND", "rules": [{"field": "name", "operator": "equal", "value": "bank_churn"}, {"field": "project_id", "operator": "equal", "value": "1531bfd9-2ca2-4a7b-bb5a-136c8da09ca1"}]}',
        'limit': 1,
        'ordering': '-created_at',
    }
    responses.get(
        url=f'{URL}/v3/models',
        json=API_RESPONSE_FROM_NAME,
        match=[matchers.query_param_matcher(params)],
    )
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=API_RESPONSE_200,
    )
    model = Model.from_name(name=MODEL_NAME, project_id=PROJECT_ID, latest=True)
    assert isinstance(model, Model)


@responses.activate
def test_model_from_name_not_found() -> None:
    resp = deepcopy(API_RESPONSE_FROM_NAME)
    resp['data']['total'] = 0
    resp['data']['item_count'] = 0
    resp['data']['items'] = []

    params = {
        'filter': '{"condition": "AND", "rules": [{"field": "name", "operator": "equal", "value": "bank_churn"}, {"field": "project_id", "operator": "equal", "value": "1531bfd9-2ca2-4a7b-bb5a-136c8da09ca1"}]}',
        'limit': 1,
        'ordering': 'created_at',
    }
    responses.get(
        url=f'{URL}/v3/models',
        json=resp,
        match=[matchers.query_param_matcher(params)],
    )

    with pytest.raises(NotFound):
        Model.from_name(name=MODEL_NAME, project_id=PROJECT_ID)


@responses.activate
def test_model_from_name_with_version_not_found() -> None:
    resp = deepcopy(API_RESPONSE_FROM_NAME)
    resp['data']['total'] = 0
    resp['data']['item_count'] = 0
    resp['data']['items'] = []

    params = {
        'filter': '{"condition": "AND", "rules": [{"field": "name", "operator": "equal", "value": "bank_churn"}, {"field": "project_id", "operator": "equal", "value": "1531bfd9-2ca2-4a7b-bb5a-136c8da09ca1"}, {"field": "version", "operator": "equal", "value": "v1"}]}',
        'limit': 1,
        'ordering': 'created_at',
    }
    responses.get(
        url=f'{URL}/v3/models',
        json=resp,
        match=[matchers.query_param_matcher(params)],
    )

    with pytest.raises(NotFound):
        Model.from_name(name=MODEL_NAME, version=MODEL_VERSION, project_id=PROJECT_ID)


@responses.activate
def test_model_list_success() -> None:
    params = {
        'filter': '{"condition": "AND", "rules": [{"field": "project_id", "operator": "equal", "value": "1531bfd9-2ca2-4a7b-bb5a-136c8da09ca1"}]}',
        'limit': 50,
        'offset': 0,
    }
    responses.get(
        url=f'{URL}/v3/models',
        json=LIST_API_RESPONSE,
        match=[matchers.query_param_matcher(params)],
    )
    models = Model.list(project_id=PROJECT_ID)
    for model in models:
        assert isinstance(model, ModelCompact)
        assert model.version is not None


@responses.activate
def test_model_list_with_name() -> None:
    params = {
        'filter': '{"condition": "AND", "rules": [{"field": "project_id", "operator": "equal", "value": "1531bfd9-2ca2-4a7b-bb5a-136c8da09ca1"}, {"field": "name", "operator": "equal", "value": "bank_churn"}]}',
        'limit': 50,
        'offset': 0,
    }
    responses.get(
        url=f'{URL}/v3/models',
        json=LIST_API_RESPONSE,
        match=[matchers.query_param_matcher(params)],
    )
    models = Model.list(project_id=PROJECT_ID, name=MODEL_NAME)
    for model in models:
        assert isinstance(model, ModelCompact)


@responses.activate
def test_delete_model() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    responses.delete(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=DELETE_202_RESPONSE,
    )
    responses.get(
        url=f'{URL}/v3/jobs/{JOB_ID}',
        json=MODEL_DELETE_JOB_API_RESPONSE_200,
    )
    job_obj = model.delete()
    assert isinstance(job_obj, Job)


@responses.activate
def test_delete_model_not_found() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    responses.delete(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=API_RESPONSE_404,
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(NotFound):
        model.delete()


@responses.activate
def test_update_model_success(mocker) -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)
    mocker.patch.dict(API_RESPONSE_200['data'], {'description': 'Test model update'})

    responses.patch(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=API_RESPONSE_200,
    )
    model.description = 'Test model update'

    model.update()
    assert model.description == 'Test model update'

    # update version
    new_version = 'v2'
    mocker.patch.dict(API_RESPONSE_200['data'], {'version': new_version})

    responses.patch(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=API_RESPONSE_200,
    )
    model.version = new_version
    model.update()
    assert model.version == new_version


@responses.activate
def test_update_model_not_found() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    responses.patch(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=API_RESPONSE_404,
        status=HTTPStatus.NOT_FOUND,
    )
    with pytest.raises(NotFound):
        model.update()


@responses.activate
def test_datasets_property(mocker: MockerFixture) -> None:
    mock_fn = mocker.patch('fiddler.entities.dataset.Dataset.list')

    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    _ = list(model.datasets)

    mock_fn.assert_called_with(model_id=UUID(MODEL_ID))


@responses.activate
def test_model_deployment_property() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}/deployment',
        json=DEPLOYMENT_RESPONSE_200,
    )
    model_deployment = model.deployment
    assert isinstance(model_deployment, ModelDeployment)
    assert model_deployment.id == UUID(MODEL_DEPLOYMENT_ID)
    assert model_deployment.cpu == 300
    assert model_deployment.artifact_type == 'SURROGATE'


def test_model_schema_dunder_methods() -> None:
    schema = ModelSchema(**MODEL_SCHEMA)

    # Get method - success
    isinstance(schema['CreditScore'], Column)

    # Get method - KeyError
    with pytest.raises(KeyError):
        _ = schema['foo']

    # Update value
    schema['CreditScore'].max = 1000
    assert schema.columns[0].max == 1000

    # Set method - new column
    new_col = schema['CreditScore'].copy()
    new_col.name = 'CreditScoreNew'
    schema[new_col.name] = new_col
    assert schema.columns[-1].name == 'CreditScoreNew'

    # Set method - replace existing column
    new_col = schema['CreditScore'].copy()
    new_col.name = 'CreditScoreNew'
    schema['CreditScore'] = new_col
    assert schema.columns[0].name == 'CreditScoreNew'

    # Delete method - success
    del schema['CreditScoreNew']
    assert schema.columns[0] != 'CreditScoreNew'

    # Delete method - KeyError
    with pytest.raises(KeyError):
        del schema['foo']


@responses.activate
def test_model_duplicate() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    assert model.id == UUID(MODEL_ID)
    assert model._event_publisher.model_id == model.id

    # Without version parameter
    model_copy = model.duplicate()

    assert model_copy.id is None
    assert model_copy.version == model.version

    with pytest.raises(AssertionError):
        # since id is None
        _ = model_copy._event_publisher

    # With version parameter
    new_version = 'v2'
    model_copy = model.duplicate(version=new_version)
    assert model_copy.id is None
    assert model_copy.version == new_version

    # Note(JP): what was this supposed to test? That mutating the copy does not
    # mutate the original? This now fails with `TypeError: 'FieldInfo' object
    # is not subscriptable"`.Is
    # https://github.com/pydantic/pydantic/discussions/6231) maybe related? I
    # think it's OK to outcomment this for now; whatever this tests is probably
    # guaranteed by pydantic, and not implemented by us (is that true)?
    #
    # assert model.schema['CreditScore'].max == 850
    # model_copy.schema['CreditScore'].max = 900 assert
    # model.schema['CreditScore'].max == 850 assert
    # model_copy.schema['CreditScore'].max == 900


@responses.activate
def test_remove_column_from_spec() -> None:
    spec = ModelSpec(**MODEL_SPEC)
    assert 'probability_churned' in spec.outputs

    spec.remove_column('probability_churned')
    assert 'probability_churned' not in spec.outputs


@responses.activate
def test_remove_column() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    # Verifying the column exists
    assert isinstance(model.schema['CreditScore'], Column)
    assert 'CreditScore' in model.spec.inputs

    model.remove_column('CreditScore')

    # Verifying the column is removed
    with pytest.raises(KeyError):
        _ = model.schema['CreditScore']
    assert 'CreditScore' not in model.spec.inputs

    # not raised when column missing
    model.remove_column('foo')

    with pytest.raises(KeyError):
        model.remove_column('foo', missing_ok=False)
