"""This module docstring describes the module. This module exposes fields, functions, and classes. Fields are variables and constants. A class has members: class fields, properties, and methods. This docstring is deliberately long enough for testing the ellipsis function."""
from my_project.package1.module1 import NAME, CODE, my_func1, my_func2, my_generator, MyClass1, MyClass2
from my_project.package2.module2 import MyEnum, User

__all__ = ["NAME", "CODE", "my_func1", "my_func2", "my_generator", "MyClass1", "MyClass2", "MyEnum", "User"]


def ignored_func(a, b, c):
    """
    Description
    
    [param]
    - a: A
    - b: B
    - c: C
    
    [return]
    A number
    """
    return
