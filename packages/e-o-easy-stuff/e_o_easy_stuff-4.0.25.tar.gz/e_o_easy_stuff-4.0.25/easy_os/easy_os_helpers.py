import os


class EasyOS:
    @staticmethod
    def get_file_name_from_path(path: str) -> str:
        return os.path.basename(path)

    @staticmethod
    def delete_directory(path: str) -> None:
        os.rmdir(path)

    @staticmethod
    def delete_directory_if_exists(path: str) -> None:
        if os.path.exists(path):
            EasyOS.delete_directory(path)

    @staticmethod
    def delete_file(path: str) -> None:
        os.remove(path)

    @staticmethod
    def delete_file_if_exists(path: str) -> None:
        if os.path.exists(path):
            EasyOS.delete_file(path)

    @staticmethod
    def create_directory(path: str, exist_ok=True) -> None:
        os.makedirs(path, exist_ok=exist_ok)

    @staticmethod
    def create_directory_if_not_exists(path: str) -> None:
        if not os.path.exists(path):
            EasyOS.create_directory(path)

    @staticmethod
    def get_file_extension_from_path(path: str) -> str:
        return os.path.splitext(path)[1]

    @staticmethod
    def get_file_name_without_extension(path: str) -> str:
        return os.path.splitext(os.path.basename(path))[0]

    @staticmethod
    def get_file_name_and_extension(path: str) -> tuple[str, str]:
        return os.path.splitext(os.path.basename(path))

    @staticmethod
    def get_parent_directory(path: str) -> str:
        return os.path.dirname(path)

    @staticmethod
    def get_parent_directory_name(path: str) -> str:
        return os.path.basename(os.path.dirname(path))

    @staticmethod
    def get_parent_directory_path(path: str) -> str:
        return os.path.dirname(path)

    @staticmethod
    def get_parent_directory_name_and_path(path: str) -> tuple[str, str]:
        return os.path.basename(os.path.dirname(path)), os.path.dirname(path)
