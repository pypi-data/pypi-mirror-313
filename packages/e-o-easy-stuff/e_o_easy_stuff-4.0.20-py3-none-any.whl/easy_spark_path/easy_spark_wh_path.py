from easy_spark_path.easy_path import Path
from easy_spark_path.easy_spark_simple_table_path import EasySparkSimpleTablePath


class EasySparkWHPath(EasySparkSimpleTablePath):
    def __init__(self, path: Path, schema: str, table_name: str):
        super().__init__(path, schema, table_name, is_lh=False)
