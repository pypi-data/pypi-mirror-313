from easy_spark_fs.easy_file_detail import EasyFileDetails
from easy_spark_fs.easy_spark_hoop import EasySparkHadoop
from easy_spark_path.easy_spark_file_path import EasySparkFilePath
from easy_utils.easy_singleton import easy_singleton
from datetime import datetime
from typing import Iterator


@easy_singleton
class EasySparkFSPath:
    def __init__(self, spark, must_java_import=True):
        self.easy_hadoop = EasySparkHadoop(spark, must_java_import)

    def get_fs_path_from_status(self, status):
        return status.getPath()

    def get_file_name_from_status(self, status) -> str:
        return status.getPath().getName()

    def get_file_full_path_from_status(self, status) -> str:
        return status.getPath().toString()

    def get_file_modification_time_from_status(self, status):
        return status.getModificationTime()

    def is_directory_from_status(self, status) -> bool:
        return status.isDirectory()

    def get_readable_file_modification_time_from_status(self, status) -> datetime:
        return datetime.fromtimestamp(self.get_file_modification_time_from_status(status) / 1000.0)

    def is_directory_from_fs_path(self, fs_path) -> bool:
        status = self.get_file_status_from_fs_path(fs_path)
        return self.is_directory_from_status(status)

    def delete_file_from_fs_path(self, fs_path) -> bool:
        return self.easy_hadoop.fs.delete(fs_path, True)

    def file_exists_from_fs_path(self, fs_path) -> bool:
        return self.easy_hadoop.fs.exists(fs_path)

    def file_exists_from_path(self, path: str, is_relative: bool) -> bool:
        fs_path = self.get_fs_path(path, is_relative)
        return self.file_exists_from_fs_path(fs_path)

    def get_file_status_from_fs_path(self, fs_path):
        return self.easy_hadoop.fs.getFileStatus(fs_path)

    def get_fs_path(self, path: str, is_relative: bool):
        if is_relative:
            return self.get_fs_absolute_path(path)
        else:
            return self.easy_hadoop.make_path(path)

    def get_fs_path_from_file_path(self, file_path: EasySparkFilePath):
        return self.get_fs_path(file_path.path, file_path.is_relative)

    def get_fs_absolute_path(self, relative_path: str):
        fs_path = self.easy_hadoop.make_path(relative_path)
        return fs_path.makeQualified(self.easy_hadoop.fs.getUri(),
                                     self.easy_hadoop.fs.getWorkingDirectory())

    def list_statuses_from_fs_path(self, fs_path) -> list:
        return list(self.easy_hadoop.fs.listStatus(fs_path))

    def get_file_details_from_status(self, status) -> EasyFileDetails:
        is_directory = self.is_directory_from_status(status)
        file_name = self.get_file_name_from_status(status)
        fs_path = self.get_fs_path_from_status(status)
        full_path = self.get_file_full_path_from_status(status)

        if is_directory:
            return EasyFileDetails(fs_path, status, is_directory, file_name, full_path, None)

        readable_modified_time = self.get_readable_file_modification_time_from_status(status)

        return EasyFileDetails(fs_path, status, is_directory, file_name, full_path, readable_modified_time)

    def get_file_details_from_fs_path(self, fs_path) -> EasyFileDetails:
        status = self.get_file_status_from_fs_path(fs_path)
        return self.get_file_details_from_status(status)

    def get_file_details_from_path(self, path: str, is_relative: bool) -> EasyFileDetails:
        fs_path = self.get_fs_path(path, is_relative)
        return self.get_file_details_from_fs_path(fs_path)

    def list_path_details_from_fs_path(self, fs_path) -> Iterator[EasyFileDetails]:
        statuses = self.list_statuses_from_fs_path(fs_path)
        for status in statuses:
            yield self.get_file_details_from_status(status)

    def list_path_details_from_path(self, path: str, is_relative: bool) -> Iterator[EasyFileDetails]:
        fs_path = self.get_fs_path(path, is_relative)
        return self.list_path_details_from_fs_path(fs_path)
