from enum import IntEnum


class DescribedIntEnum(IntEnum):
    def __new__(cls, value, msg):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.msg = msg
        return obj
