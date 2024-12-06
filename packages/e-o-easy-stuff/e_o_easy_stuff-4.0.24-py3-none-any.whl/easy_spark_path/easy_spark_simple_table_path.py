from easy_spark_path.easy_path import Path


class EasySparkSimpleTablePath:
    def __init__(self, path: Path, schema: str, table_name: str, is_lh: bool = False):
        self.base_path = path
        self.schema = schema
        self.table_name = table_name
        self.is_lh = is_lh

        if is_lh:
            self.path = f"{path.path}/Tables/{table_name}"
        else:
            self.path = f"{path.path}/Tables/{schema}/{table_name}"
