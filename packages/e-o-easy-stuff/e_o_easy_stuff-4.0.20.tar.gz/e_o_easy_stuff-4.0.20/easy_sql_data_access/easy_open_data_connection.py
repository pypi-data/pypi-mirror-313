from contextlib import contextmanager

import pyodbc


@contextmanager
def easy_open_data_connection(constr: str, autocommit: bool = True):
    con = None
    try:
        print('Connecting to SQL Server...')
        con = pyodbc.connect(constr, autocommit=autocommit)
        yield con
    finally:
        print('Closing connection...')
        if con:
            print('Closing connection Inside...')
            con.close()


