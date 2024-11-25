from enum import Enum
from collections import namedtuple


class MyEnum(Enum):
    """My enumeration"""
    CODE = 42
    NAME = "alex"
    

User = namedtuple("User", ["code", "name"])
User.__doc__ = """User namedtuple"""
User.code.__doc__ = """The code field"""
User.name.__doc__ = """The name field"""
