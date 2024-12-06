import io
import os
import shutil
from collections import namedtuple

import pandas as pd
import responses

from fiddler.entities.job import Job
from fiddler.entities.model import Model
from fiddler.schemas.xai import DatasetDataSource, RowDataSource
from fiddler.tests.constants import (
    BASE_TEST_DIR,
    DATASET_ID,
    DATASET_NAME,
    JOB_ID,
    MODEL_ID,
    MODEL_NAME,
    MODEL_VERSION,
    ORG_ID,
    ORG_NAME,
    OUTPUT_DIR,
    PROJECT_ID,
    PROJECT_NAME,
    URL,
    USER_EMAIL,
    USER_ID,
    USER_NAME,
)

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
    ],
    'schema_version': 1,
}
MODEL_SPEC = {
    'custom_features': [],
    'decisions': ['Decisions'],
    'inputs': [
        'CreditScore',
    ],
    'metadata': [],
    'outputs': ['probability_churned'],
    'schema_version': 1,
    'targets': ['Churned'],
}
MODEL_API_RESPONSE_200 = {
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
        'input_cols': [
            MODEL_SCHEMA['columns'][0],
            MODEL_SCHEMA['columns'][0],
        ],
        'output_cols': [MODEL_SCHEMA['columns'][0]],
        'target_cols': [MODEL_SCHEMA['columns'][0]],
        'metadata_cols': [],
        'decision_cols': [MODEL_SCHEMA['columns'][0]],
        'is_binary_ranking_model': False,
    },
}

EXPLAIN_RESPONSE_200 = {
    'data': {
        'explanation_type': 'FIDDLER_SHAP',
        'num_permutations': 50,
        'ci_level': 0.95,
        'explanations': {
            'probability_churned': {
                'model_prediction': 0.40507614012286625,
                'baseline_prediction': 0.19293562908483303,
                'GEM': {
                    'type': 'container',
                    'contents': [
                        {
                            'type': 'simple',
                            'feature-name': 'CreditScore',
                            'value': 619,
                            'attribution': -0.022117800470630538,
                            'attribution-uncertainty': 0.006245936205277383,
                        },
                        {
                            'type': 'simple',
                            'feature-name': 'Geography',
                            'value': 'France',
                            'attribution': 0.028808698749482956,
                            'attribution-uncertainty': 0.008490776240161464,
                        },
                        {
                            'type': 'simple',
                            'feature-name': 'Gender',
                            'value': 'Female',
                            'attribution': 0.059352095878178614,
                            'attribution-uncertainty': 0.010825591198269912,
                        },
                        {
                            'type': 'simple',
                            'feature-name': 'Age',
                            'value': 42,
                            'attribution': 0.04663932271153231,
                            'attribution-uncertainty': 0.026679728117630943,
                        },
                        {
                            'type': 'simple',
                            'feature-name': 'Tenure',
                            'value': 2,
                            'attribution': 0.012244800190215574,
                            'attribution-uncertainty': 0.006979182051724819,
                        },
                        {
                            'type': 'simple',
                            'feature-name': 'Balance',
                            'value': 0.0,
                            'attribution': 0.08161626352219709,
                            'attribution-uncertainty': 0.017052188444913206,
                        },
                        {
                            'type': 'simple',
                            'feature-name': 'NumOfProducts',
                            'value': 1,
                            'attribution': 0.038190793675380155,
                            'attribution-uncertainty': 0.0582498509252494,
                        },
                        {
                            'type': 'simple',
                            'feature-name': 'HasCrCard',
                            'value': 'Yes',
                            'attribution': 0.00654585439939201,
                            'attribution-uncertainty': 0.004515983491581958,
                        },
                        {
                            'type': 'simple',
                            'feature-name': 'IsActiveMember',
                            'value': 'Yes',
                            'attribution': -0.05122940826721414,
                            'attribution-uncertainty': 0.013359099976724447,
                        },
                        {
                            'type': 'simple',
                            'feature-name': 'EstimatedSalary',
                            'value': 101348.88,
                            'attribution': 0.012089890649499193,
                            'attribution-uncertainty': 0.004951759795660022,
                        },
                    ],
                    'attribution': 0.21214051103803322,
                },
            },
        },
        'num_refs': 30,
    },
    'api_version': '3.0',
    'kind': 'NORMAL',
}


