from pyspark.sql.functions import *
from pyspark.sql.types import StructField
from easy_spark.easy_con_opetator import EasyConOperator
from easy_spark.easy_con_value import EasyConValue


class EasySparkDeltaHelpers:

    @staticmethod
    def build_struct_type(struct_types: dict | list[StructField], nullable=False) -> StructType:
        struct_types = EasySparkDeltaHelpers.build_struct_fields(struct_types, nullable)

        return StructType(struct_types)

    @staticmethod
    def build_struct_fields(struct_types: dict | list[StructField], nullable=False) -> list[StructField]:

        if isinstance(struct_types, dict):
            struct_types = [StructField(key, value, nullable) for key, value in struct_types.items()]

        return struct_types

    @staticmethod
    def build_condition(keys: dict[str, any], conditions="", prefix: str = None):
        conditions = conditions

        if keys is None or len(keys) == 0:
            return conditions

        for key, value in keys.items():
            if isinstance(value, EasyConValue):
                operator = value.operator
                value = value.value
            else:
                operator = EasyConOperator.EQUALS

            operator_text = operator.value
            is_integer = isinstance(value, int) or isinstance(value, float)
            is_bool_val = isinstance(value, bool)

            if not conditions == "" and not conditions.endswith("And "):
                conditions += f" And "

            key_text = f"{prefix}.{key}" if prefix else key

            if is_integer or is_bool_val:
                conditions += f"{key_text} {operator_text} {value}"
            else:
                conditions += f"{key_text} {operator_text} '{value}'"

        return conditions

    @staticmethod
    def build_condition_by_multiple_keys(multiple_keys: list[tuple[str, list]], conditions=""):
        conditions = conditions

        if multiple_keys is None or len(multiple_keys) == 0:
            return conditions

        for key in multiple_keys:
            if key[1] is None and len(key[1]) == 0:
                continue

            if not conditions == "" and not conditions.endswith("And "):
                conditions += f" And "

            if len(key[1]) == 1:
                conditions = EasySparkDeltaHelpers.build_condition({key[0]: key[1][0]}, conditions)
            else:
                conditions += f"{key[0]} in {tuple(key[1])}"
        return conditions

    @staticmethod
    def combine_from_dfs(dfs: list[DataFrame], type: str = 'unionByName',
                         allow_missing_columns: bool = True) -> DataFrame:

        # Fid the index of df in dfs with the most number of columns
        index_df = 0
        for df in dfs:
            if len(df.columns) > len(dfs[index_df].columns):
                index_df = dfs.index(df)

        combine_df = dfs[index_df]

        if len(dfs) > 1:
            others_dfs = dfs[:index_df] + dfs[index_df + 1:]
            for other_df in others_dfs:
                if type == 'unionByName':
                    combine_df = combine_df.unionByName(other_df, allowMissingColumns=allow_missing_columns)
                else:
                    combine_df = combine_df.union(other_df)

        return combine_df

    @staticmethod
    def add_missing_columns_based_on_schema(df: DataFrame, schema: StructType) -> DataFrame:
        for field in schema.fields:
            if field.name not in df.columns:
                df = df.withColumn(field.name, lit(None).cast(field.dataType))
        return df

    @staticmethod
    def remove_columns_based_on_schema(df, schema: StructType) -> DataFrame:
        for coloumn in df.columns:
            if coloumn not in schema.names:
                df = df.drop(coloumn)

        return df
