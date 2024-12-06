from pyspark.sql import SparkSession

from easy_spark.easy_merge_option_type import EasyMergeOptionType
from easy_spark.easy_merge_type import EasyMergeType
from easy_spark.easy_save_mode_type import EasySaveModeType
from easy_spark.easy_spark_delta_helpers import EasySparkDeltaHelpers
from easy_spark.easy_spark_df import EasySparkDF
from easy_spark.easy_spark_df_optimize import EasySparkDFOptimize
from easy_spark.easy_spark_instance import EasySparkInstance
from pyspark.sql.functions import *
from delta.tables import *
from pyspark.sql import Row
from pandas import DataFrame as DataFramePandas
import pandas as pd
from easy_spark_fs.easy_spark_catalog import EasySparkCatalog
from easy_spark_fs.easy_spark_fs_file import EasySparkFSFile
from easy_spark_fs.easy_spark_fs_path import EasySparkFSPath
from easy_spark_path.easy_spark_table_path import EasySparkTablePath


# TODO: Use with
# TODO: Add Z Index
# TODO Add Method to remove nulls from df
# TODO: Also support group of operators
# TODO: More SQL queries like delete, join
# TODO: Do the insert
# TODO: Check all the imports
# TODO: For merge you can specify what records you want to insert
# TODO: Overwrite eq and + -
# TODO:
# filtered_df = easy_df.df.filter(
#             (col('LastImpression').isNull()) |  # Filters None values
#             (col('LastImpression') == '') |  # Filters empty strings
#             (isnan(col('LastImpression')))  # Filters NaN valuesA
#         )
##TODO: .option('optimize',True).option('zorderCol',UniqueIdentifierColumn)
# TODO: Joins in DFS method
# TODO: Add methods for alias (df_alias = df.select(col("name").alias("person_name")))
# TODO: Add Warehouse to DF
# TODO: This how you remove duplicates
# ## Remove duplicates based unique identifier
# # Define window specification based on partition column and unique identifier column.
# if SourceDateTimeColumn != 'NA':
#     window_spec = Window.partitionBy(UniqueIdentifierColumn).orderBy(col(SourceDateTimeColumn).desc())
#     # Add a new column "row_num" to identify duplicate rows within each partition.
#     df = df.withColumn("row_num", row_number().over(window_spec))
#     # Keep only rows where "row_num" is 1 (i.e., the row with max value in PartitionColumn).
#     df = df.filter(df.row_num == 1)
#     # Drop the "row_num" column since we no longer need it.
#     df = df.drop("row_num")


