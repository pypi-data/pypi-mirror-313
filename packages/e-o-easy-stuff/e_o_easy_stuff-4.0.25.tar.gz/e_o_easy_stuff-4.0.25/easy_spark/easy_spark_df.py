from pyspark.sql import Row
from pyspark.sql.functions import *
from pyspark.sql.types import StructField
from easy_panda.easy_panda import EasyPanda
from easy_spark.easy_format_type import EasyFormatType
from easy_spark.easy_save_type import EasySaveType
from easy_spark.easy_merge_option_type import EasyMergeOptionType
from easy_spark.easy_save_mode_type import EasySaveModeType
from easy_spark.easy_spark_delta_helpers import EasySparkDeltaHelpers
from easy_spark.easy_spark_df_optimize import EasySparkDFOptimize
from easy_spark.easy_spark_instance import EasySparkInstance
from easy_spark.easy_sql_builder import EasySQLSelectBuilder
from easy_spark_path.easy_file_type import EasyFileType
from easy_spark_path.easy_spark_directory_path import EasySparkDirectoryPath
from easy_spark_path.easy_spark_file_path import EasySparkFilePath
from easy_spark_path.easy_spark_table_path import EasySparkTablePath
from easy_spark_path.easy_spark_simple_table_path import EasySparkSimpleTablePath
from pyspark.sql import SparkSession
from datetime import datetime
import numpy as np
from pandas import DataFrame as DataFramePandas
import pandas as pd
from typing import Callable
from pyspark.sql.window import Window


