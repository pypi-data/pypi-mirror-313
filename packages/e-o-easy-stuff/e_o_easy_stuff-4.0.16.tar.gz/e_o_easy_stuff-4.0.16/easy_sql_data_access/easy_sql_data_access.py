class EasySQLDataAccess:
    def __init__(self, con):
        self.con = con

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
        result = cursor.execute(sql_command, parameters)
        return result

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
