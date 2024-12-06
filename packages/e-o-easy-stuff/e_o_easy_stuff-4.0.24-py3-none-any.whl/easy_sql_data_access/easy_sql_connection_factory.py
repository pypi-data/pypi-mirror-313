from easy_sql_data_access.easy_open_data_connection import easy_open_data_connection
from easy_sql_data_access.easy_sql_data_connection_builder import EasySQLDataConnectionBuilder


class EasySQLConnectionFactory:
    def __init__(self, constr: str, autocommit: bool = True):
        self.constr = constr
        self.autocommit = autocommit

    @staticmethod
    def create_from_builder(builder: EasySQLDataConnectionBuilder):
        return EasySQLConnectionFactory(builder.constr)

    def open(self, autocommit: bool = None) -> easy_open_data_connection:
        if autocommit is None:
            autocommit = self.autocommit
        return easy_open_data_connection(self.constr, autocommit)