class EasySparkDF:
    _spark: SparkSession = None

    # Constructor
    def __init__(self, df: DataFrame = None, spark: SparkSession = None):
        self._df: DataFrame = df
        EasySparkDF._spark = spark
        self.spark_instance = EasySparkInstance(spark)

    @staticmethod
    def create(spark: SparkSession, df: DataFrame = None) -> 'EasySparkDF':
        return EasySparkDF(df, spark)

    @staticmethod
    def create_empty(spark: SparkSession, schema: StructType = None) -> 'EasySparkDF':
        return EasySparkDF(None, spark).empty(schema)

    @property
    def df(self) -> DataFrame:
        return self._df

    @df.setter
    def df(self, value: DataFrame):
        self._df = value

    @property
    def current_schema(self) -> StructType:
        return self._df.schema if self._df and self._df.schema else None

    def from_simple_table_path(self, simple_table_path: EasySparkSimpleTablePath, df_format="delta",
                               options: list[tuple[str, any]] = None) -> 'EasySparkDF':
        return self.from_path(simple_table_path.path, df_format, options)

    def from_table_path(self, table_path: EasySparkTablePath, df_format="delta",
                        options: list[tuple[str, any]] = None) -> 'EasySparkDF':
        if table_path.is_table_name:
            return self.from_lh_table_path(table_path.path)
        else:
            return self.from_path(table_path.path, df_format, options)

    def from_path(self, path: str, df_format="delta", options: list[tuple[str, any]] = None) -> 'EasySparkDF':
        entry = EasySparkDF._spark.read.format(df_format)
        if options:
            for option in options:
                entry = entry.option(option[0], option[1])
        self._df = entry.load(path)
        return self

    def from_lh_table_name(self, name: str, table_name: str, limit: int = None) -> 'EasySparkDF':
        sql_builder = EasySQLSelectBuilder.new().select(["*"]).from_lh_table_name(name, table_name).limit(limit)
        return self.from_sql(sql_builder.sql)

    def from_lh_table_path(self, path: str, limit: int = None) -> 'EasySparkDF':
        sql_builder = EasySQLSelectBuilder.new().select(["*"]).from_path(path).limit(limit)
        return self.from_sql(sql_builder.sql)

    def from_lh_table_name_using_sql(self, name: str, table_name: str, limit: int = None) -> 'EasySparkDF':
        if limit:
            self._df = EasySparkDF._spark.sql(f"SELECT * FROM {name}.{table_name} LIMIT {limit}")
        else:
            self._df = EasySparkDF._spark.sql(f"SELECT * FROM {name}.{table_name}")

        return self

    def from_sql_builder(self, sql_builder: EasySQLSelectBuilder) -> 'EasySparkDF':
        return self.from_sql(sql_builder.sql)

    def from_dict(self, records: dict, schema: StructType = None) -> 'EasySparkDF':
        new_schema = schema if schema is not None else self.current_schema
        self._df = EasySparkDF._spark.createDataFrame([Row(**records)], new_schema)
        return self

    def from_list(self, records: list[dict], schema: StructType = None, ignore_order=False) -> 'EasySparkDF':
        new_schema = schema if schema is not None else self.current_schema

        if ignore_order:
            rows = [Row(**record) for record in records]
            self._df = EasySparkDF._spark.createDataFrame(rows, new_schema)
        else:
            pdf_df = pd.DataFrame(records)
            self.from_pandas(pdf_df, new_schema)

        return self

    def from_tuple(self, records: list[tuple], schema: StructType = None) -> 'EasySparkDF':
        new_schema = schema if schema is not None else self.current_schema
        self._df = EasySparkDF._spark.createDataFrame(records, new_schema)
        return self

    def from_sql(self, sql: str) -> 'EasySparkDF':
        self._df = EasySparkDF._spark.sql(sql)
        return self

    def from_json(self, json: str) -> 'EasySparkDF':
        self._df = EasySparkDF._spark.read.json(json)
        return self

    def from_csv(self, csv_path: str, header=True, seperator=",", infer_schema=True) -> 'EasySparkDF':
        self._df = EasySparkDF._spark.read.option("header", header).csv(csv_path, sep=seperator,
                                                                        inferSchema=infer_schema)

        return self

    def from_file_path_csv(self, path: str, header=True, options: list[tuple[str, any]] = None) -> 'EasySparkDF':
        entry = EasySparkDF._spark.read.format("csv")
        if header:
            entry = entry.option("header", "true")
        if options:
            for option in options:
                entry = entry.option(option[0], option[1])
        self._df = entry.load(path)

        return self

    def from_file_path_parquet(self, path: str, options: list[tuple[str, any]] = None) -> 'EasySparkDF':
        entry = EasySparkDF._spark.read.format("parquet")
        if options:
            for option in options:
                entry = entry.option(option[0], option[1])

        self._df = entry.parquet(path)
        return self

    def from_file_path_json(self, path: str, multiline=True, options: list[tuple[str, any]] = None) -> 'EasySparkDF':
        entry = EasySparkDF._spark.read.format("json")
        if multiline:
            entry = entry.option("multiline", "true")
        if options:
            for option in options:
                entry = entry.option(option[0], option[1])

        self._df = entry.json(path)
        return self

    def from_file_path(self, file_path: EasySparkFilePath, header=True, multiline=True,
                       options: list[tuple[str, any]] = None) -> 'EasySparkDF':
        if file_path.file_type == EasyFileType.CSV:
            return self.from_file_path_csv(file_path.path, header, options)
        elif file_path.file_type == EasyFileType.PARQUET:
            return self.from_file_path_parquet(file_path.path, options)
        elif file_path.file_type == EasyFileType.JSON:
            return self.from_file_path_json(file_path.path, multiline, options)
        else:
            raise ValueError('File type not supported')

    def from_directory_path_using_wildcard(self, directory_path: EasySparkDirectoryPath, file_type: EasyFileType,
                                           header=True,
                                           multiline=True,
                                           options: list[tuple[str, any]] = None) -> 'EasySparkDF':
        path = directory_path.path
        # Check if path ends with / if not add it
        if path[-1] != '/':
            path = path + '/'
        path = path + "*." + file_type.value

        if file_type == EasyFileType.CSV:
            return self.from_file_path_csv(path, header, options)
        elif file_type == EasyFileType.PARQUET:
            return self.from_file_path_parquet(path, options)
        elif file_type == EasyFileType.JSON:
            return self.from_file_path_json(path, multiline, options)
        else:
            raise ValueError('File type not supported')

    def from_easy_panda(self, easy_panda: EasyPanda, schema: StructType = None) -> 'EasySparkDF':
        return self.from_pandas(easy_panda.pd_df, schema)

    def from_pandas(self, pd_df: DataFramePandas, schema: StructType = None) -> 'EasySparkDF':
        new_schema = schema if schema is not None else self.current_schema
        self._df = EasySparkDF._spark.createDataFrame(pd_df, new_schema)

        return self

    def clear(self) -> 'EasySparkDF':
        self._df = EasySparkDF._spark.createDataFrame([], StructType([]))

        return self

    def empty(self, schema: StructType = None) -> 'EasySparkDF':
        new_schema = schema if schema is not None else self.current_schema
        self._df = EasySparkDF._spark.createDataFrame([], new_schema)

        return self

    def filter_by_filter(self, condition: str) -> 'EasySparkDF':
        self._df = self._df.filter(condition)
        return self

    def filter_by_any(self, condition: any) -> 'EasySparkDF':
        self._df = self._df.filter(condition)
        return self

    def filter(self, keys: dict[str, any] = None):
        for key in keys:
            self._df = self._df[self._df[key] == keys[key]]

        return self

    def filter_using_filter(self, keys: dict[str, any] = None):
        if keys:
            conditions = EasySparkDeltaHelpers.build_condition(keys)
            self._df = self._df.filter(conditions)

        return self

    def where_using_where(self, keys: dict[str, any] = None) -> 'EasySparkDF':
        if keys:
            conditions = EasySparkDeltaHelpers.build_condition(keys)
            self._df = self._df.where(conditions)
        return self

    def where(self, condition: str) -> 'EasySparkDF':
        if condition:
            self._df = self._df.where(condition)
        return self

    def where_by_any(self, condition: any) -> 'EasySparkDF':
        if condition:
            self._df = self._df.where(condition)
        return self

    def combine_from_df(self, df: DataFrame, type: str = 'unionByName',
                        allow_missing_columns: bool = True) -> 'EasySparkDF':
        self._df = EasySparkDeltaHelpers.combine_from_dfs([self._df, df], type, allow_missing_columns)
        return self

    def combine_from_pd_df(self, pd_df: DataFramePandas, schema: StructType = None, type: str = 'unionByName',
                           allow_missing_columns: bool = True) -> 'EasySparkDF':
        new_schema = schema if schema is not None else self.current_schema
        df = EasySparkDF._spark.createDataFrame(pd_df, new_schema)
        return self.combine_from_df(df, type, allow_missing_columns)

    def rename_column_empty_spaces(self, value="") -> 'EasySparkDF':
        for col_name in self._df.columns:
            self._df = self._df.withColumnRenamed(col_name, col_name.replace(" ", value))
        return self

    def rename_column_invalid_chars(self, invalid_chars=",;{}()", value="") -> 'EasySparkDF':
        for col_name in self._df.columns:
            current_col_name = col_name
            for c in invalid_chars:
                current_col_name = current_col_name.replace(c, value)
            self._df = self._df.withColumnRenamed(col_name, current_col_name)

        return self

    def rename_column_wildcard(self, from_value="", value="") -> 'EasySparkDF':
        for col_name in self._df.columns:
            current_col_name = col_name
            current_col_name = current_col_name.replace(from_value, value)
            self._df = self._df.withColumnRenamed(col_name, current_col_name)

        return self

    def rename_columns(self, values: dict[str, str]):
        for col_name in self._df.columns:
            if col_name in values:
                self._df = self._df.withColumnRenamed(col_name, values[col_name])

        return self

    def rename_column(self, from_value="", value=""):
        ##First check if the column exists
        if from_value in self._df.columns:
            self._df = self._df.withColumnRenamed(from_value, value)

        return self

    def drop_column_if_exists(self, column_name: str) -> 'EasySparkDF':
        if column_name in self._df.columns:
            self._df = self._df.drop(column_name)
        return self

    def add_column(self, column_name: str, value: any) -> 'EasySparkDF':
        self._df = self._df.withColumn(column_name, lit(value))
        return self

    def capitalize_column_between_spaces(self) -> 'EasySparkDF':
        for col_name in self._df.columns:
            current_col_name = col_name
            # Capitalize the first letter of each word
            for word in current_col_name.split(" "):
                current_col_name = current_col_name.replace(word, word.capitalize())
            self._df = self._df.withColumnRenamed(col_name, current_col_name)

        return self

    def title_columns(self) -> 'EasySparkDF':
        for col_name in self._df.columns:
            self._df = self._df.withColumnRenamed(col_name, col_name.title())

        return self

    def replace_nan(self, value=None) -> 'EasySparkDF':
        self._df = self._df.replace({np.nan: value}).replace({"nan": value})

        return self

    def overwrite_types(self, struct_types: dict | list[StructField] = None) -> 'EasySparkDF':
        struct_types = EasySparkDeltaHelpers.build_struct_fields(struct_types)

        for struct_t in struct_types:
            filed_r = struct_t.name.replace("`", "")
            # Check if field is in df
            if filed_r not in self._df.columns:
                continue
            self._df = self._df.withColumn(filed_r, col(struct_t.name).cast(struct_t.dataType))

        return self

    def overwrite_to_dates(self, overwrite_columns: list[tuple[str, str]]) -> 'EasySparkDF':
        for (column_name, column_date_format) in overwrite_columns:
            if column_date_format:
                self._df = self._df.withColumn(column_name,
                                               to_timestamp(self._df[column_name], column_date_format))
            else:
                self._df = self._df.withColumn(column_name, to_timestamp(self._df[column_name]))

        return self

    def add_audit_fields(self) -> 'EasySparkDF':
        now_date = datetime.now()
        date_only = now_date.date()
        self._df = self._df.withColumn("CreatedDate", lit(now_date))
        self._df = self._df.withColumn("CreatedYear", lit(now_date.year))
        self._df = self._df.withColumn("CreatedMonth", lit(now_date.month))
        self._df = self._df.withColumn("CreatedDay", lit(now_date.day))
        self._df = self._df.withColumn("CreatedDateOnly", lit(date_only))

        return self

    def remove_audit_fields(self) -> 'EasySparkDF':
        self.drop_column_if_exists("CreatedDate").drop_column_if_exists("CreatedYear").drop_column_if_exists(
            "CreatedMonth").drop_column_if_exists("CreatedDay").drop_column_if_exists("CreatedDateOnly")

        return self

    def remove_audit_field_columns(self):
        return self.remove_audit_fields()

    def add_hash_column_from_columns(self, hash_column_name: str, columns: list[str] = None) -> 'EasySparkDF':
        if not columns:
            columns = self._df.columns

        self._df = self._df.withColumn(hash_column_name, sha2(concat_ws("", *columns), 256))
        return self

    def append_from_dict(self, record: dict) -> 'EasySparkDF':
        row = Row(**record)
        return self.append_from_row(row)

    def append_from_row(self, row: Row) -> 'EasySparkDF':
        df = EasySparkDF._spark.createDataFrame([row], self._df.schema)
        self._df = self.combine_from_df(df, type='union', allow_missing_columns=True)._df
        return self

    def select(self, columns: list[str]) -> 'EasySparkDF':
        self._df = self._df.select(columns)
        return self

    def select_except(self, columns: list[str]) -> 'EasySparkDF':
        self._df = self._df.select([col for col in self._df.columns if col not in columns])
        return self

    def clone(self, new_schema: StructType = None) -> 'EasySparkDF':
        if new_schema:
            new_df = EasySparkDF._spark.createDataFrame(self._df.rdd, new_schema)
            return EasySparkDF.create(EasySparkDF._spark, new_df)
        else:
            new_df = EasySparkDF._spark.createDataFrame(self._df.rdd, self.current_schema)
            return EasySparkDF.create(EasySparkDF._spark, new_df)

    def clone_from_pd_df(self, pd_df: DataFramePandas, schema: StructType = None) -> 'EasySparkDF':
        return EasySparkDF.create(EasySparkDF._spark).from_pandas(pd_df, schema)

    def clone_from_list(self, records: list[dict], schema: StructType = None, ignore_order=False) -> 'EasySparkDF':
        return EasySparkDF.create(EasySparkDF._spark).from_list(records, schema, ignore_order)

    def copy(self, new_schema: StructType = None) -> 'EasySparkDF':
        if new_schema:
            new_df = self._df
            new_df = EasySparkDeltaHelpers.remove_columns_based_on_schema(new_df, new_schema)
            new_df = EasySparkDeltaHelpers.add_missing_columns_based_on_schema(new_df, new_schema)
            new_df = EasySparkDF._spark.createDataFrame(new_df.rdd, new_schema)

            return EasySparkDF.create(EasySparkDF._spark, new_df)
        else:
            return EasySparkDF.create(EasySparkDF._spark, self._df)

    def distinct(self, columns: list[str] = None) -> 'EasySparkDF':
        if columns:
            self._df = self._df.distinct(columns)
        else:
            self._df = self._df.distinct()
        return self

    def order_columns(self, columns: list[str]) -> 'EasySparkDF':
        # Order the columns in the order of the list
        self._df = self._df.select(columns)
        return self

    def add_partitions(self, columns: list[str]) -> 'EasySparkDF':
        self._df = self._df.repartition(*columns)
        return self

    def is_empty_or_null(self) -> bool:
        return self._df is None or self._df.isEmpty()

    def delete_empty_rows(self, columns: list[str]) -> 'EasySparkDF':
        self._df = self._df.dropna(subset=columns)
        return self

    def collect_distinct_values(self, column_name: str) -> list[any]:
        return self._df.select(column_name).distinct().rdd.map(lambda x: x[0]).collect()

    def collect_distinct_rows(self, columns: list[str]) -> list[Row]:
        return self._df.select(columns).distinct().collect()

    def collect(self) -> list[Row]:
        return self._df.collect()

    def iterator(self):
        return self._df.toLocalIterator()

    def transform(self, func: Callable[[DataFrame], DataFrame]) -> 'EasySparkDF':
        self._df = func(self._df)
        return self

    def delete_duplicates_by_cols(self, columns: list[str],
                                  *cols: Union["ColumnOrName", List["ColumnOrName_"]]) -> 'EasySparkDF':
        window_spec = Window.partitionBy(columns).orderBy(*cols)
        self._df = self._df.withColumn("row_num", row_number().over(window_spec))
        self._df = self._df.filter(self._df.row_num == 1)
        self._df = self._df.drop("row_num")
        return self

    def delete_duplicates_by_desc(self, columns: list[str], column_name: str) -> 'EasySparkDF':
        return self.delete_duplicates_by_cols(columns, col(column_name).desc())

    def save_to_table_from_table_path(self, table_path: EasySparkTablePath,
                                      save_mode_type: EasySaveModeType = EasySaveModeType.OVER_WRITE,
                                      merge_option_type: EasyMergeOptionType = EasyMergeOptionType.OVERWRITE_SCHEMA,
                                      partition_columns: list[str] = None,
                                      options: list[tuple[str, any]] = None) -> 'EasySparkDF':
        if table_path.is_table_name:
            return self.save(table_path.path, EasySaveType.TABLE, EasyFormatType.DELTA, save_mode_type,
                             merge_option_type,
                             partition_columns, options)
        else:
            return self.save(table_path.path, EasySaveType.SAVE, EasyFormatType.DELTA, save_mode_type,
                             merge_option_type,
                             partition_columns, options)

    def save_to_table_from_simple_table_path(self, simple_table_path: EasySparkSimpleTablePath,
                                             save_mode_type: EasySaveModeType = EasySaveModeType.OVER_WRITE,
                                             merge_option_type: EasyMergeOptionType = EasyMergeOptionType.OVERWRITE_SCHEMA,
                                             partition_columns: list[str] = None,
                                             options: list[tuple[str, any]] = None) -> 'EasySparkDF':
        return self.save(simple_table_path.path, EasySaveType.SAVE, EasyFormatType.DELTA, save_mode_type,
                         merge_option_type,
                         partition_columns,
                         options)

    def save_as_table(self, path: str, save_mode_type: EasySaveModeType = EasySaveModeType.OVER_WRITE,
                      merge_option_type: EasyMergeOptionType = EasyMergeOptionType.OVERWRITE_SCHEMA,
                      partition_columns: list[str] = None,
                      options: list[tuple[str, any]] = None) -> 'EasySparkDF':
        return self.save(path, EasySaveType.TABLE, EasyFormatType.DELTA, save_mode_type, merge_option_type,
                         partition_columns, options)

    def save_to_table_from_path(self, path: str, save_mode_type: EasySaveModeType = EasySaveModeType.OVER_WRITE,
                                merge_option_type: EasyMergeOptionType = EasyMergeOptionType.OVERWRITE_SCHEMA,
                                partition_columns: list[str] = None,
                                options: list[tuple[str, any]] = None) -> 'EasySparkDF':
        return self.save(path, EasySaveType.SAVE, EasyFormatType.DELTA, save_mode_type, merge_option_type,
                         partition_columns, options)

    def save_from_file_path(self, file_path: EasySparkFilePath,
                            save_mode_type: EasySaveModeType = EasySaveModeType.OVER_WRITE,
                            merge_option_type: EasyMergeOptionType = None, partition_columns: list[str] = None,
                            options: list[tuple[str, any]] = None):
        if file_path.file_type == EasyFileType.PARQUET:
            return self.save(file_path.path, EasySaveType.PARQUET, None, save_mode_type,
                             merge_option_type, partition_columns,
                             options)
        elif file_path.file_type == EasyFileType.CSV:
            return self.save(file_path.path, EasySaveType.CSV, None, save_mode_type, merge_option_type,
                             partition_columns,
                             options)
        elif file_path.file_type == EasyFileType.JSON:
            return self.save(file_path.path, EasySaveType.JSON, None, save_mode_type, merge_option_type,
                             partition_columns,
                             options)
        else:
            raise ValueError('File type not supported')

    def save(self, path: str, save_type: EasySaveType, format_type: EasyFormatType = None,
             save_mode_type: EasySaveModeType | None = EasySaveModeType.OVER_WRITE,
             merge_option_type: EasyMergeOptionType = None, partition_columns: list[str] = None,
             options: list[tuple[str, any]] = None) -> 'EasySparkDF':
        entry = self._df.write
        if format_type:
            entry = entry.format(format_type.value)
        if save_mode_type:
            entry = entry.mode(save_mode_type.value)
        if merge_option_type:
            entry = entry.option(merge_option_type.value, "true")
        if options:
            for option in options:
                entry = entry.option(option[0], option[1])
        if partition_columns:
            entry = entry.partitionBy(partition_columns)
        if save_type == EasySaveType.TABLE:
            entry.saveAsTable(path)
        elif save_type == EasySaveType.SAVE:
            entry.save(path)
        elif save_type == EasySaveType.PARQUET:
            entry.parquet(path)
        elif save_type == EasySaveType.CSV:
            entry.csv(path)
        elif save_type == EasySaveType.JSON:
            entry.json(path)

        return self
