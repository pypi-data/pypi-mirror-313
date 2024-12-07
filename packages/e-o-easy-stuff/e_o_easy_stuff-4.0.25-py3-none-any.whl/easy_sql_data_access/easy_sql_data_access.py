from typing import Tuple


class EasySQLDataAccess:
    def __init__(self, con):
        self.con = con

    @staticmethod
    def create(con):
        return EasySQLDataAccess(con)

    def new_cursor(self):
        if self.con is None:
            raise ValueError("Connection is not open")
        return self.con.cursor()

    @staticmethod
    def execute_cursor(cursor, sql_command: str) -> any:
        result = cursor.execute(sql_command)
        return result

    @staticmethod
    def execute_cursor_with_parameters(cursor, sql_command: str, parameters: tuple) -> any:
        if parameters:
            return cursor.execute(sql_command, parameters)
        else:
            return cursor.execute(sql_command)

    def execute(self, sql_command: str):
        cursor = self.new_cursor()
        try:
            self.execute_cursor(cursor, sql_command)
        finally:
            cursor.close()

    def execute_with_parameters(self, sql_command: str, parameters: tuple):
        cursor = self.new_cursor()
        try:
            self.execute_cursor_with_parameters(cursor, sql_command, parameters)
        finally:
            cursor.close()

    def query_list_dict(self, sql_command: str, parameters: tuple = None) -> list[dict[str, any]]:
        print('Querying...', sql_command)
        cursor = self.new_cursor()
        try:
            result = self.execute_cursor_with_parameters(cursor, sql_command, parameters)
            list_result = [{column[0]: value for column, value in zip(result.description, row)} for row in
                           result.fetchall()]
            return list_result
        finally:
            cursor.close()

    def query_dict(self, sql_command: str, parameters: tuple = None) -> dict[str, any]:
        cursor = self.new_cursor()
        try:
            result = self.execute_cursor_with_parameters(cursor, sql_command, parameters)
            return {column[0]: value for column, value in zip(result.description, result.fetchone())}
        finally:
            cursor.close()

    def query_list_tuple(self, sql_command: str, parameters: tuple = None) -> list[tuple]:
        cursor = self.new_cursor()
        try:
            result = self.execute_cursor_with_parameters(cursor, sql_command, parameters)
            return result.fetchall()
        finally:
            cursor.close()

    def query_tuple(self, sql_command: str, parameters: tuple = None) -> tuple:
        cursor = self.new_cursor()
        try:
            result = self.execute_cursor_with_parameters(cursor, sql_command, parameters)
            return result.fetchone()
        finally:
            cursor.close()

    def update(self, table_name: str, id_column_name: str, id: any, entity: dict[str, any]):
        sql = f"UPDATE {table_name} SET " + ', '.join(
            [f"{key} = ?" for key in entity.keys()]) + f" WHERE {id_column_name} = ?"
        self.execute_with_parameters(sql, tuple(entity.values()) + (id,))

        pass

    def patch(self, table_name: str, id_column_name: str, id: any, entity: dict[str, any]):
        sql = f"UPDATE {table_name} SET " + ', '.join(
            [f"{key} = ?" for key in entity.keys()]) + f" WHERE {id_column_name} = ?"
        self.execute_with_parameters(sql, tuple(entity.values()) + (id,))

        pass

    def insert(self, table_name: str, entity: dict[str, any]):
        sql = f"INSERT INTO {table_name} ({', '.join(entity.keys())}) VALUES ({', '.join(['?' for _ in entity.keys()])})"
        self.execute_with_parameters(sql, tuple(entity.values()))

        pass

    def upsert(self, table_name: str, id_column_name: str, id: any, entity: dict[str, any]):
        dict_record = self.get(table_name, id_column_name, id)
        if dict_record:
            self.update(table_name, id_column_name, id, entity)
        else:
            self.insert(table_name, entity)

        pass

    def delete(self, table_name: str, id_column_name: str, id: any):
        sql = f"DELETE FROM {table_name} WHERE {id_column_name} = ?"
        self.execute_with_parameters(sql, (id,))

        pass

    def get_list(self, table_name: str) -> list[dict[str, any]]:
        sql = f"SELECT * FROM {table_name}"
        dict_list = self.query_list_dict(sql)
        return dict_list

    def get_list_with_filters(self, table_name: str, filters: dict[str, any]) -> list[dict[str, any]]:
        sql = f"SELECT * FROM {table_name} WHERE " + ' AND '.join([f"{key} = ?" for key in filters.keys()])

        dict_list = self.query_list_dict(sql, tuple(filters.values()))
        return dict_list

    def get(self, table_name: str, id_column_name: str, id: any) -> dict[str, any]:
        sql = f"SELECT * FROM {table_name} WHERE {id_column_name} = ?"
        dict_record = self.query_dict(sql, (id,))
        return dict_record

        pass

    def get_with_filters(self, table_name: str, filters: dict[str, any]) -> dict[str, any]:
        sql = f"SELECT * FROM {table_name} WHERE " + ' AND '.join([f"{key} = ?" for key in filters.keys()])
        dict_record = self.query_dict(sql, tuple(filters.values()))
        return dict_record

        pass

    def get_list_from_sql(self, sql: str, values: Tuple = None) -> list[dict[str, any]]:
        dict_list = self.query_list_dict(sql, values)
        return dict_list
