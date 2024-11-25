"""Module 1"""

NAME = "alex"
CODE = 42


def my_func1(arg, name="alex", code=42):
    return


def my_func2(arg, code=420, name="alexr"):
    """
    This is an unnamed section. It represents the description 
    for the function. It is deliberately long enough for testing
    the ellipsis function
    
    [param]
    Introducing parameters
    - arg: Argument
    - code: Integer
    - name: String
    
    [return]
    An integer
    
    [except]
    Introducing exceptions
    - Exception: An exception
    """
    return
    

def my_generator(arg, code=42, name="alex"):
    """
    Multiline 
    description
    
    [param]
    - arg: Argument
    - code: Integer
    - name: String
    
    [yield]
    Integers
    
    [except]
    - Exception: An exception
    """
    yield


class MyClass1:
    
    def __init__(self, arg, name="alex", code=42):
        """
        Multiline 
        description
        
        [param]
        - arg: Argument
        - name: String
        - code: Integer
        
        [except]
        Introducing exceptions
        - Exception: An exception
        """
        return
        
    def method(self):
        return
        
    @staticmethod
    def static_method(a, b, c):
        """
        Multiline
        description
        
        [param]
        - a: A
        - b: B
        - c: C
        
        [return]
        An integer
        """
        return
        
    @classmethod
    def class_method(cls, a, b):
        """
        Multiline
        description
        
        [param]
        - a: A
        - b: B
        
        [return]
        An integer
        """
        return
        

class MyClass2(MyClass1):
    """Docstring for the class"""
    
    def method(self):
        """New docstring"""
        return
        
    def new_method(self):
        pass
