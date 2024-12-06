import os
import tempfile
from pathlib import Path

import pandas as pd
import pytest

from fiddler.schemas.server_info import Version
from fiddler.utils.helpers import group_by, try_series_retype
from fiddler.utils.validations import validate_artifact_dir
from fiddler.utils.version import match_semver


def test_match_semvar_version() -> None:
    assert match_semver(None, '>=22.9.0') is False
    assert match_semver(Version.parse('22.9.0'), '>=22.10.0') is False
    assert match_semver(Version.parse('22.10.0'), '>=22.10.0') is True
    assert match_semver(Version.parse('22.10.0'), '>22.10.0') is False
    assert match_semver(Version.parse('22.11.0'), '>=22.10.0') is True
    assert match_semver(Version.parse('22.11.0'), '>22.10.0') is True
    assert match_semver(Version.parse('22.10.0'), '<=22.10.0') is True
    assert match_semver(Version.parse('22.10.0'), '<22.10.0') is False
    assert match_semver(Version.parse('22.9.0'), '<22.10.0') is True
    assert match_semver(Version.parse('22.11.0-RC1'), '>=22.11.0') is True


def test_validate_artifact_dir(tmp_path) -> None:
    artifact_dir = os.path.join(Path(__file__).resolve().parent, 'artifact_test_dir')
    assert validate_artifact_dir(Path(artifact_dir)) is None
    # Test for artifact_dir not valid directory
    with pytest.raises(ValueError):
        validate_artifact_dir(Path('test'))
    # Test for package.py file not found
    mock_dir = tmp_path / 'test'
    mock_dir.mkdir()
    with pytest.raises(ValueError):
        validate_artifact_dir(Path(mock_dir))


def test_group_by_helper() -> None:
    df = pd.DataFrame(
        [
            {'col1': 1, 'col2': 'foo'},
            {'col1': 2, 'col2': 'bar'},
            {'col1': 3, 'col2': 'baz'},
            {'col1': 3, 'col2': 'foo'},
        ]
    )

    # with output_path
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / 'data.csv'

        assert file_path.exists() is False
        group_by(df=df, group_by_col='col2', output_path=file_path)
        assert file_path.exists() is True

    # without output path
    grouped_df = group_by(df=df, group_by_col='col2')
    assert grouped_df.equals(
        pd.DataFrame(
            [
                {'col2': 'foo', 'col1': [1, 3]},
                {'col2': 'bar', 'col1': [2]},
                {'col2': 'baz', 'col1': [3]},
            ]
        )
    )


def test_try_series_retype() -> None:
    series = pd.Series([1, 2, 3], dtype='float')
    series = try_series_retype(series, 'int')
    assert series.dtype == 'int'

    series = pd.Series([1, 2, None])
    series = try_series_retype(series, 'int')
    assert series.dtype == 'float'


def test_try_series_retype_str_or_unkown() -> None:
    series = pd.Series(['HIGH', 'MEDIUM', '', None], dtype='str')
    series = try_series_retype(series, 'str')
    assert series.dtype == 'object'


def test_try_series_retype_timestamp() -> None:
    series = pd.Series(
        ['2023-11-12 09:15:32.23', '2023-12-11 09:15:32.45'], dtype='str'
    )
    series = try_series_retype(series, 'timestamp')
    assert series.dtype == 'datetime64[ns]'


def test_try_series_retype_timestamp_error() -> None:
    series = pd.Series(['2023-11-12 09:15:32.23', None], dtype='str')

    with pytest.raises(TypeError):
        try_series_retype(series, 'timestamp')
