from easy_sql_data_access.easy_open_data_connection import easy_open_data_connection
from easy_sql_data_access.easy_sql_data_access import EasySQLDataAccess
from easy_sql_data_access.easy_sql_data_connection_builder import EasySQLDataConnectionBuilder


class EasySQLManageDataAccess:
    def __init__(self, constr: str, autocommit: bool = True):
        self.constr = constr
        self.autocommit = autocommit

    @staticmethod
    def create_from_builder(builder: EasySQLDataConnectionBuilder, autocommit: bool = True):
        return EasySQLManageDataAccess(builder.constr, autocommit)

    def __enter__(self):
        print('Entering Data Access...')
        self.con_cm = easy_open_data_connection(self.constr, self.autocommit)
        self.con = self.con_cm.__enter__()
        self.data_access = EasySQLDataAccess(self.con)
        return self.data_access

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Exiting Data Access...')
        self.con_cm.__exit__(exc_type, exc_val, exc_tb)
