from __future__ import annotations

import os
import logging
from collections import namedtuple
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from uuid import UUID

import pandas as pd

from fiddler.constants.dataset import EnvType
from fiddler.constants.xai import (
    DEFAULT_DOWNLOAD_CHUNK_SIZE,
    DownloadFormat,
    ExplainMethod,
)
from fiddler.decorators import handle_api_error
from fiddler.entities.job import Job
from fiddler.exceptions import Unsupported
from fiddler.schemas.job import JobCompactResp
from fiddler.schemas.xai import DatasetDataSource, EventIdDataSource, RowDataSource
from fiddler.utils.decorators import check_version


logger = logging.getLogger(__name__)


class XaiMixin:
    id: UUID | None
    _client: Callable

    def _get_method(self, update: bool = False) -> Callable:
        """Get HTTP method"""
        return self._client().put if update else self._client().post

    @handle_api_error
    def explain(  # pylint: disable=too-many-arguments
        self,
        input_data_source: RowDataSource | EventIdDataSource,
        ref_data_source: DatasetDataSource | None = None,
        method: ExplainMethod | str = ExplainMethod.FIDDLER_SHAP,
        num_permutations: int | None = None,
        ci_level: float | None = None,
        top_n_class: int | None = None,
    ) -> tuple:
        """
        Get explanation for a single observation.

        :param input_data_source: DataSource for the input data to compute explanation
            on (RowDataSource, EventIdDataSource)
        :param ref_data_source: Dataset data source for the reference data to compute explanation
            on.
            Only used for non-text models and the following methods:
            'SHAP', 'FIDDLER_SHAP', 'PERMUTE', 'MEAN_RESET'
        :param method: Explanation method name. Could be your custom
            explanation method or one of the following method:
            'SHAP', 'FIDDLER_SHAP', 'IG', 'PERMUTE', 'MEAN_RESET', 'ZERO_RESET'
        :param num_permutations: For Fiddler SHAP, that corresponds to the number of
            coalitions to sample to estimate the Shapley values of each single-reference
             game. For the permutation algorithms, this corresponds to the number
            of permutations from the dataset to use for the computation.
        :param ci_level: The confidence level (between 0 and 1) to use for the
            confidence intervals in Fiddler SHAP. Not used for other methods.
        :param top_n_class: For multiclass classification models only, specifying if
            only the n top classes are computed or all classes (when parameter is None)

        :return: A named tuple with the explanation results.
        """
        self._check_id_attributes()
        payload: dict[str, Any] = {
            'model_id': self.id,
            'input_data_source': input_data_source.dict(),
            'explanation_type': method,
        }
        if ref_data_source:
            payload['ref_data_source'] = ref_data_source.dict(exclude_none=True)
        if num_permutations:
            payload['num_permutations'] = num_permutations
        if ci_level:
            payload['ci_level'] = ci_level
        if top_n_class:
            payload['top_n_class'] = top_n_class

        response = self._client().post(
            url='v3/explain', data=payload, headers={'Content-Type': 'application/json'}
        )

        return namedtuple('Explain', response.json()['data'])(**response.json()['data'])

    @handle_api_error
    def get_slice(
        self,
        query: str,
        sample: bool = False,
        max_rows: int | None = None,
        columns: list[str] | None = None,
    ) -> None:
        """
        Fetch data with slice query.

        :param query: An SQL query that begins with the keyword 'SELECT'
        :param columns: Allows caller to explicitly specify list of
                        columns to select overriding columns selected in the query.
        :param max_rows: Number of maximum rows to fetch
        :param sample: Whether rows should be sample or not from the database
        :return: Dataframe of the query output
        """
        raise Unsupported(
            'This method is not supported since version 3.4. Please use `model.download_data` instead.'
        )

    @handle_api_error
    def download_data(  # pylint: disable=too-many-arguments
        self,
        output_dir: Path | str,
        env_type: EnvType,
        env_id: UUID | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        segment_id: UUID | None = None,
        segment_definition: UUID | None = None,
        max_rows: int | None = None,
        columns: list[str] | None = None,
        chunk_size: int | None = DEFAULT_DOWNLOAD_CHUNK_SIZE,
        fetch_vectors: bool | None = None,
        output_format: DownloadFormat = DownloadFormat.PARQUET,
    ) -> None:
        """
        Download data with a slice data configuration to PARQUET or CSV file.

        :param output_dir: Path to download the file
        :param env_type: Type of environment to query (PRODUCTION or PRE_PRODUCTION)
        :param env_id: If PRE_PRODUCTION env selected, provide the uuid of the dataset to query
        :param start_time: Start time to retrieve data, only for PRODUCTION env. If not time zone is indicated, we will infer UTC time zone.
        :param start_time: End time to retrieve data, only for PRODUCTION env. If not time zone is indicated, we will infer UTC time zone.
        :param segment_id: Optional segment UUID to query data using a saved segment associated with the model
        :param segment_definition: Optional segment FQL definition to query data using an applied segment. This segment will not be saved to the model.
        :param columns: Allows caller to explicitly specify list of columns to retrieve. Default to None which fetch all columns from the model.
        :param max_rows: Number of maximum rows to fetch
        :param chunk_size: Number of rows per chunk to download data. Default to 1000. You can increase that number for faster download if you query less than 1000 columns and don't have vector columns.
        :param fetch_vectors: Whether the vectors columns are fetched or not. Default to False.
        :param output_format: Format indicating if the result should be a CSV file or a PARQUET file. Default to PARQUET file.
        """
        self._check_id_attributes()

        output_dir = Path(output_dir)
        if not output_dir.exists():
            os.makedirs(output_dir)

        payload: dict[str, Any] = {
            'model_id': self.id,
            'env_type': env_type,
            'csv': output_format == DownloadFormat.CSV,
            'column_names': columns,
        }
        if env_id:
            payload['env_id'] = env_id
        if start_time or end_time:
            payload['time_filter'] = {
                'start_time': start_time.astimezone(timezone.utc).strftime(
                    '%Y-%m-%d %H:%M:%S'
                )
                if start_time
                else None,
                'end_time': end_time.astimezone(timezone.utc).strftime(
                    '%Y-%m-%d %H:%M:%S'
                )
                if end_time
                else None,
                'time_zone': 'UTC',
            }

        if segment_id or segment_definition:
            payload['segment'] = {'id': segment_id, 'definition': segment_definition}

        if max_rows:
            payload['num_samples'] = max_rows

        if chunk_size:
            payload['chunk_size'] = chunk_size

        if fetch_vectors:
            payload['fetch_vectors'] = fetch_vectors

        file_path = os.path.join(
            output_dir,
            'output.csv' if output_format == DownloadFormat.CSV else 'output.parquet',
        )

        with self._client().post(
            url='/v3/analytics/download-slice-data',
            data=payload,
            headers={'Content-Type': 'application/json'},
        ) as resp:
            # Download file
            with open(file_path, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)

        logger.info(
            'Data succesfully downloaded',
        )

    @handle_api_error
    def download_slice(  # pylint: disable=too-many-arguments
        self,
        output_dir: Path | str,
        query: str,
        sample: bool = False,
        max_rows: int | None = None,
        columns: list[str] | None = None,
    ) -> None:
        """
        Download data with slice query to parquet file.

        :param output_dir: Path to download the file
        :param query: An SQL query that begins with the keyword 'SELECT'
        :param columns: Allows caller to explicitly specify list of
                        columns to select overriding columns selected in the query.
        :param max_rows: Number of maximum rows to fetch
        :param sample: Whether rows should be sample or not from the database
        """
        raise Unsupported(
            'This method is not supported since version 3.4. Please use `model.download_data` instead.'
        )

    @handle_api_error
    def get_mutual_info(
        self,
        query: str,
        column_name: str,
        num_samples: int | None = None,
        normalized: bool = False,
    ) -> None:
        """
        Get mutual information.

        The Mutual information measures the dependency between
        two random variables. It's a non-negative value. If two random variables are
        independent MI is equal to zero. Higher MI values means higher dependency.

        :param query: slice query to compute Mutual information on
        :param column_name: column name to compute mutual information with respect to
               all the variables in the dataset.
        :param num_samples: Number of samples to select for computation
        :param normalized: If set to True, it will compute Normalized Mutual Information
        :return: a dictionary of mutual information w.r.t the given feature
                 for each column given
        """
        raise Unsupported('This method is not supported since version 3.4.')

    @handle_api_error
    def predict(
        self,
        df: pd.DataFrame,
        chunk_size: int | None = None,
    ) -> pd.DataFrame:
        """
        Run model on an input dataframe.

        :param df: Feature dataframe
        :param chunk_size: Chunk size for fetching predictions

        :return: Dataframe of the predictions
        """
        self._check_id_attributes()

        payload: dict[str, Any] = {
            'model_id': self.id,
            'data': df.to_dict('records'),
        }
        if chunk_size:
            payload['chunk_size'] = chunk_size

        response = self._client().post(
            url='/v3/predict',
            data=payload,
            headers={'Content-Type': 'application/json'},
        )
        return pd.DataFrame(response.json()['data']['predictions'])

    @handle_api_error
    def get_feature_impact(  # pylint: disable=too-many-arguments
        self,
        data_source: DatasetDataSource,
        num_iterations: int | None = None,
        num_refs: int | None = None,
        ci_level: float | None = None,
        min_support: int | None = None,
        output_columns: list[str] | None = None,
    ) -> tuple:
        """
        Get global feature impact for a model over a dataset or a slice.

        :param data_source: Dataset data Source for the input dataset to compute feature
            impact on
        :param num_iterations: The maximum number of ablated model inferences per feature
        :param num_refs: The number of reference points used in the explanation
        :param ci_level: The confidence level (between 0 and 1)
        :param min_support: Only used for NLP (TEXT inputs) models. Specify a minimum
            support (number of times a specific word was present in the sample data)
            to retrieve top words. Default to 15.
        :param output_columns: Only used for NLP (TEXT inputs) models. Output column
            names to compute feature impact on.

        :return: Feature Impact tuple
        """

        self._check_id_attributes()

        payload: dict[str, Any] = {
            'model_id': self.id,
            'data_source': data_source.dict(exclude_none=True),
        }

        if num_refs:
            payload['num_refs'] = num_refs
        if num_iterations:
            payload['num_iterations'] = num_iterations
        if ci_level:
            payload['ci_level'] = ci_level
        if min_support:
            payload['min_support'] = min_support
        if output_columns:
            payload['output_columns'] = output_columns

        response = self._client().post(
            url='/v3/analytics/feature-impact',
            data=payload,
            headers={'Content-Type': 'application/json'},
        )

        return namedtuple('FeatureImpact', response.json()['data'])(
            **response.json()['data']
        )

    @handle_api_error
    def get_feature_importance(  # pylint: disable=too-many-arguments
        self,
        data_source: DatasetDataSource,
        num_iterations: int | None = None,
        num_refs: int | None = None,
        ci_level: float | None = None,
    ) -> tuple:
        """
        Get global feature importance for a model over a dataset or a slice.

        :param data_source: Dataset data aSource for the input dataset to compute feature
            importance on
        :param num_iterations: The maximum number of ablated model inferences per feature
        :param num_refs: The number of reference points used in the explanation
        :param ci_level: The confidence level (between 0 and 1)

        :return: Feature Importance tuple
        """

        self._check_id_attributes()

        payload: dict[str, Any] = {
            'model_id': self.id,
            'data_source': data_source.dict(),
        }

        if num_refs:
            payload['num_refs'] = num_refs
        if num_iterations:
            payload['num_iterations'] = num_iterations
        if ci_level:
            payload['ci_level'] = ci_level

        response = self._client().post(
            url='/v3/analytics/feature-importance',
            data=payload,
            headers={'Content-Type': 'application/json'},
        )

        return namedtuple('FeatureImportance', response.json()['data'])(
            **response.json()['data']
        )

    @handle_api_error
    def precompute_feature_impact(  # pylint: disable=too-many-arguments
        self,
        dataset_id: UUID | str,
        num_samples: int | None = None,
        num_iterations: int | None = None,
        num_refs: int | None = None,
        ci_level: float | None = None,
        min_support: int | None = None,
        update: bool = False,
    ) -> Job:
        """Pre-compute feature impact for a model on a dataset.

        This is used in various places in the UI.
        A single feature impact can be precomputed (computed and cached) for a model.

        :param dataset_id: The unique identifier of the dataset
        :param num_samples: The number of samples used
        :param num_iterations: The maximum number of ablated model inferences per feature
        :param num_refs: The number of reference points used in the explanation
        :param ci_level: The confidence level (between 0 and 1)
        :param min_support: Only used for NLP (TEXT inputs) models. Specify a minimum
            support (number of times a specific word was present in the sample data)
            to retrieve top words. Default to 15.
        :param update: Whether the precomputed feature impact should be recomputed and updated

        :return: Async Job
        """

        self._check_id_attributes()

        payload: dict[str, Any] = {
            'model_id': self.id,
            'env_id': dataset_id,
            'env_type': EnvType.PRE_PRODUCTION,
        }
        if num_samples:
            payload['num_samples'] = num_samples
        if num_refs:
            payload['num_refs'] = num_refs
        if num_iterations:
            payload['num_iterations'] = num_iterations
        if ci_level:
            payload['ci_level'] = ci_level
        if min_support:
            payload['min_support'] = min_support

        method = self._get_method(update)

        response = method(
            url='/v3/analytics/precompute-feature-impact',
            data=payload,
            headers={'Content-Type': 'application/json'},
        )

        job_compact = JobCompactResp(**response.json()['data']['job'])
        logger.info(
            'Model[%s] - Submitted job (%s) for precomputing feature impact',
            self.id,
            job_compact.id,
        )
        return Job.get(id_=job_compact.id)

    @handle_api_error
    def precompute_feature_importance(  # pylint: disable=too-many-arguments
        self,
        dataset_id: UUID | str,
        num_samples: int | None = None,
        num_iterations: int | None = None,
        num_refs: int | None = None,
        ci_level: float | None = None,
        update: bool = False,
    ) -> Job:
        """Pre-compute feature importance for a model on a dataset.

        This is used in various places in the UI.
        A single feature importance can be precomputed (computed and cached) for a model.

        :param dataset_id: The unique identifier of the dataset
        :param num_samples: The number of samples used
        :param num_iterations: The maximum number of ablated model inferences per feature
        :param num_refs: The number of reference points used in the explanation
        :param ci_level: The confidence level (between 0 and 1)
        :param update: Whether the precomputed feature impact should be recomputed and updated

        :return: Async Job
        """

        self._check_id_attributes()

        payload: dict[str, Any] = {
            'model_id': self.id,
            'env_id': dataset_id,
            'env_type': EnvType.PRE_PRODUCTION,
        }
        if num_samples:
            payload['num_samples'] = num_samples
        if num_refs:
            payload['num_refs'] = num_refs
        if num_iterations:
            payload['num_iterations'] = num_iterations
        if ci_level:
            payload['ci_level'] = ci_level

        method = self._get_method(update)

        response = method(
            url='/v3/analytics/precompute-feature-importance',
            data=payload,
            headers={'Content-Type': 'application/json'},
        )

        job_compact = JobCompactResp(**response.json()['data']['job'])
        logger.info(
            'Model[%s] - Submitted job (%s) for precomputing feature importance',
            self.id,
            job_compact.id,
        )
        return Job.get(id_=job_compact.id)

    @handle_api_error
    def get_precomputed_feature_importance(self) -> tuple:
        """Get precomputed feature importance for a model"""

        self._check_id_attributes()
        response = self._client().post(
            url='/v3/analytics/feature-importance/precomputed',
            data={'model_id': self.id},
            headers={'Content-Type': 'application/json'},
        )

        return namedtuple('FeatureImportance', response.json()['data'])(
            **response.json()['data']
        )

    @handle_api_error
    def get_precomputed_feature_impact(self) -> tuple:
        """Get precomputed feature impact for a model"""

        self._check_id_attributes()
        response = self._client().post(
            url='/v3/analytics/feature-impact/precomputed',
            data={'model_id': self.id},
            headers={'Content-Type': 'application/json'},
        )

        return namedtuple('FeatureImpact', response.json()['data'])(
            **response.json()['data']
        )

    @handle_api_error
    def precompute_predictions(
        self,
        dataset_id: UUID | str,
        chunk_size: int | None = None,
        update: bool = False,
    ) -> Job:
        """
        Pre-compute predictions for a model on a dataset

        :param dataset_id: The unique identifier of the dataset
        :param chunk_size: Chunk size for fetching predictions
        :param update: Whether the pre-computed predictions should be re-computed and updated for this dataset

        :return: Dataframe of the predictions
        """
        self._check_id_attributes()

        payload: dict[str, Any] = {
            'model_id': self.id,
            'env_id': dataset_id,
        }

        if chunk_size:
            payload['batch_size'] = chunk_size

        method = self._get_method(update)

        response = method(
            url='/v3/analytics/precompute-predictions',
            data=payload,
            headers={'Content-Type': 'application/json'},
        )

        job_compact = JobCompactResp(**response.json()['data']['job'])
        logger.info(
            'Model[%s] - Submitted job (%s) for precomputing predictions on dataset[%s]',
            self.id,
            job_compact.id,
            dataset_id,
        )
        return Job.get(id_=job_compact.id)

    def _check_id_attributes(self) -> None:
        if not self.id:
            raise AttributeError(
                'This method is available only for model object generated from '
                'API response.'
            )

    @check_version(version_expr='>=24.11.1')
    @handle_api_error
    def upload_feature_impact(
        self, feature_impact_map: dict, update: bool = False
    ) -> dict:
        """
        User feature impact method. Currently supported for Tabular models only.

        :param feature_impact_map: Feature impacts dictionary with feature name as key
                                    and impact as value
        :param update: Whether the feature impact is being updated or uploaded

        :return: Dictionary with feature_names, feature_impact_scores, system_generated etc
        """
        self._check_id_attributes()
        payload: dict[str, Any] = {
            'model_id': self.id,
            'feature_impact_map': feature_impact_map,
        }

        url = '/v3/analytics/upload-feature-impact'

        http_method = self._get_method(update=update)

        response = http_method(
            url=url, data=payload, headers={'Content-Type': 'application/json'}
        )

        return response.json()['data']
