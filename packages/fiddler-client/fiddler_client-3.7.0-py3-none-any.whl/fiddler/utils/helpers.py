from __future__ import annotations

from datetime import datetime
import logging
from http import HTTPStatus
from pathlib import Path

import pandas as pd

from fiddler.constants.common import TIMESTAMP_FORMAT
from fiddler.constants.model import DataType
from fiddler.exceptions import NotFound
from fiddler.schemas.response import ErrorData, ErrorItem

logger = logging.getLogger(__name__)


def try_series_retype(series: pd.Series, new_type: str) -> pd.DataFrame | pd.Series:
    """Retype series."""
    if new_type in ['unknown', 'str', 'vector']:
        # Do not retype data
        return series

    try:
        return series.astype(new_type)
    except (TypeError, ValueError) as e:
        if new_type == 'int':
            logger.warning(
                '"%s" cannot be loaded as int '
                '(likely because it contains missing values, and '
                'Pandas does not support NaN for ints). Loading '
                'as float instead.',
                series.name,
            )
            return series.astype('float')
        if new_type.lower() == DataType.TIMESTAMP.value:
            try:
                return series.apply(lambda x: datetime.strptime(x, TIMESTAMP_FORMAT))
            # if timestamp str doesn't contain millisec.
            except ValueError:
                # @TODO: Should such cases be
                # 1. handled by client OR
                # 2. should server apped 00 ms if not present during ingestion OR
                # 3. should it break if timestamp format does not match while ingestion?
                return series.apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
        else:
            raise e


def raise_not_found(message: str) -> None:
    """Raise NotFound if the resource is not found while fetching with names"""
    raise NotFound(
        error=ErrorData(
            code=HTTPStatus.NOT_FOUND,
            message=message,
            errors=[
                ErrorItem(
                    reason='ObjectNotFound',
                    message=message,
                    help='',
                ),
            ],
        ),
    )


def group_by(
    df: pd.DataFrame, group_by_col: str, output_path: Path | str | None = None
) -> pd.DataFrame:
    """
    Group the events by a column. Use this method to form the grouped data for ranking models

    :param df: The dataframe with flat data.
    :param group_by_col: The column to group the data by.
    :param output_path: Optional argument, the path to write the grouped data to.
    If not specified, data won't be written anywhere.
    :return grouped_df: dataframe in grouped format
    """
    grouped_df = df.groupby(by=group_by_col, sort=False)
    grouped_df = grouped_df.aggregate(lambda x: x.tolist())

    if output_path is not None:
        grouped_df.to_csv(output_path, index=True)

    return grouped_df.reset_index()
