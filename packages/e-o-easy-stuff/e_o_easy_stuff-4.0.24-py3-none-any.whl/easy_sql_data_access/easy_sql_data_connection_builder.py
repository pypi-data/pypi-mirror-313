class EasySQLDataConnectionBuilder:
    def __init__(self, constr: str):
        self.constr = constr

    @staticmethod
    def init_using_credentials(server: str, database: str, username: str, password: str):
        constr = (
            f"Driver={{ODBC Driver 18 for SQL Server}};"
            f"Server={server};"
            f"Database={database};"
            f"UID={username};"
            f"PWD={password};"
            f"Authentication=ActiveDirectoryPassword;"
            f"Encrypt=yes;"
            f"TrustServerCertificate=no;"
            f"Connection Timeout=30;"
        )
        return EasySQLDataConnectionBuilder(constr)
