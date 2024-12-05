from easy_spark.easy_spark_delta_helpers import EasySparkDeltaHelpers


class EasySQLSelectBuilder:
    def __init__(self):
        self.sql: str = "SELECT"
        pass;

    def select(self, columns: list[str]) -> 'EasySQLSelectBuilder':
        self.sql += " " + ", ".join(columns)
        return self

    def from_table_name(self, table: str) -> 'EasySQLSelectBuilder':
        self.sql += f" FROM {table}"
        return self

    def from_lh_table_name(self, name: str, table_name: str) -> 'EasySQLSelectBuilder':
        self.sql += f" FROM {name}.{table_name}"
        return self

    def from_path(self, path: str) -> 'EasySQLSelectBuilder':
        self.sql += f" FROM delta.`{path}`"
        return self

    def where(self, keys: dict[str, any]) -> 'EasySQLSelectBuilder':
        conditions = EasySparkDeltaHelpers.build_condition(keys)

        self.sql += f" WHERE {conditions}"
        return self

    def where_from_condition(self, condition: str) -> 'EasySQLSelectBuilder':
        self.sql += f" WHERE {condition}"
        return self

    def limit(self, limit: int) -> 'EasySQLSelectBuilder':
        if limit:
            self.sql += f" LIMIT {limit}"
        return self

    @staticmethod
    def new() -> 'EasySQLSelectBuilder':
        return EasySQLSelectBuilder()
