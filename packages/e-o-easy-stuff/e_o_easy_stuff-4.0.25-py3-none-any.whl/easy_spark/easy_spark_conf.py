from easy_spark.easy_spark_instance import EasySparkInstance
from pyspark.sql import SparkSession


class EasySparkConf:
    def __init__(self, spark: SparkSession = None):
        self.spark_instance = EasySparkInstance(spark)
        pass

    @staticmethod
    def create(spark: SparkSession = None):
        return EasySparkConf(spark)

    def optimize(self, optimize_write_enabled=True, rebase_mode_in_write=True, rebase_mode_in_read=True,
                 vorder_enabled: bool = False, low_shuffle_enabled: bool = False, concurrent_writes: bool = False,
                 ignore_corrupt_files: bool = False, auto_merge: bool = False, optimize_write_binsize=None):
        if rebase_mode_in_write:
            self.spark_instance.spark.conf.set("spark.sql.parquet.int96RebaseModeInWrite", "CORRECTED")
            self.spark_instance.spark.conf.set("spark.sql.parquet.datetimeRebaseModeInWrite", "CORRECTED")
        if rebase_mode_in_read:
            self.spark_instance.spark.conf.set("spark.sql.parquet.int96RebaseModeInRead", "CORRECTED")
            self.spark_instance.spark.conf.set("spark.sql.parquet.datetimeRebaseModeInRead", "CORRECTED")
        if optimize_write_enabled:
            self.spark_instance.spark.conf.set("spark.microsoft.delta.optimizeWrite.enabled", "true")
        if vorder_enabled:
            self.spark_instance.spark.conf.set("spark.sql.parquet.vorder.enabled", "true")
        if low_shuffle_enabled:
            self.spark_instance.spark.conf.set("spark.microsoft.delta.merge.lowShuffle.enabled", "true")
        if ignore_corrupt_files:
            self.spark_instance.spark.conf.set("spark.sql.files.ignoreCorruptFiles", "true")
        if auto_merge:
            self.spark_instance.spark.conf.set("spark.databricks.delta.schema.autoMerge.enabled", "true")
        if concurrent_writes:
            self.spark_instance.spark.conf.set("spark.databricks.delta.concurrentWrites", "true")
        if optimize_write_binsize:
            self.spark_instance.spark.conf.set("spark.microsoft.delta.optimizeWrite.binSize", optimize_write_binsize)
            self.spark_instance.spark.conf.set("spark.microsoft.delta.optimizedWrite.binSize", optimize_write_binsize)
