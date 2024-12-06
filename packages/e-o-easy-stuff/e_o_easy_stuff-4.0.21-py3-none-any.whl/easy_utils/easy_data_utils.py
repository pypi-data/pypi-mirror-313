import inspect


class EasyDataUtils:
    def __init__(self):
        pass

    @staticmethod
    def name_to_pascal_case(name: str) -> str:
        return (name[0].upper() + name[1:]).strip()

    @staticmethod
    def name_to_pascal_case_between_dots(name: str) -> str:
        return '.'.join([EasyDataUtils.name_to_pascal_case(x) for x in name.split('.')])

    @staticmethod
    def names_to_pascal_case_from_dict(record: dict) -> dict:
        return {EasyDataUtils.name_to_pascal_case_between_dots(key): value for key, value in record.items()}

    @staticmethod
    def flatten_record(record: dict):
        out = {}

        def flatten(x, name=''):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + '.')
            else:
                out[name[:-1]] = x

        flatten(record)

        return

    @staticmethod
    def map_dict_to_object_ctor_simple(cls, record: dict[str, any]):
        return cls(**record)

    @staticmethod
    def map_list_dict_to_object_ctor_simple(cls, records: list[dict[str, any]]):
        return [EasyDataUtils.map_dict_to_object_ctor_simple(cls, record) for record in records]

    @staticmethod
    def map_dict_to_object_ctor(cls, record: dict[str, any]):
        params = inspect.signature(cls.__init__).parameters
        return EasyDataUtils.map_dict_to_object_from_params_ctor(cls, params, record)

    @staticmethod
    def map_dict_to_object_from_params_ctor(cls, params, record: dict[str, any]):
        filtered_data = {key: record[key] for key in params if key in record and key != 'self'}
        return cls(**filtered_data)

    @staticmethod
    def map_object_to_dict(obj: any) -> dict[str, any]:
        return {key: getattr(obj, key) for key in obj.__dict__}

    @staticmethod
    def map_list_dict_to_object_ctor(cls, records: list[dict[str, any]]):
        return [EasyDataUtils.map_dict_to_object_ctor(cls, record) for record in records]

    @staticmethod
    def map_list_dict_to_object_from_params_ctor(cls, params, records: list[dict[str, any]]):
        return [EasyDataUtils.map_dict_to_object_from_params_ctor(cls, params, record) for record in records]

    @staticmethod
    def map_dict_to_object(cls, record: dict[str, any]):
        obj = cls()
        for key, value in record.items():
            setattr(obj, key, value)
        return obj

    @staticmethod
    def map_list_dict_to_object(cls, records: list[dict[str, any]]):
        return [EasyDataUtils.map_dict_to_object(cls, record) for record in records]
