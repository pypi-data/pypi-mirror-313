import pandas as pd
from pandas import DataFrame as DataFramePandas


class EasyPandaHelpers:
    @staticmethod
    def order_pd_types_to_pd_df(pd_df: DataFramePandas, pd_types: dict[str, str]) -> dict[str, str]:
        if pd_df.empty:
            return pd_types

        pd_types = {key: pd_types[key] for key in pd_df.columns}
        return pd_types

    @staticmethod
    def combine_pd_types(pd_types: dict[str, str], pd_types_to_add: dict[str, str]) -> dict[
        str, str]:
        for key, value in pd_types_to_add.items():
            if key not in pd_types:
                pd_types[key] = value
        return pd_types

    @staticmethod
    def overwrite_pd_types(pd_types: dict[str, str], pd_types_to_overwrite: dict[str, str]) -> dict[
        str, str]:
        for key, value in pd_types_to_overwrite.items():
            if key in pd_types:
                pd_types[key] = value
        return pd_types
