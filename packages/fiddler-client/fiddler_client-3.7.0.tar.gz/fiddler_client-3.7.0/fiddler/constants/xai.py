import enum


@enum.unique
class ExplainMethod(str, enum.Enum):
    SHAP = 'SHAP'
    FIDDLER_SHAP = 'FIDDLER_SHAP'
    IG = 'IG'
    PERMUTE = 'PERMUTE'
    ZERO_RESET = 'ZERO_RESET'
    MEAN_RESET = 'MEAN_RESET'


@enum.unique
class DownloadFormat(str, enum.Enum):
    PARQUET = 'PARQUET'
    CSV = 'CSV'


DEFAULT_DOWNLOAD_CHUNK_SIZE = 1000
