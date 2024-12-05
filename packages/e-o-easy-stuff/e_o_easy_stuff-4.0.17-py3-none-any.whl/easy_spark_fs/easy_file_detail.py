from datetime import datetime


class EasyFileDetails:
    def __init__(self, fs_path, file_status, is_directory: bool, file_name: str, full_path: str,
                 readable_modified_time: datetime):
        self.fs_path = fs_path
        self.file_status = file_status
        self.file_name: str = file_name
        self.full_path: str = full_path
        self.readable_modified_time: datetime = readable_modified_time
        self.is_directory: bool = is_directory
