# TODO: Add import
from notebookutils import mssparkutils


class EasySparkMSSparkUtilsHelpers:
    def __init__(self):
        pass

    @staticmethod
    def create_directory(path: str):
        mssparkutils.fs.mkdirs(path)
