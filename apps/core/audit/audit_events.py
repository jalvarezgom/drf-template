from enum import IntEnum, unique, StrEnum


class DescribedIntEnum(IntEnum):
    def __new__(cls, value, msg):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.msg = msg
        return obj


class AuditActions:
    class Categories(StrEnum):
        User = "USER"

    class Events:
        @unique
        class User(DescribedIntEnum):
            # 100 - 199
            SIGNUP = 100, "{0.actor} has signed up"
            LOGIN = 101, "{0.actor} has logged in successfully"
            FAILED_LOGIN = 102, "{0.actor} has failed to log in from IP {ip}"
