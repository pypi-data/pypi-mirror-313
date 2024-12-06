from __future__ import annotations

import builtins
import logging
import typing
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from functools import cached_property
from pathlib import Path
from typing import Any, Iterator
from uuid import UUID

import pandas as pd

from fiddler.constants.dataset import EnvType
from fiddler.constants.model import ModelInputType, ModelTask
from fiddler.decorators import handle_api_error
from fiddler.entities.base import BaseEntity
from fiddler.entities.events import EventPublisher
from fiddler.entities.job import Job
from fiddler.entities.model_artifact import ModelArtifact
from fiddler.entities.model_deployment import ModelDeployment
from fiddler.entities.project import ProjectCompactMixin
from fiddler.entities.surrogate import Surrogate
from fiddler.entities.user import CreatedByMixin, UpdatedByMixin
from fiddler.entities.xai import XaiMixin
from fiddler.schemas.filter_query import OperatorType, QueryCondition, QueryRule
from fiddler.schemas.job import JobCompactResp
from fiddler.schemas.model import ModelResp
from fiddler.schemas.model_deployment import DeploymentParams
from fiddler.schemas.model_schema import ModelSchema
from fiddler.schemas.model_spec import ModelSpec
from fiddler.schemas.model_task_params import ModelTaskParams
from fiddler.schemas.xai_params import XaiParams
from fiddler.utils.helpers import raise_not_found
from fiddler.utils.model_generator import ModelGenerator

if typing.TYPE_CHECKING:
    from fiddler.entities.baseline import Baseline
    from fiddler.entities.dataset import Dataset

logger = logging.getLogger(__name__)


