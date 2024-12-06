from easy_spark_path.easy_spark_file_path import EasySparkFilePath
from easy_spark_path.easy_warehouse_type import EasyWarehouseType


class EasySparkDirectoryPath:
    LH_DEFAULT_FILE_PATH = '/lakehouse/default/Files'
    WH_DEFAULT_FILE_PATH = '/warehouse/default/Files'

    def __init__(self, path: str, is_relative: bool, warehouse_type: EasyWarehouseType = EasyWarehouseType.LH):
        self.path = path
        self.is_relative = is_relative
        self.warehouse_type = warehouse_type

    @staticmethod
    def create_from_path(path: str, is_relative: bool,
                         warehouse_type: EasyWarehouseType = EasyWarehouseType.LH) -> 'EasySparkDirectoryPath':
        new_path = EasySparkFilePath.build_path(path, is_relative, warehouse_type)
        return EasySparkDirectoryPath(new_path, is_relative, warehouse_type)

    @staticmethod
    def create_from_relative_path(path: str,
                                  warehouse_type: EasyWarehouseType = EasyWarehouseType.LH) -> 'EasySparkDirectoryPath':
        return EasySparkDirectoryPath.create_from_path(path, True, warehouse_type)

    @staticmethod
    def create_from_absolute_path(path: str,
                                  warehouse_type: EasyWarehouseType = EasyWarehouseType.LH) -> 'EasySparkDirectoryPath':
        return EasySparkDirectoryPath.create_from_path(path, False, warehouse_type)