PREDICT_RESPONSE_200 = {
    'data': {'predictions': [{'predicted_quality': 5.759617514660622}]},
    'api_version': '3.0',
    'kind': 'NORMAL',
}

FEATURE_IMPORTANCE_RESPONSE_200 = {
    'data': {
        'loss': 'pointwise_logloss',
        'num_refs': 10000,
        'ci_level': 0.5,
        'mean_loss': 0.35653354054994635,
        'mean_loss_ci': 0.09459192835065221,
        'feature_names': [
            'CreditScore',
            'Geography',
            'Gender',
            'Age',
            'Tenure',
            'Balance',
            'NumOfProducts',
            'HasCrCard',
            'IsActiveMember',
            'EstimatedSalary',
        ],
        'mean_loss_increase_importance': [
            0.004429064308612665,
            0.11303687040447762,
            0.010247568997879158,
            0.20021169408760484,
            0.020512200372182397,
            0.36803439130037513,
            0.2339702870224178,
            0.0014671647143862244,
            0.022758435725508515,
            0.011785520720929346,
        ],
        'random_sample_ci': [
            0.00021145873961269672,
            0.0012444603359610608,
            0.00022339657233601845,
            0.0016025718376113422,
            0.00020151632282746737,
            0.0018154124659677064,
            0.0021341170223544335,
            0.00016283332959968953,
            0.0010258365777659855,
            0.0002324089593535596,
        ],
        'fixed_sample_ci': [
            0.00018964651570488745,
            0.0010810129244220677,
            0.0001612062857999329,
            0.001333218784229577,
            0.000139368878515909,
            0.001191577806041505,
            0.0014415377334894384,
            8.741009867015967e-05,
            0.0007286815550017811,
            0.00019660620632828166,
        ],
        'total_input_samples': 3,
        'valid_input_samples': 3,
        'model_task': 'BINARY_CLASSIFICATION',
        'model_input_type': 'TABULAR',
        'env_id': 'a6385884-4970-4eeb-b8cc-36ce9746cd5e',
        'env_name': DATASET_NAME,
        'created_at': '2023-11-22 16:50:57.705784',
    },
    'api_version': '3.0',
    'kind': 'NORMAL',
}

FEATURE_IMPACT_RESPONSE_200 = {
    'data': {
        'num_inputs': 3,
        'num_refs': 10000,
        'ci_level': 0.5,
        'mean_prediction': 0.08983428988388353,
        'mean_prediction_ci': 0.006687591607821416,
        'feature_names': [
            'CreditScore',
            'Geography',
            'Gender',
            'Age',
            'Tenure',
            'Balance',
            'NumOfProducts',
            'HasCrCard',
            'IsActiveMember',
            'EstimatedSalary',
        ],
        'mean_abs_prediction_change_impact': [
            0.00712590582097325,
            0.04386081743167407,
            0.01618882705936992,
            0.09012170216686392,
            0.003203886657934025,
            0.034259594581994,
            0.03950092221577272,
            0.0008308543417424118,
            0.09500517056814688,
            0.015902298170793795,
        ],
        'random_sample_ci': [
            9.460265530465104e-05,
            0.0004967738708175746,
            0.0001390532937646932,
            0.001011710786484173,
            3.2151564756512305e-05,
            0.0003379320087881252,
            0.0007824117094712736,
            6.632377333582839e-06,
            0.001290117285928614,
            0.0001246149963496527,
        ],
        'fixed_sample_ci': [
            9.387290704313362e-05,
            0.00047072988314235967,
            0.00011810560126585543,
            0.0009869435854980898,
            2.6313946023718767e-05,
            0.0003171540654523467,
            0.0007768114901140053,
            5.596843413373775e-06,
            0.001029967633853864,
            0.00011703590760866858,
        ],
        'model_task': 'BINARY_CLASSIFICATION',
        'model_input_type': 'TABULAR',
        'env_id': 'a6385884-4970-4eeb-b8cc-36ce9746cd5e',
        'env_name': DATASET_NAME,
        'created_at': '2023-11-22 16:50:57.705784',
    },
    'api_version': '3.0',
    'kind': 'NORMAL',
}

