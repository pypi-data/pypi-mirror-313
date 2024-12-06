from easy_sql_data_access.easy_sql_data_connection_builder import EasySQLDataConnectionBuilder
from easy_sql_data_access.easy_sql_manage_data_access import EasySQLManageDataAccess


class EasySQLDataAccessFactory:
    def __init__(self, constr: str, autocommit: bool = True):
        self.constr = constr
        self.autocommit = autocommit

    @staticmethod
    def create_from_builder(builder: EasySQLDataConnectionBuilder):
        return EasySQLDataAccessFactory(builder.constr)

    def open(self, autocommit: bool = None) -> EasySQLManageDataAccess:
        if autocommit is None:
            autocommit = self.autocommit
        return EasySQLManageDataAccess(self.constr, autocommit)
