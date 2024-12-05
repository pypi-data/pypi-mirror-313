from easy_spark.easy_spark_instance import EasySparkInstance
from easy_utils.easy_singleton import easy_singleton


@easy_singleton
class EasySparkCatalog:
    def __init__(self, spark):
        self.spark_instance = EasySparkInstance(spark)

    def table_exists_from_table_name(self, table_name: str, db_name: str) -> bool:
        return self.spark_instance.spark.catalog._jcatalog.tableExists(table_name, db_name)

    def table_exists_from_path(self, path: str) -> bool:
        return self.spark_instance.spark.catalog._jcatalog.tableExists(path)
