from easy_spark_path.easy_file_type import EasyFileType
from easy_spark_path.easy_warehouse_type import EasyWarehouseType


class EasySparkFilePath:
    LH_DEFAULT_FILE_PATH = '/lakehouse/default/Files'
    WH_DEFAULT_FILE_PATH = '/warehouse/default/Files'

    def __init__(self, path: str, is_relative: bool, extension: str, file_type: EasyFileType,
                 warehouse_type: EasyWarehouseType = EasyWarehouseType.LH):
        self.path = path
        self.extension = extension.upper()
        self.file_type = file_type
        self.is_relative = is_relative
        self.warehouse_type = warehouse_type

    @staticmethod
    def create_from_path(path: str, is_relative: bool, file_type: EasyFileType = None,
                         warehouse_type: EasyWarehouseType = EasyWarehouseType.LH) -> 'EasySparkFilePath':
        extension = EasySparkFilePath.get_extension_from_path(path)
        if extension is None and file_type is not None:
            extension = EasySparkFilePath.get_extension_from_file_type(file_type)
        if extension is None:
            raise ValueError('Extension is required')
        if file_type is None:
            file_type = EasySparkFilePath.get_file_type_from_extension(extension)
        if file_type == EasyFileType.UNKNOWN:
            raise ValueError('Unknown file type')
        new_path = EasySparkFilePath.build_path(path, is_relative, warehouse_type)
        new_path = EasySparkFilePath.build_path_with_extension(new_path, extension)
        return EasySparkFilePath(new_path, is_relative, extension, file_type, warehouse_type)

    @staticmethod
    def create_from_relative_path(path: str, file_type: EasyFileType = None,
                                  warehouse_type: EasyWarehouseType = EasyWarehouseType.LH) -> 'EasySparkFilePath':
        return EasySparkFilePath.create_from_path(path, True, file_type, warehouse_type)

    @staticmethod
    def create_from_absolute_path(path: str, file_type: EasyFileType = None,
                                  warehouse_type: EasyWarehouseType = EasyWarehouseType.LH) -> 'EasySparkFilePath':
        return EasySparkFilePath.create_from_path(path, False, file_type, warehouse_type)

    @staticmethod
    def build_path(path: str, is_relative: bool, warehouse_type: EasyWarehouseType = EasyWarehouseType.LH) -> str:
        default_path = EasySparkFilePath.LH_DEFAULT_FILE_PATH if warehouse_type == EasyWarehouseType.LH else EasySparkFilePath.WH_DEFAULT_FILE_PATH
        new_path = path

        if is_relative and default_path not in path:
            if new_path[-1] == '/':
                new_path = new_path[:-1]
            if new_path[0] == '/':
                new_path = new_path[1:]
            new_path = f"{default_path}/{path}"

        return new_path

    @staticmethod
    def build_path_with_extension(path: str, extension: str) -> str:
        if '.' in path:
            return path
        return f"{path}.{extension}"

    @staticmethod
    def get_extension_from_path(path: str) -> str | None:
        if '.' not in path:
            return None
        return (path.split('.')[-1]).upper()

    @staticmethod
    def get_file_type_from_extension(extension: str) -> EasyFileType:
        if extension in ['CSV', 'JSON', 'PARQUET', 'AVRO']:
            return EasyFileType(extension)
        return EasyFileType.UNKNOWN

    @staticmethod
    def get_extension_from_file_type(file_type: EasyFileType) -> str:
        return file_type.value.upper()
