from easy_spark.easy_spark_instance import EasySparkInstance
from easy_spark_path.easy_spark_table_path import EasySparkTablePath


class EasySparkDFOptimize:
    def __init__(self, spark):
        self.spark_instance = EasySparkInstance(spark)

    def vacuum_from_lh_table_name(self, name: str, table_name: str) -> 'EasySparkDFOptimize':
        vacuum_script = f"VACUUM {name}.{table_name}"
        self.spark_instance.spark.sql(vacuum_script)
        return self

    def vacuum_from_lh_table(self, table_name: str) -> 'EasySparkDFOptimize':
        vacuum_script = f"VACUUM {table_name}"
        self.spark_instance.spark.sql(vacuum_script)
        return self

    def vacuum_from_path(self, path: str) -> 'EasySparkDFOptimize':
        vacuum_script = f"VACUUM delta.`{path}`"
        self.spark_instance.spark.sql(vacuum_script)
        return self

    def vacuum_from_table_pat(self, table_path: EasySparkTablePath) -> 'EasySparkDFOptimize':
        if table_path.is_table_name:
            return self.vacuum_from_lh_table(table_path.path)
        else:
            return self.vacuum_from_path(table_path.path)

    def optimize_from_lh_table_name(self, name: str, table_name: str) -> 'EasySparkDFOptimize':
        optimize_script = f"OPTIMIZE {name}.{table_name}"
        self.spark_instance.spark.sql(optimize_script)
        return self

    def optimize_from_lh_table(self, table_name: str) -> 'EasySparkDFOptimize':
        optimize_script = f"OPTIMIZE {table_name}"
        self.spark_instance.spark.sql(optimize_script)
        return self

    def optimize_from_path(self, path: str) -> 'EasySparkDFOptimize':
        optimize_script = f"OPTIMIZE delta.`{path}`"
        self.spark_instance.spark.sql(optimize_script)
        return self

    def optimize_from_table_pat(self, table_path: EasySparkTablePath) -> 'EasySparkDFOptimize':
        if table_path.is_table_name:
            return self.optimize_from_lh_table(table_path.path)
        else:
            return self.optimize_from_path(table_path.path)
