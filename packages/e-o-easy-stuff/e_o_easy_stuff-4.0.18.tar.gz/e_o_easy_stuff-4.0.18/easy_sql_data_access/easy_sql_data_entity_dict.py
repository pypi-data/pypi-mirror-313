from easy_sql_data_access.easy_sql_data_access_factory import EasySQLDataAccessFactory


class EasySQLDataEntityDict:
    def __init__(self, data_access_factory: EasySQLDataAccessFactory,
                 table_name: str, id_column_name: str = "Id"):
        self.data_access_factory = data_access_factory
        self.table_name = table_name
        self.id_column_name = id_column_name
        pass

    def update(self, id: any, entity: dict[str, any]):
        sql = f"UPDATE {self.table_name} SET " + ', '.join(
            [f"{key} = ?" for key in entity.keys()]) + f" WHERE {self.id_column_name} = ?"
        with self.data_access_factory.open() as data_access:
            data_access.execute_with_parameters(sql, tuple(entity.values()) + (id,))

        pass

    def patch(self, id: any, entity: dict[str, any]):
        sql = f"UPDATE {self.table_name} SET " + ', '.join(
            [f"{key} = ?" for key in entity.keys()]) + f" WHERE {self.id_column_name} = ?"
        with self.data_access_factory.open() as data_access:
            data_access.execute_with_parameters(sql, tuple(entity.values()) + (id,))

        pass

    def insert(self, entity: dict[str, any]):
        sql = f"INSERT INTO {self.table_name} ({', '.join(entity.keys())}) VALUES ({', '.join(['?' for _ in entity.keys()])})"
        with self.data_access_factory.open() as data_access:
            data_access.execute_with_parameters(sql, tuple(entity.values()))

        pass

    def delete(self, id: any):
        sql = f"DELETE FROM {self.table_name} WHERE {self.id_column_name} = ?"
        with self.data_access_factory.open() as data_access:
            data_access.execute_with_parameters(sql, (id,))

        pass

    def get_list(self) -> list[dict[str, any]]:
        sql = f"SELECT * FROM {self.table_name}"
        with self.data_access_factory.open() as data_access:
            dict_list = data_access.query_list_dict(sql)
            return dict_list

    def get_list_with_filters(self, filters: dict[str, any]) -> list[dict[str, any]]:
        sql = f"SELECT * FROM {self.table_name} WHERE " + ' AND '.join([f"{key} = ?" for key in filters.keys()])
        with self.data_access_factory.open() as data_access:
            dict_list = data_access.query_list_dict(sql, tuple(filters.values()))
            return dict_list

    def get(self, id: any) -> dict[str, any]:
        sql = f"SELECT * FROM {self.table_name} WHERE {self.id_column_name} = ?"
        with self.data_access_factory.open() as data_access:
            dict_record = data_access.query_dict(sql, (id,))
            return dict_record

        pass

    def get_with_filters(self, filters: dict[str, any]) -> dict[str, any]:
        sql = f"SELECT * FROM {self.table_name} WHERE " + ' AND '.join([f"{key} = ?" for key in filters.keys()])
        with self.data_access_factory.open() as data_access:
            dict_record = data_access.query_dict(sql, tuple(filters.values()))
            return dict_record

        pass
