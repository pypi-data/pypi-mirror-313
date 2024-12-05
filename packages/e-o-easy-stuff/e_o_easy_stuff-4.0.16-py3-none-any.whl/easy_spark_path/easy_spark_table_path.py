from easy_spark_path.easy_spark_lh_path import EasySparkLHPath
from easy_spark_path.easy_path import Path
from easy_spark_path.easy_spark_simple_table_path import EasySparkSimpleTablePath
from easy_spark_path.easy_warehouse_type import EasyWarehouseType
from easy_spark_path.easy_spark_wh_path import EasySparkWHPath


class EasySparkTablePath:
    def __init__(self, path: str, is_table_name: bool, warehouse_type: EasyWarehouseType):
        self.path = path
        self.is_table_name = is_table_name
        self.warehouse_type = warehouse_type

    @staticmethod
    def create_from_lh_table_name(lh_name: str, table_name, schema: str = None):
        path = f'{lh_name}.{schema}.{table_name}' if schema is not None else f'{lh_name}.{table_name}'
        return EasySparkTablePath(path, True, EasyWarehouseType.LH)

    @staticmethod
    def create_from_wh_table_name(wh_name: str, table_name, schema: str):
        path = f'{wh_name}.{schema}.{table_name}'
        return EasySparkTablePath(path, True, EasyWarehouseType.WH)

    @staticmethod
    def create_from_simple_table_path(simple_table_path: EasySparkSimpleTablePath) -> 'EasySparkTablePath':
        warehouse_type = EasyWarehouseType.LH if simple_table_path.is_lh else EasyWarehouseType.WH
        return EasySparkTablePath(simple_table_path.path, False, warehouse_type)

    @staticmethod
    def create_from_lh_path(lh_table_path: EasySparkLHPath) -> 'EasySparkTablePath':
        return EasySparkTablePath.create_from_simple_table_path(lh_table_path)

    @staticmethod
    def create_from_wh_path(wh_table_path: EasySparkWHPath) -> 'EasySparkTablePath':
        return EasySparkTablePath.create_from_simple_table_path(wh_table_path)

    @staticmethod
    def create_from_path(path: Path, schema: str, table_name: str, is_lh) -> 'EasySparkTablePath':
        return EasySparkTablePath.create_from_simple_table_path(
            EasySparkSimpleTablePath(path, schema, table_name, is_lh))

    @staticmethod
    def create_from_path_details(workspace_id: str, warehouse_id: str, schema: str, table_name: str,
                                 is_lh) -> 'EasySparkTablePath':
        return EasySparkTablePath.create_from_simple_table_path(
            EasySparkSimpleTablePath(Path(workspace_id, warehouse_id), schema, table_name, is_lh))