class Model(
    BaseEntity,
    CreatedByMixin,
    ProjectCompactMixin,
    UpdatedByMixin,
    XaiMixin,
):  # pylint: disable=too-many-ancestors
    def __init__(  # pylint: disable=too-many-arguments
        self,
        name: str,
        project_id: UUID | str,
        schema: ModelSchema,
        spec: ModelSpec,
        version: str | None = None,
        input_type: str = ModelInputType.TABULAR,
        task: str = ModelTask.NOT_SET,
        task_params: ModelTaskParams | None = None,
        description: str | None = None,
        event_id_col: str | None = None,
        event_ts_col: str | None = None,
        event_ts_format: str | None = None,
        xai_params: XaiParams | None = None,
    ) -> None:
        """Construct a model instance"""
        self.name = name
        self.version = version
        self.project_id = project_id
        self.schema = schema
        self.input_type = input_type
        self.task = task
        self.description = description
        self.event_id_col = event_id_col
        self.event_ts_col = event_ts_col
        self.event_ts_format = event_ts_format
        self.spec = spec
        self.task_params = task_params or ModelTaskParams()
        self.xai_params = xai_params or XaiParams()

        self.id: UUID | None = None
        self.artifact_status: str | None = None
        self.artifact_files: list[dict] | None = None
        self.is_binary_ranking_model: bool | None = None
        self.created_at: datetime | None = None
        self.updated_at: datetime | None = None

        # Deserialized response object
        self._resp: ModelResp | None = None

    @staticmethod
    def _get_url(id_: UUID | str | None = None) -> str:
        """Get model resource/item url."""
        url = '/v3/models'
        return url if not id_ else f'{url}/{id_}'

    @classmethod
    def _from_dict(cls, data: dict) -> Model:
        """Build entity object from the given dictionary."""

        # Deserialize the response
        resp_obj = ModelResp(**data)

        # Initialize
        instance = cls(
            name=resp_obj.name,
            version=resp_obj.version,
            schema=resp_obj.schema_,
            spec=resp_obj.spec,
            project_id=resp_obj.project.id,
            input_type=resp_obj.input_type,
            task=resp_obj.task,
            task_params=resp_obj.task_params,
            description=resp_obj.description,
            event_id_col=resp_obj.event_id_col,
            event_ts_col=resp_obj.event_ts_col,
            event_ts_format=resp_obj.event_ts_format,
            xai_params=resp_obj.xai_params,
        )

        # Add remaining fields
        fields = [
            'id',
            'created_at',
            'updated_at',
            'artifact_status',
            'artifact_files',
            'is_binary_ranking_model',
        ]
        for field in fields:
            setattr(instance, field, getattr(resp_obj, field, None))

        instance._resp = resp_obj
        return instance

    def _refresh(self, data: dict) -> None:
        """Refresh the fields of this instance from the given response dictionary"""
        # Deserialize the response
        resp_obj = ModelResp(**data)

        # Reset fields
        self.schema = resp_obj.schema_
        self.project_id = resp_obj.project.id

        fields = [
            'id',
            'name',
            'version',
            'spec',
            'input_type',
            'task',
            'task_params',
            'description',
            'event_id_col',
            'event_ts_col',
            'event_ts_format',
            'xai_params',
            'created_at',
            'updated_at',
            'artifact_status',
            'artifact_files',
            'is_binary_ranking_model',
        ]
        for field in fields:
            setattr(self, field, getattr(resp_obj, field, None))

        self._resp = resp_obj

    @cached_property
    def _artifact(self) -> ModelArtifact:
        """Model artifact instance"""
        assert self.id is not None
        return ModelArtifact(model_id=self.id)

    @cached_property
    def _surrogate(self) -> Surrogate:
        """Model artifact instance"""
        assert self.id is not None
        return Surrogate(model_id=self.id)

    @cached_property
    def _event_publisher(self) -> EventPublisher:
        """Event publisher instance"""
        assert self.id is not None
        return EventPublisher(model_id=self.id)

    @classmethod
    @handle_api_error
    def get(cls, id_: UUID | str) -> Model:
        """Get the model instance using model id."""
        response = cls._client().get(url=cls._get_url(id_))
        return cls._from_response(response=response)

    @classmethod
    @handle_api_error
    def from_name(
        cls,
        name: str,
        project_id: UUID | str,
        version: str | None = None,
        latest: bool = False,
    ) -> Model:
        """
        Get the model instance from model name within a project.

        :param name: Model name
        :param project_id: Project identifier
        :param version: Version name
        :param latest: Whether to fetch the latest version of the model or first version
        :return: Model instance
        """
        _filter = QueryCondition(
            rules=[
                QueryRule(field='name', operator=OperatorType.EQUAL, value=name),
                QueryRule(
                    field='project_id',
                    operator=OperatorType.EQUAL,
                    value=project_id,
                ),
            ]
        )

        if version:
            _filter.add_rule(
                QueryRule(field='version', operator=OperatorType.EQUAL, value=version)
            )

        ordering = '-created_at' if latest else 'created_at'
        response = cls._client().get(
            url=cls._get_url(),
            params={'filter': _filter.json(), 'limit': 1, 'ordering': ordering},
        )

        if response.json()['data']['total'] == 0:
            raise_not_found('Model not found for the given identifier')

        return cls.get(id_=response.json()['data']['items'][0]['id'])

    @handle_api_error
    def create(self) -> Model:
        """Create a new model."""
        payload = {
            'name': self.name,
            'project_id': str(self.project_id),
            'schema': self.schema.dict(),
            'spec': self.spec.dict(),
            'input_type': self.input_type,
            'task': self.task,
            'task_params': self.task_params.dict(),
            'description': self.description,
            'event_id_col': self.event_id_col,
            'event_ts_col': self.event_ts_col,
            'event_ts_format': self.event_ts_format,
            'xai_params': self.xai_params.dict(),
        }

        if self.version:
            payload['version'] = self.version

        response = self._client().post(
            url=self._get_url(),
            # The above seems to be safe for stdlib JSON-encoding.
            json=payload,
        )
        self._refresh_from_response(response=response)
        return self

    @handle_api_error
    def update(self) -> None:
        """Update an existing model."""
        body: dict[str, Any] = {
            'version': self.version,
            'xai_params': self.xai_params.dict(),
            'description': self.description,
            'event_id_col': self.event_id_col,
            'event_ts_col': self.event_ts_col,
            'event_ts_format': self.event_ts_format,
        }

        response = self._client().patch(
            url=self._get_url(id_=self.id),
            # object seems safe for stdlib JSON-encoding
            json=body,
        )
        self._refresh_from_response(response=response)

    @classmethod
    @handle_api_error
    def list(
        cls, project_id: UUID | str, name: str | None = None
    ) -> Iterator[ModelCompact]:
        """
        Get a list of all models with the given filters

        :param project_id: Project identifier
        :param name: Model name, use this for listing all the versions of a model
        :return: ModelCompact iterator
        """
        _filter = QueryCondition(
            rules=[
                QueryRule(
                    field='project_id', operator=OperatorType.EQUAL, value=project_id
                ),
            ]
        )

        if name:
            _filter.add_rule(
                QueryRule(field='name', operator=OperatorType.EQUAL, value=name)
            )

        params = {'filter': _filter.json()}

        for model in cls._paginate(url=cls._get_url(), params=params):
            yield ModelCompact(
                id=model['id'], name=model['name'], version=model['version']
            )

    def duplicate(self, version: str | None = None) -> Model:
        """
        Duplicate the model instance with the given version name.

        This call will not save the model on server. After making changes to the model
        instance call .create() to add the model version to Fiddler Platform.

        :param version: Version name for the new instance
        :return: Model instance
        """
        return Model(
            name=self.name,
            project_id=self.project_id,
            schema=deepcopy(self.schema),
            spec=deepcopy(self.spec),
            version=version if version else self.version,
            input_type=self.input_type,
            task=self.task,
            task_params=deepcopy(self.task_params),
            description=self.description,
            event_id_col=self.event_id_col,
            event_ts_col=self.event_ts_col,
            event_ts_format=self.event_ts_format,
            xai_params=deepcopy(self.xai_params),
        )

    @property
    def datasets(self) -> Iterator[Dataset]:
        """Fetch all the datasets of this model"""
        from fiddler.entities.dataset import (  # pylint: disable=import-outside-toplevel
            Dataset,
        )

        assert self.id is not None

        yield from Dataset.list(model_id=self.id)

    @property
    def baselines(self) -> Iterator[Baseline]:
        """Fetch all the baselines of this model"""
        from fiddler.entities.baseline import (  # pylint: disable=import-outside-toplevel
            Baseline,
        )

        assert self.id is not None

        yield from Baseline.list(model_id=self.id)

    @cached_property
    @handle_api_error
    def deployment(self) -> ModelDeployment:
        """Fetch model deployment instance of this model"""
        assert self.id is not None

        return ModelDeployment.of(model_id=self.id)

    @classmethod
    @handle_api_error
    def from_data(  # pylint: disable=too-many-arguments, too-many-locals
        cls,
        source: pd.DataFrame | Path | str,
        name: str,
        project_id: UUID | str,
        spec: ModelSpec | None = None,
        version: str | None = None,
        input_type: str = ModelInputType.TABULAR,
        task: str = ModelTask.NOT_SET,
        task_params: ModelTaskParams | None = None,
        description: str | None = None,
        event_id_col: str | None = None,
        event_ts_col: str | None = None,
        event_ts_format: str | None = None,
        xai_params: XaiParams | None = None,
        max_cardinality: int | None = None,
        sample_size: int | None = None,
    ) -> Model:
        """
        Build model instance from the given dataframe

        :param source: Dataframe or a file to generate model instance
        :param name: Model name
        :param project_id: Project identifier
        :param spec: ModelSpec instance
        :param version: Model version name
        :param input_type: Model input task type
        :param task: Model task like Regression, Binary classification etc.
        :param task_params: Parameters based on the task type
        :param description: A note or description of the model
        :param event_id_col: Column name in which event id will be sent
        :param event_ts_col: Column name in which event timestamp will be sent
        :param event_ts_format: Format of values in `event_ts_col` column
        :param xai_params: Parameters for xai features
        :param max_cardinality: Max cardinality to detect categorical columns.
        :param sample_size: No. of samples to use for generating schema.
        :return: Model instance
        """

        resp_obj = ModelGenerator(
            source=source,
            spec=spec,
        ).generate(max_cardinality=max_cardinality, sample_size=sample_size)

        return Model(
            name=name,
            version=version,
            schema=resp_obj.schema_,
            spec=resp_obj.spec,
            project_id=project_id,
            input_type=input_type,
            task=task,
            task_params=task_params,
            description=description,
            event_id_col=event_id_col,
            event_ts_col=event_ts_col,
            event_ts_format=event_ts_format,
            xai_params=xai_params,
        )

    @handle_api_error
    def delete(self) -> Job:
        """
        Delete a model and it's associated resources.

        :return: model deletion job instance
        """
        assert self.id is not None
        response = self._client().delete(url=self._get_url(id_=self.id))

        job_compact = JobCompactResp(**response.json()['data']['job'])
        return Job.get(id_=job_compact.id)

    def remove_column(self, column_name: str, missing_ok: bool = True) -> None:
        """
        Remove a column from the model schema and spec

        This method is only to modify model object before creating and
        will not save the model on Fiddler Platform. After making
        changes to the model instance, call `.create()` to add the model
        to Fiddler Platform.

        :param column_name: Column name to be removed
        :param missing_ok: If True, do not raise an error if the column is not found
        :return: None

        :raises KeyError: If the column name is not found and missing_ok is False
        """
        try:
            del self.schema[column_name]
        except KeyError as e:
            if not missing_ok:
                raise e
        self.spec.remove_column(column_name)

    @handle_api_error
    def publish(
        self,
        source: builtins.list[dict[str, Any]] | str | Path | pd.DataFrame,
        environment: EnvType = EnvType.PRODUCTION,
        dataset_name: str | None = None,
        update: bool = False,
    ) -> builtins.list[UUID] | Job:
        """
        Publish Pre-production or Production data

        :param source: one of:
            Path or str path: path for data file.
            list[dict]: list of events (max 1000) PRE_PRODUCTION environment is not
                supported
            dataframe: events dataframe. EnvType.PRE_PRODUCTION not supported.
        :param environment: Either EnvType.PRE_PRODUCTION or EnvType.PRODUCTION
        :param dataset_name: Name of the dataset. Not supported for EnvType.PRODUCTION
        :param update: flag indicating if the events are updates to previously
            published rows

        :return: list[UUID] for list of dicts or dataframe source and Job object for
            file path source.
        """
        logger.info('Model[%s/%s] - Publishing events', self.name, self.version)
        return self._event_publisher.publish(
            source=source,
            environment=environment,
            dataset_name=dataset_name,
            update=update,
        )

    def add_artifact(
        self,
        model_dir: str | Path,
        deployment_params: DeploymentParams | None = None,
    ) -> Job:
        """
        Upload and deploy model artifact.

        :param model_dir: Path to model artifact tar file
        :param deployment_params: Model deployment parameters
        :return: Async job instance
        """
        return self._artifact.add(
            model_dir=model_dir, deployment_params=deployment_params
        )

    def update_artifact(
        self,
        model_dir: str | Path,
        deployment_params: DeploymentParams | None = None,
    ) -> Job:
        """
        Update existing model artifact.

        :param model_dir: Path to model artifact tar file
        :param deployment_params: Model deployment parameters
        :return: Async job instance
        """
        return self._artifact.update(
            model_dir=model_dir, deployment_params=deployment_params
        )

    def download_artifact(
        self,
        output_dir: str | Path,
    ) -> None:
        """
        Download existing model artifact.

        :param output_dir: Path to download model artifact tar file
        """

        self._artifact.download(output_dir=output_dir)

    def add_surrogate(
        self,
        dataset_id: UUID | str,
        deployment_params: DeploymentParams | None = None,
    ) -> Job:
        """
        Add a new surrogate model

        :param dataset_id: Dataset to be used for generating surrogate model
        :param deployment_params: Model deployment parameters
        :return: Async job
        """
        job = self._surrogate.add(
            dataset_id=dataset_id, deployment_params=deployment_params
        )
        return job

    @handle_api_error
    def update_surrogate(
        self,
        dataset_id: UUID | str,
        deployment_params: DeploymentParams | None = None,
    ) -> Job:
        """
        Update an existing surrogate model

        :param dataset_id: Dataset to be used for generating surrogate model
        :param deployment_params: Model deployment parameters
        :return: Async job
        """
        job = self._surrogate.update(
            dataset_id=dataset_id, deployment_params=deployment_params
        )
        return job


@dataclass
class ModelCompact:
    id: UUID
    name: str
    version: str | None = None

    def fetch(self) -> Model:
        """Fetch model instance"""
        return Model.get(id_=self.id)


class ModelCompactMixin:
    @property
    def model(self) -> ModelCompact:
        """Model instance"""
        response = getattr(self, '_resp', None)
        if not response or not hasattr(response, 'model'):
            raise AttributeError(
                'This property is available only for objects generated from API '
                'response.'
            )

        return ModelCompact(
            id=response.model.id,
            name=response.model.name,
            version=response.model.version,
        )
