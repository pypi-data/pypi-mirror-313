import pandas as pd
from pandas import DataFrame as DataFramePandas
from easy_panda.easy_panda_helpers import EasyPandaHelpers
from easy_panda.easy_panda_type import EasyPandaType
from easy_spark_path.easy_file_type import EasyFileType
from easy_spark_path.easy_spark_file_path import EasySparkFilePath


class EasyPanda:
    def __init__(self, pd_df: DataFramePandas):
        self._pd_df = pd_df

    @staticmethod
    def create(pd_df: DataFramePandas = None) -> 'EasyPanda':
        return EasyPanda(pd_df)

    @property
    def pd_df(self) -> DataFramePandas:
        return self._pd_df

    @pd_df.setter
    def pd_df(self, value: DataFramePandas):
        self._pd_df = value

    def from_dict(self, records: dict) -> 'EasyPanda':
        self._pd_df = pd.DataFrame.from_dict(records)
        return self

    def from_list(self, records: list[dict]) -> 'EasyPanda':
        self._pd_df = pd.DataFrame(records)

        return self

    def from_tuple(self, records: list[tuple]) -> 'EasyPanda':
        self._pd_df = pd.DataFrame(records)

        return self

    def from_json_normalize(self, records: list[dict]) -> 'EasyPanda':
        self._pd_df = pd.json_normalize(records)
        return self

    def from_csv(self, csv_path: str, header=True, seperator=",") -> 'EasyPanda':
        self._pd_df = pd.read_csv(csv_path, header=0 if header else None, sep=seperator)
        return self

    def set_types(self, pd_types: dict[str, EasyPandaType]) -> 'EasyPanda':
        convert_pd_types = {key: pd_types[key].value for key in pd_types}
        convert_pd_types = EasyPandaHelpers.order_pd_types_to_pd_df(self._pd_df, convert_pd_types)
        self._pd_df = self._pd_df.astype(convert_pd_types)
        return self

    def overwrite_types(self, pd_types: dict[str, EasyPandaType]) -> 'EasyPanda':
        convert_pd_types = {key: pd_types[key].value for key in pd_types}
        convert_pd_types = EasyPandaHelpers.overwrite_pd_types(self._pd_df.dtypes.to_dict(), convert_pd_types)
        # convert_pd_types = EasyPandaHelpers.order_pd_types_to_pd_df(self._pd_df, convert_pd_types)
        self._pd_df = self._pd_df.astype(convert_pd_types)
        return self

    def to_dict(self) -> dict:
        return self._pd_df.to_dict()

    def to_list_dict(self) -> list[dict]:
        return self._pd_df.to_dict(orient='records')

    def to_csv(self, path: str, index=False) -> 'EasyPanda':
        self._pd_df.to_csv(path, index=index)
        return self

    def to_json(self, path: str, index=False) -> 'EasyPanda':
        self._pd_df.to_json(path, index=index)
        return self

    def to_parquet(self, path: str, index=False) -> 'EasyPanda':
        self._pd_df.to_parquet(path, index=index)
        return self

    def to_file_path(self, file_path: EasySparkFilePath, index=False) -> 'EasyPanda':
        if file_path.file_type == EasyFileType.CSV:
            return self.to_csv(file_path.path, index)
        elif file_path.file_type == EasyFileType.JSON:
            return self.to_json(file_path.path, index)
        elif file_path.file_type == EasyFileType.PARQUET:
            return self.to_parquet(file_path.path, index)
        else:
            raise ValueError('File type not supported')

    def overwrite_types_from_type(self, from_type: EasyPandaType, to_type: EasyPandaType):
        cols = [col for col, col_type in self._pd_df.dtypes.items() if col_type == from_type.value]
        self._pd_df[cols] = self._pd_df[cols].astype(to_type.value)

    def is_empty_or_null(self) -> bool:
        return self._pd_df.empty or self._pd_df.isnull().values.any()
