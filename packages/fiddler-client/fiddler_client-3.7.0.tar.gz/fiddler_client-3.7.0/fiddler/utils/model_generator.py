from __future__ import annotations

import os.path
import tempfile
from pathlib import Path
from typing import Any

import pandas as pd

from fiddler.connection import ConnectionMixin
from fiddler.entities.file import File
from fiddler.schemas.model import GenerateModelResp
from fiddler.schemas.model_spec import ModelSpec


class ModelGenerator(ConnectionMixin):
    def __init__(
        self,
        source: pd.DataFrame | Path | str,
        spec: ModelSpec | None = None,
    ) -> None:
        """
        Initialize model generator instance

        :param source: Dataframe or a file to generate model instance
        :param spec: ModelSpec instance
        """

        if isinstance(source, (Path, str)):
            source = Path(source)

            if not source.exists():
                raise ValueError(f'File not found - {source}')

        self.source = source
        self.spec = spec

    def _upload(self) -> File:
        if isinstance(self.source, pd.DataFrame):
            with tempfile.TemporaryDirectory() as tmp:
                file_path = os.path.join(tmp, 'data.parquet')
                self.source.astype('str').to_parquet(path=file_path, index=False)

                return File(path=Path(file_path)).upload()

        return File(path=self.source).upload()

    def generate(
        self, max_cardinality: int | None = None, sample_size: int | None = None
    ) -> GenerateModelResp:
        """
        Generate model instance from the given source

        :param max_cardinality: Max cardinality to detect categorical columns.
        :param sample_size: No. of samples to use for generating schema.
        :return: Model instance
        """

        file = self._upload()

        payload: dict[str, Any] = {'file_id': file.id}

        if max_cardinality is not None:
            payload['max_cardinality'] = max_cardinality

        if sample_size is not None:
            payload['sample_size'] = sample_size

        if self.spec:
            payload['spec'] = self.spec.dict()

        response = self._client().post(
            url='/v3/model-factory',
            data=payload,
            headers={'Content-Type': 'application/json'},
        )

        return GenerateModelResp(**response.json()['data'])
