from enum import Enum


class EasyFormatType(Enum):
    DELTA = "delta"
    CSV = "csv"
    PARQUET = "parquet"
    JSON = "json"