class EasySparkDeltaTable:
    _spark: SparkSession = None

    def __init__(self, spark: SparkSession, path: str = None, for_name: bool = False,
                 create_schema: StructType = None,
                 partition_columns: list[str] = None):
        self.spark_instance = EasySparkInstance(spark)
        self.spark_fs_path = EasySparkFSPath(spark)
        self.spark_catalog = EasySparkCatalog(spark)
        self.df_optimize = EasySparkDFOptimize(spark)
        EasySparkDeltaTable._spark = spark
        self._delta_path = None
        self.path: str = path
        self.for_name: bool = for_name

        if self.path:
            if for_name:
                self.for_name_from_path(self.path)
            else:
                self.from_path(self.path)

            if create_schema is not None:
                self.create_empty_if_not_exists(create_schema, partition_columns=partition_columns)
            self.init_delta()

    @staticmethod
    def create(spark: SparkSession, path: str = None, create_schema: StructType = None,
               partition_columns: list[str] = None) -> 'EasySparkDeltaTable':
        return EasySparkDeltaTable(spark, path, False, create_schema, partition_columns)

    @staticmethod
    def create_for_name(spark: SparkSession, path: str = None, create_schema: StructType = None,
                        partition_columns: list[str] = None) -> 'EasySparkDeltaTable':

        return EasySparkDeltaTable(spark, path, True, create_schema, partition_columns)

    @staticmethod
    def create_for_name_from_lh_table_name(spark: SparkSession, name: str, table_name: str,
                                           create_schema: StructType = None,
                                           partition_columns: list[str] = None) -> 'EasySparkDeltaTable':
        path = f'{name}.{table_name}'
        return EasySparkDeltaTable.create_for_name(spark, path, create_schema, partition_columns)

    @staticmethod
    def create_for_name_from_lh_table(spark: SparkSession, table_name: str,
                                      create_schema: StructType = None,
                                      partition_columns: list[str] = None) -> 'EasySparkDeltaTable':
        return EasySparkDeltaTable.create_for_name(spark, table_name, create_schema, partition_columns)

    @staticmethod
    def create_from_table_path(spark: SparkSession, table_path: EasySparkTablePath, create_schema: StructType = None,
                               partition_columns: list[str] = None):
        if table_path.is_table_name:
            return EasySparkDeltaTable.create_for_name_from_lh_table(spark, table_path.path, create_schema,
                                                                     partition_columns)
        else:
            return EasySparkDeltaTable.create(spark, table_path.path, create_schema, partition_columns)

    @property
    def delta_path(self):
        return self._delta_path

    def to_easy_df(self) -> EasySparkDF:
        return EasySparkDF(self._delta_path.toDF(), EasySparkDeltaTable._spark)

    def to_fs_file(self, must_java_import=False) -> EasySparkFSFile:
        return EasySparkFSFile(EasySparkDeltaTable._spark, self.path, must_java_import)

    def from_path(self, path: str) -> 'EasySparkDeltaTable':
        self.path = path

        return self

    def for_name_from_path(self, path: str) -> 'EasySparkDeltaTable':
        self.path = path
        self.for_name = True

        return self

    def init_delta(self) -> 'EasySparkDeltaTable':
        if self.exists():
            if self.for_name:
                self._delta_path = DeltaTable.forName(EasySparkDeltaTable._spark, self.path)
            else:
                self._delta_path = DeltaTable.forPath(EasySparkDeltaTable._spark, self.path)

        return self

    def exists(self) -> bool:
        if self.for_name:
            return self.spark_catalog.table_exists_from_path(self.path)
        else:
            return self.spark_fs_path.file_exists_from_path(self.path, False)

    def create_empty_if_not_exists(self, schema: StructType = None,
                                   partition_columns: list[str] = None) -> 'EasySparkDeltaTable':

        if not self.exists():
            self.create_empty(schema, partition_columns)

        return self

    def create_empty(self, schema: StructType = None, partition_columns: list[str] = None) -> 'EasySparkDeltaTable':
        easy_df = EasySparkDF.create(EasySparkDeltaTable._spark).empty(schema)

        self.save(easy_df, partition_columns=partition_columns)
        return self

    def get_dict(self, keys: dict[str, any]) -> dict[str, any] | None:
        df = self.to_easy_df().filter(keys).df
        if df is None or df.count() == 0:
            return None

        rows = df.collect()
        return rows[0].asDict()

    def get_dict_using_filter(self, keys: dict[str, any]) -> dict[str, any] | None:
        df = self.to_easy_df().filter_using_filter(keys).df
        if df is None or df.count() == 0:
            return None

        rows = df.collect()
        return rows[0].asDict()

    def get_dict_by_filter(self, condition: str) -> dict[str, any] | None:
        df = self.to_easy_df().filter_by_filter(condition).df
        if df is None or df.count() == 0:
            return None

        rows = df.collect()
        return rows[0].asDict()

    def get_dict_by_where(self, condition: str) -> dict[str, any] | None:
        df = self.to_easy_df().where(condition).df
        if df is None or df.count() == 0:
            return None

        rows = df.collect()
        return rows[0].asDict()

    def get_rows_using_filter(self, keys: dict[str, any] = None) -> list[Row]:
        return self.to_easy_df().filter_using_filter(keys).df.collect()

    def get_rows_by_filter(self, condition: str = None) -> list[Row]:
        return self.to_easy_df().filter_by_filter(condition).df.collect()

    def get_rows_by_where(self, condition: str = None) -> list[Row]:
        return self.to_easy_df().where(condition).df.collect()

    def get_rows_using_where(self, keys: dict[str, any] = None) -> list[Row]:
        return self.to_easy_df().where_using_where(keys).df.collect()

    def get_rows(self, keys: dict[str, any] = None) -> list[Row]:
        return self.to_easy_df().filter(keys).df.collect()

    def get_list(self, keys: dict[str, any] = None) -> list[dict[str, any]]:
        rows = self.get_rows(keys)
        return [row.asDict() for row in rows]

    def get_list_using_filter(self, keys: dict[str, any] = None) -> list[dict[str, any]]:
        rows = self.get_rows_using_filter(keys)
        return [row.asDict() for row in rows]

    def get_list_by_filter(self, condition: str = None) -> list[dict[str, any]]:
        rows = self.get_rows_by_filter(condition)
        return [row.asDict() for row in rows]

    def get_list_by_where(self, condition: str = None) -> list[dict[str, any]]:
        rows = self.get_rows_by_where(condition)
        return [row.asDict() for row in rows]

    def add_from_dict(self, record: dict, schema: StructType = None) -> 'EasySparkDeltaTable':
        return self.add_from_list([record], schema)

    def add_from_list(self, records: list[dict], schema: StructType = None,
                      ignore_order=False) -> 'EasySparkDeltaTable':
        new_easy_df = EasySparkDF.create(self.spark_instance.spark).clone_from_list(records, schema, ignore_order)
        self.save(new_easy_df, save_mode_type=EasySaveModeType.APPEND)
        return self

    def add_from_df(self, df: DataFrame, merge_option_type: EasyMergeOptionType = EasyMergeOptionType.OVERWRITE_SCHEMA,
                    partition_columns: list[str] = None) -> 'EasySparkDeltaTable':
        new_easy_df = EasySparkDF.create(self.spark_instance.spark, df)
        self.save(new_easy_df, save_mode_type=EasySaveModeType.APPEND, merge_option_type=merge_option_type,
                  partition_columns=partition_columns)
        return self

    def combine_from_df(self, df: DataFrame, type: str = 'unionByName',
                        allow_missing_columns: bool = True,
                        merge_option_type: EasyMergeOptionType = EasyMergeOptionType.OVERWRITE_SCHEMA,
                        partition_columns: list[str] = None) -> 'EasySparkDeltaTable':
        easy_df = self.to_easy_df()
        easy_df.combine_from_df(df, type, allow_missing_columns)
        self.save(easy_df, merge_option_type=merge_option_type, partition_columns=partition_columns)
        return self

    def add_from_pd_df(self, pd_df: DataFramePandas, schema: StructType = None,
                       merge_option_type: EasyMergeOptionType = EasyMergeOptionType.OVERWRITE_SCHEMA,
                       partition_columns: list[str] = None) -> 'EasySparkDeltaTable':
        new_easy_df = EasySparkDF.create(self.spark_instance.spark).clone_from_pd_df(pd_df, schema)
        self.save(new_easy_df, save_mode_type=EasySaveModeType.APPEND, merge_option_type=merge_option_type,
                  partition_columns=partition_columns)
        return self

    def combine_from_pd_df(self, pd_df: DataFramePandas, schema: StructType = None,
                           type: str = 'unionByName',
                           allow_missing_columns: bool = True,
                           merge_option_type: EasyMergeOptionType = EasyMergeOptionType.OVERWRITE_SCHEMA) -> 'EasySparkDeltaTable':
        easy_df = self.to_easy_df()
        easy_df.combine_from_pd_df(pd_df, schema, type, allow_missing_columns)
        self.save(easy_df, merge_option_type=merge_option_type)
        return self

    def update(self, keys: dict[str, any], values: dict[str, any]) -> 'EasySparkDeltaTable':
        conditions = EasySparkDeltaTable._build_condition(keys)
        sets = {k: lit(v) for k, v in values.items()}

        self._delta_path.update(
            condition=conditions,
            set=sets
        )
        return self

    def update_by_condition(self, condition: str, values: dict[str, any]) -> 'EasySparkDeltaTable':
        sets = {k: lit(v) for k, v in values.items()}
        self._delta_path.update(
            condition=condition,
            set=sets
        )
        return self

    def delete(self, keys: dict[str, any] = None,
               multiple_keys: list[tuple[str, list]] = None) -> 'EasySparkDeltaTable':
        conditions = ""

        if keys:
            conditions = EasySparkDeltaTable._build_condition(keys)

        if multiple_keys and len(multiple_keys) > 0:
            conditions = EasySparkDeltaHelpers.build_condition_by_multiple_keys(multiple_keys, conditions)

        self._delta_path.delete(condition=conditions)
        return self

    def delete_by_multiple_keys(self, key: str, key_values: list) -> 'EasySparkDeltaTable':
        self._delta_path.delete(f"{key} in {tuple(key_values)}")
        return self

    def delete_by_condition(self, condition: str) -> 'EasySparkDeltaTable':
        self._delta_path.delete(condition)
        return self

    def delete_all(self) -> 'EasySparkDeltaTable':
        easy_df = self.to_easy_df()
        easy_df.empty()
        self.save(easy_df, save_mode_type=EasySaveModeType.OVER_WRITE)

        return self

    def save_from_df(self, df: DataFrame = None, save_mode_type: EasySaveModeType = EasySaveModeType.OVER_WRITE,
                     merge_option_type: EasyMergeOptionType = EasyMergeOptionType.OVERWRITE_SCHEMA,
                     partition_columns: list[str] = None):
        easy_df = EasySparkDF.create(EasySparkDeltaTable._spark, df)
        return self.save(easy_df, save_mode_type, merge_option_type, partition_columns)

    def save(self, easy_df: EasySparkDF = None, save_mode_type: EasySaveModeType = EasySaveModeType.OVER_WRITE,
             merge_option_type: EasyMergeOptionType = EasyMergeOptionType.OVERWRITE_SCHEMA,
             partition_columns: list[str] = None) -> 'EasySparkDeltaTable':
        if not easy_df:
            easy_df = self.to_easy_df()

        if self.for_name:
            easy_df.save_as_table(self.path, save_mode_type=save_mode_type, merge_option_type=merge_option_type,
                                  partition_columns=partition_columns)
        else:
            easy_df.save_to_table_from_path(self.path, save_mode_type=save_mode_type,
                                            merge_option_type=merge_option_type,
                                            partition_columns=partition_columns)

        return self

    def merge_from_list(self, merge_type: EasyMergeType, keys: list[str], records: list[dict],
                        schema: StructType = None,
                        add_missing_columns=True, add_missing_columns_to_current=False, ignore_order=False,
                        to_keys: dict[str, any] = None) -> 'EasySparkDeltaTable':

        if schema is None:
            easy_df = self.to_easy_df()
            schema = easy_df.current_schema

        if ignore_order:
            rows = [Row(**record) for record in records]
            df = EasySparkDeltaTable._spark.createDataFrame(rows, schema)
        else:
            pdf_df = pd.DataFrame(records)
            df = EasySparkDeltaTable._spark.createDataFrame(pdf_df, schema)

        return self.merge_from_df(merge_type, keys, df, add_missing_columns, add_missing_columns_to_current, to_keys)

    def merge_from_tuple(self, merge_type: EasyMergeType, keys: list[str], records: list[tuple],
                         schema: StructType = None,
                         add_missing_coloumns=True, add_missing_columns_to_current=False,
                         to_keys: dict[str, any] = None) -> 'EasySparkDeltaTable':
        if schema is None:
            easy_df = self.to_easy_df()
            schema = easy_df.current_schema

        df = EasySparkDeltaTable._spark.createDataFrame(records, schema)
        return self.merge_from_df(merge_type, keys, df, add_missing_coloumns, add_missing_columns_to_current, to_keys)

    def merge_from_df(self, merge_type: EasyMergeType, keys: list[str], df: DataFrame, add_missing_coloumns=True,
                      add_missing_columns_to_current=False, to_keys: dict[str, any] = None) -> 'EasySparkDeltaTable':
        current_easy_df = self.to_easy_df()
        current_df = current_easy_df.df
        df_columns = df.columns
        current_columns = current_df.columns

        if add_missing_coloumns:
            for current_column in current_columns:
                if current_column not in df_columns:
                    df = df.withColumn(current_column, lit(None).cast(current_df.schema[current_column].dataType))

        if add_missing_columns_to_current:
            current_df_has_new_columns = False
            for df_column in df_columns:
                if df_column not in current_columns:
                    current_df = current_df.withColumn(df_column, lit(None).cast(df.schema[df_column].dataType))
                    current_df_has_new_columns = True

            if current_df_has_new_columns:
                self.save_from_df(current_df, save_mode_type=EasySaveModeType.OVER_WRITE,
                                  merge_option_type=EasyMergeOptionType.OVERWRITE_SCHEMA)
                self.init_delta()

        merge_relationships = [f"A.`{key}` = B.`{key}` and " for key in keys]
        merge_relationships = "".join(merge_relationships)[:-4]

        if to_keys:
            to_conditions = EasySparkDeltaHelpers.build_condition(to_keys, "", "A")
            merge_relationships += f"And {to_conditions}"

        merge_entry = self._delta_path.alias('A').merge(
            df.alias('B'),
            merge_relationships
        )

        if merge_type == EasyMergeType.UPDATE_AND_INSERT:
            merge_entry = merge_entry.whenMatchedUpdateAll().whenNotMatchedInsertAll()
        elif merge_type == EasyMergeType.UPDATE_ONLY:
            merge_entry = merge_entry.whenMatchedUpdateAll()
        elif merge_type == EasyMergeType.INSERT_ONLY:
            merge_entry = merge_entry.whenNotMatchedInsertAll()

        merge_entry.execute()

        return self

    def optimize(self):
        if self.for_name:
            self.df_optimize.optimize_from_lh_table(self.path)
        else:
            self.df_optimize.optimize_from_path(self.path)

    def vacuum(self):
        if self.for_name:
            self.df_optimize.vacuum_from_lh_table(self.path)
        else:
            self.df_optimize.vacuum_from_path(self.path)

    # Private Method
    @staticmethod
    def _build_condition(keys: dict[str, any]):
        return EasySparkDeltaHelpers.build_condition(keys)
