from typing import Generic, TypeVar, Type, Tuple
import inspect
from easy_sql_data_access.easy_sql_data_access_factory import EasySQLDataAccessFactory
from easy_sql_data_access.easy_sql_data_entity_dict import EasySQLDataEntityDict
from easy_utils.easy_data_utils import EasyDataUtils
from easy_sql_data_access.easy_sql_data_access import EasySQLDataAccess

T = TypeVar('T')


class EasySQLDataEntityType(Generic[T]):
    def __init__(self, entity_type: Type[T], use_ctor: bool, data_access: EasySQLDataAccessFactory | EasySQLDataAccess,
                 table_name: str,
                 id_column_name: str = "Id", simple_map=True, add_lock=False):
        self.table_name = table_name
        self.id_column_name = id_column_name
        self.entity_type = entity_type
        self.class_parameters = inspect.signature(entity_type.__init__).parameters
        self.use_ctor = use_ctor
        self.simple_map = simple_map
        self.data_entity_dict = EasySQLDataEntityDict(data_access, table_name, id_column_name, add_lock)

    def update(self, id: any, entity: T):
        dict_record = EasyDataUtils.map_object_to_dict(entity)
        self.data_entity_dict.update(id, dict_record)

    def patch(self, id: any, entity: dict[str, any]):
        self.data_entity_dict.patch(id, entity)

    def insert(self, entity: T):
        dict_record = EasyDataUtils.map_object_to_dict(entity)
        self.data_entity_dict.insert(dict_record)

    def upsert(self, id: any, entity: T):
        dict_record = EasyDataUtils.map_object_to_dict(entity)
        self.data_entity_dict.upsert(id, dict_record)

    def delete(self, id: any):
        self.data_entity_dict.delete(id)

    def get_list(self) -> list[T]:
        dict_list = self.data_entity_dict.get_list()
        return self.map_list_dict_to_object(dict_list)

    def get_list_with_filters(self, filters: dict[str, any]) -> list[T]:
        dict_list = self.data_entity_dict.get_list_with_filters(filters)
        return self.map_list_dict_to_object(dict_list)

    def get(self, id: any) -> T:
        dict_record = self.data_entity_dict.get(id)
        return self.map_dict_to_object(dict_record)

    def get_with_filters(self, filters: dict[str, any]) -> T:
        dict_record = self.data_entity_dict.get_with_filters(filters)
        return self.map_dict_to_object(dict_record)

    def get_list_from_sql(self, sql: str, values: Tuple = None) -> list[T]:
        dict_list = self.data_entity_dict.get_list_from_sql(sql, values)
        return self.map_list_dict_to_object(dict_list)

    def map_dict_to_object(self, dict_record: dict[str, any]) -> T:
        if self.use_ctor:
            if self.simple_map:
                return EasyDataUtils.map_dict_to_object_ctor_simple(self.entity_type, dict_record)
            else:
                return EasyDataUtils.map_dict_to_object_from_params_ctor(self.entity_type, self.class_parameters,
                                                                         dict_record)
        else:
            return EasyDataUtils.map_dict_to_object(self.entity_type, dict_record)

    def map_list_dict_to_object(self, dict_list: list[dict[str, any]]) -> list[T]:
        if self.use_ctor:
            if self.simple_map:
                return EasyDataUtils.map_list_dict_to_object_ctor_simple(self.entity_type, dict_list)
            else:
                return EasyDataUtils.map_list_dict_to_object_from_params_ctor(self.entity_type, self.class_parameters,
                                                                              dict_list)
        else:
            return EasyDataUtils.map_list_dict_to_object(self.entity_type, dict_list)