PRECOMPUTE_FEATURE_IMPACT_202_RESPONSE = {
    'data': {'job': {'id': JOB_ID, 'name': 'Pre-compute feature impact'}},
    'api_version': '3.0',
    'kind': 'NORMAL',
}
PRECOMPUTE_FEATURE_IMPACT_JOB_API_RESPONSE_200 = {
    'api_version': '3.0',
    'kind': 'NORMAL',
    'data': {
        'name': 'Pre-compute feature impact',
        'id': JOB_ID,
        'info': {
            'resource_type': 'MODEL',
            'resource_name': 'bank_churn',
            'project_name': 'bank_churn',
        },
        'status': 'SUCCESS',
        'progress': 100.0,
        'error_message': None,
        'error_reason': None,
    },
}

PRECOMPUTE_FEATURE_IMPORTANCE_202_RESPONSE = {
    'data': {'job': {'id': JOB_ID, 'name': 'Pre-compute feature importance'}},
    'api_version': '3.0',
    'kind': 'NORMAL',
}
PRECOMPUTE_FEATURE_IMPORTANCE_JOB_API_RESPONSE_200 = {
    'api_version': '3.0',
    'kind': 'NORMAL',
    'data': {
        'name': 'Pre-compute feature importance',
        'id': JOB_ID,
        'info': {
            'resource_type': 'MODEL',
            'resource_name': 'bank_churn',
            'project_name': 'bank_churn',
        },
        'status': 'SUCCESS',
        'progress': 100.0,
        'error_message': None,
        'error_reason': None,
    },
}

USER_FEATURE_IMPACT_RESPONSE_200 = {
    'data': {
        'feature_names': [
            'creditscore',
            'geography',
            'gender',
            'age',
            'tenure',
            'balance',
            'numofproducts',
            'hascrcard',
            'isactivemember',
            'estimatedsalary',
        ],
        'feature_impact_scores': [
            0.011580908964862443,
            0.006309520155042726,
            0.007567492652213872,
            0.00477455398879517,
            0.00026155170582271506,
            0.0,
            0.0032795830224845025,
            0.000988697882581393,
            0.0,
            0.0022799670889706025,
        ],
        'system_generated': False,
        'model_task': 'BINARY_CLASSIFICATION',
        'model_input_type': 'TABULAR',
        'created_at': '2024-06-26 09:34:13.120418+00:00',
    },
    'api_version': '3.0',
    'kind': 'NORMAL',
}

PRECOMPUTE_PREDICTIONS_202_RESPONSE = {
    'data': {'job': {'id': JOB_ID, 'name': 'Pre-compute predictions'}},
    'api_version': '3.0',
    'kind': 'NORMAL',
}

PRECOMPUTE_PREDICTIONS_JOB_API_RESPONSE_200 = {
    'api_version': '3.0',
    'kind': 'NORMAL',
    'data': {
        'name': 'Pre-compute predictions',
        'id': JOB_ID,
        'info': {
            'resource_type': 'MODEL',
            'resource_name': 'bank_churn',
            'project_name': 'bank_churn',
        },
        'status': 'SUCCESS',
        'progress': 100.0,
        'error_message': None,
        'error_reason': None,
    },
}

FEATURE_IMPACT_MAP = {
    'creditscore': 0.011580908964862443,
    'geography': 0.006309520155042726,
    'gender': 0.007567492652213872,
    'age': 0.00477455398879517,
    'tenure': 0.00026155170582271506,
    'balance': 0.0,
    'numofproducts': 0.0032795830224845025,
    'hascrcard': 0.000988697882581393,
    'isactivemember': 0.0,
    'estimatedsalary': 0.0022799670889706025,
}


@responses.activate
def test_explain() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    responses.post(
        url=f'{URL}/v3/explain',
        json=EXPLAIN_RESPONSE_200,
    )
    explain_result = model.explain(
        input_data_source=RowDataSource(
            row={
                'CreditScore': 619,
                'Geography': 'France',
                'Gender': 'Female',
                'Age': 42,
                'Tenure': 2,
                'Balance': 0.0,
                'NumOfProducts': 1,
                'HasCrCard': 'Yes',
                'IsActiveMember': 'Yes',
                'EstimatedSalary': 101348.88,
            },
        ),
        ref_data_source=DatasetDataSource(
            env_type='PRODUCTION',
        ),
    )
    assert explain_result == namedtuple('Explain', EXPLAIN_RESPONSE_200['data'])(
        **EXPLAIN_RESPONSE_200['data']
    )



