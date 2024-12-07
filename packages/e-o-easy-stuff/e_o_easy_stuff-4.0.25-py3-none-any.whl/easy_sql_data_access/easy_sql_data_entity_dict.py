from typing import Tuple

from easy_sql_data_access.easy_sql_data_access import EasySQLDataAccess
from easy_sql_data_access.easy_sql_data_access_factory import EasySQLDataAccessFactory
import threading


class EasySQLDataEntityDict:
    def __init__(self, data_access: EasySQLDataAccessFactory | EasySQLDataAccess,
                 table_name: str, id_column_name: str = "Id", add_lock=False):
        self.data_access = data_access
        self.table_name = table_name
        self.id_column_name = id_column_name
        self.add_lock = add_lock
        self.lock = threading.Lock()
        pass

    def update(self, id: any, entity: dict[str, any]):
        def perform_update(data_access_inner: EasySQLDataAccess):
            if self.add_lock:
                with self.lock:
                    data_access_inner.update(self.table_name, self.id_column_name, id, entity)
            else:
                data_access_inner.update(self.table_name, self.id_column_name, id, entity)

        if isinstance(self.data_access, EasySQLDataAccessFactory):
            with self.data_access.open() as data_access:
                perform_update(data_access)
        elif isinstance(self.data_access, EasySQLDataAccess):
            perform_update(self.data_access)

        pass

    def patch(self, id: any, entity: dict[str, any]):
        def perform_patch(data_access_inner: EasySQLDataAccess):
            if self.add_lock:
                with self.lock:
                    data_access_inner.patch(self.table_name, self.id_column_name, id, entity)
            else:
                data_access_inner.patch(self.table_name, self.id_column_name, id, entity)

        if isinstance(self.data_access, EasySQLDataAccessFactory):
            with self.data_access.open() as data_access:
                perform_patch(data_access)
        elif isinstance(self.data_access, EasySQLDataAccess):
            perform_patch(self.data_access)

        pass

    def insert(self, entity: dict[str, any]):
        def perform_insert(data_access_inner: EasySQLDataAccess):
            if self.add_lock:
                with self.lock:
                    data_access_inner.insert(self.table_name, entity)
            else:
                data_access_inner.insert(self.table_name, entity)

        if isinstance(self.data_access, EasySQLDataAccessFactory):
            with self.data_access.open() as data_access:
                perform_insert(data_access)
        elif isinstance(self.data_access, EasySQLDataAccess):
            perform_insert(self.data_access)

        pass

    def upsert(self, id: any, entity: dict[str, any]):
        def perform_upsert(data_access_inner: EasySQLDataAccess):
            if self.add_lock:
                with self.lock:
                    data_access_inner.upsert(self.table_name, self.id_column_name, id, entity)
            else:
                data_access_inner.upsert(self.table_name, self.id_column_name, id, entity)

        if isinstance(self.data_access, EasySQLDataAccessFactory):
            with self.data_access.open() as data_access:
                perform_upsert(data_access)
        elif isinstance(self.data_access, EasySQLDataAccess):
            perform_upsert(self.data_access)

        pass

    def delete(self, id: any):
        def perform_delete(data_access_inner: EasySQLDataAccess):
            if self.add_lock:
                with self.lock:
                    data_access_inner.delete(self.table_name, self.id_column_name, id)
            else:
                data_access_inner.delete(self.table_name, self.id_column_name, id)

        if isinstance(self.data_access, EasySQLDataAccessFactory):
            with self.data_access.open() as data_access:
                perform_delete(data_access)
        elif isinstance(self.data_access, EasySQLDataAccess):
            perform_delete(self.data_access)

        pass

    def get_list(self) -> list[dict[str, any]]:
        def perform_get_list(data_access_inner: EasySQLDataAccess) -> list[dict[str, any]]:
            if self.add_lock:
                with self.lock:
                    return data_access_inner.get_list(self.table_name)
            else:
                return data_access_inner.get_list(self.table_name)

        if isinstance(self.data_access, EasySQLDataAccessFactory):
            with self.data_access.open() as data_access:
                return perform_get_list(data_access)
        elif isinstance(self.data_access, EasySQLDataAccess):
            return perform_get_list(self.data_access)

    def get_list_with_filters(self, filters: dict[str, any]) -> list[dict[str, any]]:
        def perform_get_list_with_filters(data_access_inner: EasySQLDataAccess) -> list[dict[str, any]]:
            if self.add_lock:
                with self.lock:
                    return data_access_inner.get_list_with_filters(self.table_name, filters)
            else:
                return data_access_inner.get_list_with_filters(self.table_name, filters)

        if isinstance(self.data_access, EasySQLDataAccessFactory):
            with self.data_access.open() as data_access:
                return perform_get_list_with_filters(data_access)
        elif isinstance(self.data_access, EasySQLDataAccess):
            return perform_get_list_with_filters(self.data_access)

    def get(self, id: any) -> dict[str, any]:
        def perform_get(data_access_inner: EasySQLDataAccess) -> dict[str, any]:
            if self.add_lock:
                with self.lock:
                    return data_access_inner.get(self.table_name, self.id_column_name, id)
            else:
                return data_access_inner.get(self.table_name, self.id_column_name, id)

        if isinstance(self.data_access, EasySQLDataAccessFactory):
            with self.data_access.open() as data_access:
                return perform_get(data_access)
        elif isinstance(self.data_access, EasySQLDataAccess):
            return perform_get(self.data_access)

        pass

    def get_with_filters(self, filters: dict[str, any]) -> dict[str, any]:
        def perform_get_with_filters(data_access_inner: EasySQLDataAccess) -> dict[str, any]:
            if self.add_lock:
                with self.lock:
                    return data_access_inner.get_with_filters(self.table_name, filters)
            else:
                return data_access_inner.get_with_filters(self.table_name, filters)

        if isinstance(self.data_access, EasySQLDataAccessFactory):
            with self.data_access.open() as data_access:
                return perform_get_with_filters(data_access)
        elif isinstance(self.data_access, EasySQLDataAccess):
            return perform_get_with_filters(self.data_access)

        pass

    def get_list_from_sql(self, sql: str, values: Tuple = None) -> list[dict[str, any]]:
        def perform_get_list_from_sql(data_access_inner: EasySQLDataAccess) -> list[dict[str, any]]:
            if self.add_lock:
                with self.lock:
                    return data_access_inner.get_list_from_sql(sql, values)
            else:
                return data_access_inner.get_list_from_sql(sql, values)

        if isinstance(self.data_access, EasySQLDataAccessFactory):
            with self.data_access.open() as data_access:
                return perform_get_list_from_sql(data_access)
        elif isinstance(self.data_access, EasySQLDataAccess):
            return perform_get_list_from_sql(self.data_access)

        pass
