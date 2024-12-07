from enum import Enum


class EasyPandaType(Enum):
    DATE = 'datetime64[ns]'
    STR = 'str'
    BOOL = 'bool'
    INT = 'int32'
    LONG = 'int64'
    FLOAT = 'float64'
    OBJECT = 'object'