@responses.activate
def test_download_data() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    parquet_path = os.path.join(OUTPUT_DIR, 'test_slice_download.parquet')
    parquet_output = os.path.join(BASE_TEST_DIR, 'slice_test_dir')
    with open(parquet_path, 'rb') as parquet_file:
        data = io.BufferedReader(parquet_file)
        responses.post(
            url=f'{URL}/v3/analytics/download-slice-data',
            body=data,
        )
        expected_df = pd.DataFrame({'Age': [38, 57, 42]})
        model.download_data(
            output_dir=parquet_output,
            env_type='PRE_PRODUCTION',
            env_id=DATASET_ID,
            segment_definition='Age >= 20',
            columns=['Age'],
            max_rows=3,
        )
        slice_df = pd.read_parquet(parquet_path)
        pd.testing.assert_frame_equal(expected_df, slice_df)
    shutil.rmtree(str(parquet_output))




@responses.activate
def test_predict() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    responses.post(
        url=f'{URL}/v3/predict',
        json=PREDICT_RESPONSE_200,
    )
    data = {
        'row_id': 1109,
        'fixed acidity': 10.8,
        'volatile acidity': 0.47,
        'citric acid': 0.43,
        'residual sugar': 2.1,
        'chlorides': 0.171,
        'free sulfur dioxide': 27.0,
        'total sulfur dioxide': 66.0,
        'density': 0.9982,
        'pH': 3.17,
        'sulphates': 0.76,
        'alcohol': 10.8,
    }
    df = pd.DataFrame(data, index=data.keys())
    predictions = model.predict(df=df)

    expected_result = pd.DataFrame(PREDICT_RESPONSE_200['data']['predictions'])
    pd.testing.assert_frame_equal(predictions, expected_result)


@responses.activate
def test_get_feature_impact() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    responses.post(
        url=f'{URL}/v3/analytics/feature-impact',
        json=FEATURE_IMPACT_RESPONSE_200,
    )
    feature_impact = model.get_feature_impact(
        data_source=DatasetDataSource(
            env_type='PRE-PRODUCTION',
            env_id=DATASET_ID,
        ),
    )

    assert feature_impact == namedtuple(
        'FeatureImpact', FEATURE_IMPACT_RESPONSE_200['data']
    )(**FEATURE_IMPACT_RESPONSE_200['data'])


@responses.activate
def test_get_feature_importance() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    responses.post(
        url=f'{URL}/v3/analytics/feature-importance',
        json=FEATURE_IMPORTANCE_RESPONSE_200,
    )
    feature_importance = model.get_feature_importance(
        data_source=DatasetDataSource(
            env_type='PRE-PRODUCTION',
            env_id=DATASET_ID,
        ),
    )

    assert feature_importance == namedtuple(
        'FeatureImportance', FEATURE_IMPORTANCE_RESPONSE_200['data']
    )(**FEATURE_IMPORTANCE_RESPONSE_200['data'])


@responses.activate
def test_precompute_feature_impact() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    responses.post(
        url=f'{URL}/v3/analytics/precompute-feature-impact',
        json=PRECOMPUTE_FEATURE_IMPACT_202_RESPONSE,
    )
    responses.get(
        url=f'{URL}/v3/jobs/{JOB_ID}',
        json=PRECOMPUTE_FEATURE_IMPACT_JOB_API_RESPONSE_200,
    )

    job_obj = model.precompute_feature_impact(dataset_id=DATASET_ID, update=False)
    assert isinstance(job_obj, Job)


@responses.activate
def test_update_precompute_feature_impact() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    responses.put(
        url=f'{URL}/v3/analytics/precompute-feature-impact',
        json=PRECOMPUTE_FEATURE_IMPACT_202_RESPONSE,
    )
    responses.get(
        url=f'{URL}/v3/jobs/{JOB_ID}',
        json=PRECOMPUTE_FEATURE_IMPACT_JOB_API_RESPONSE_200,
    )

    job_obj = model.precompute_feature_impact(dataset_id=DATASET_ID, update=True)
    assert isinstance(job_obj, Job)


