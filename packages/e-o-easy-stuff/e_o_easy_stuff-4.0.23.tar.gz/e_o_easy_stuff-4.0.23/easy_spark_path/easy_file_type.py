from enum import Enum


class EasyFileType(Enum):
    CSV = 'csv'
    PARQUET = 'parquet'
    JSON = 'json'
    UNKNOWN = 'UNKNOWN'
