from pyspark.sql import SparkSession
from easy_utils.easy_singleton import easy_singleton


@easy_singleton
class EasySparkInstance:

    def __init__(self, spark: SparkSession = None):
        if spark:
            self._spark = spark
        pass

    @property
    def spark(self) -> SparkSession:
        return self._spark
