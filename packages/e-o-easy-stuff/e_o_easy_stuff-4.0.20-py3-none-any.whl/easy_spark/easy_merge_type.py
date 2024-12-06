from enum import Enum


class EasyMergeType(Enum):
    UPDATE_AND_INSERT = "UpdateAndInsert"
    INSERT_ONLY = "InsertOnly"
    UPDATE_ONLY = "UpdateOnly"