@responses.activate
def test_precompute_feature_importance() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    responses.post(
        url=f'{URL}/v3/analytics/precompute-feature-importance',
        json=PRECOMPUTE_FEATURE_IMPORTANCE_202_RESPONSE,
    )
    responses.get(
        url=f'{URL}/v3/jobs/{JOB_ID}',
        json=PRECOMPUTE_FEATURE_IMPORTANCE_JOB_API_RESPONSE_200,
    )

    job_obj = model.precompute_feature_importance(dataset_id=DATASET_ID, update=False)
    assert isinstance(job_obj, Job)


@responses.activate
def test_update_precompute_feature_importance() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    responses.put(
        url=f'{URL}/v3/analytics/precompute-feature-importance',
        json=PRECOMPUTE_FEATURE_IMPORTANCE_202_RESPONSE,
    )
    responses.get(
        url=f'{URL}/v3/jobs/{JOB_ID}',
        json=PRECOMPUTE_FEATURE_IMPORTANCE_JOB_API_RESPONSE_200,
    )

    job_obj = model.precompute_feature_importance(dataset_id=DATASET_ID, update=True)
    assert isinstance(job_obj, Job)


@responses.activate
def test_get_precomputed_feature_importance() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    responses.post(
        url=f'{URL}/v3/analytics/feature-importance/precomputed',
        json=FEATURE_IMPORTANCE_RESPONSE_200,
    )
    assert model.get_precomputed_feature_importance() == namedtuple(
        'FeatureImportance', FEATURE_IMPORTANCE_RESPONSE_200['data']
    )(**FEATURE_IMPORTANCE_RESPONSE_200['data'])


@responses.activate
def test_get_precomputed_feature_impact() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    responses.post(
        url=f'{URL}/v3/analytics/feature-impact/precomputed',
        json=FEATURE_IMPACT_RESPONSE_200,
    )
    assert model.get_precomputed_feature_impact() == namedtuple(
        'FeatureImpact', FEATURE_IMPACT_RESPONSE_200['data']
    )(**FEATURE_IMPACT_RESPONSE_200['data'])


@responses.activate
def test_precompute_predictions() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    responses.post(
        url=f'{URL}/v3/analytics/precompute-predictions',
        json=PRECOMPUTE_PREDICTIONS_202_RESPONSE,
    )
    responses.get(
        url=f'{URL}/v3/jobs/{JOB_ID}',
        json=PRECOMPUTE_PREDICTIONS_JOB_API_RESPONSE_200,
    )

    job_obj = model.precompute_predictions(dataset_id=DATASET_ID, update=False)
    assert isinstance(job_obj, Job)


@responses.activate
def test_update_precompute_predictions() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    responses.put(
        url=f'{URL}/v3/analytics/precompute-predictions',
        json=PRECOMPUTE_PREDICTIONS_202_RESPONSE,
    )
    responses.get(
        url=f'{URL}/v3/jobs/{JOB_ID}',
        json=PRECOMPUTE_PREDICTIONS_JOB_API_RESPONSE_200,
    )

    job_obj = model.precompute_predictions(dataset_id=DATASET_ID, update=True)
    assert isinstance(job_obj, Job)


@responses.activate
def test_upload_feature_impact() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    responses.post(
        url=f'{URL}/v3/analytics/upload-feature-impact',
        json=USER_FEATURE_IMPACT_RESPONSE_200,
    )
    assert (
        model.upload_feature_impact(feature_impact_map=FEATURE_IMPACT_MAP)
        == USER_FEATURE_IMPACT_RESPONSE_200['data']
    )


@responses.activate
def test_update_feature_impact() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )
    model = Model.get(id_=MODEL_ID)

    responses.put(
        url=f'{URL}/v3/analytics/upload-feature-impact',
        json=USER_FEATURE_IMPACT_RESPONSE_200,
    )
    assert (
        model.upload_feature_impact(feature_impact_map=FEATURE_IMPACT_MAP, update=True)
        == USER_FEATURE_IMPACT_RESPONSE_200['data']
    )
