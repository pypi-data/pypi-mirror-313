from pyspark.sql import SparkSession
from datetime import datetime
from easy_spark_fs.easy_spark_fs_path import EasySparkFSPath
from easy_spark_fs.easy_spark_hoop import EasySparkHadoop
from easy_spark_path.easy_spark_file_path import EasySparkFilePath


class EasySparkFSFile:
    def __init__(self, spark: SparkSession = None, path: str = None, must_java_import=True, is_relative: bool = False):
        self.easy_spark_hadoop = EasySparkHadoop(spark, must_java_import)
        self.easy_spark_fs_path = EasySparkFSPath(spark)
        self.fs_path = None
        self.path: str = path
        self.file_status = None

        if self.path:
            self.from_path(self.path, is_relative)

    @staticmethod
    def create(spark: SparkSession = None, path: str = None, must_java_import=False,
               is_relative: bool = False) -> 'EasySparkFSFile':
        return EasySparkFSFile(spark, path, must_java_import, is_relative)

    @staticmethod
    def create_from_file_path(spark: SparkSession = None, file_path: EasySparkFilePath = None,
                              must_java_import=False) -> 'EasySparkFSFile':
        return EasySparkFSFile(spark, file_path.path, must_java_import, file_path.is_relative)

    def from_path(self, path: str, is_relative: bool = False) -> 'EasySparkFSFile':
        self.path = path
        self.fs_path = self.easy_spark_fs_path.get_fs_path(self.path, is_relative)
        self.init_file_status()
        return self

    def init_file_status(self) -> 'EasySparkFSFile':
        if self.fs_path and self.file_exists():
            self.file_status = self.easy_spark_fs_path.get_file_status_from_fs_path(self.fs_path)
        return self

    def file_exists(self) -> bool:
        return self.easy_spark_fs_path.file_exists_from_fs_path(self.fs_path)

    def get_file_status(self):
        return self.file_status

    def get_modified_time(self):
        return self.easy_spark_fs_path.get_file_modification_time_from_status(self.file_status)

    def get_readable_modified_time(self) -> datetime:
        return self.easy_spark_fs_path.get_readable_file_modification_time_from_status(self.file_status)

    def get_name(self) -> str:
        return self.easy_spark_fs_path.get_file_name_from_status(self.file_status)

    def get_full_path(self) -> str:
        return self.easy_spark_fs_path.get_file_full_path_from_status(self.file_status)

    def delete_file(self) -> bool:
        return self.easy_spark_fs_path.delete_file_from_fs_path(self.fs_path)

    def write_file_content(self, content: any, delete_if_exists: bool = False) -> bool:
        if delete_if_exists:
            if self.file_exists():
                self.delete_file()
        elif self.file_exists():
            return False

        output_stream = self.easy_spark_hadoop.fs.create(self.fs_path)
        try:
            output_stream.write(content)
        finally:
            output_stream.close()

        return True
