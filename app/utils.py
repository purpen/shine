# -*- coding: utf-8 -*-
import enum

class DBEnum(enum.Enum):
    @classmethod
    def get_enum_labels(cls):
        return [i.value for i in cls]


def is_sequence(arg):
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))