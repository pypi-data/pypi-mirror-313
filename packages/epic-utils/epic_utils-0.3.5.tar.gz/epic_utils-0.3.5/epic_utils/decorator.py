from .error import ErrorHandler
from time import perf_counter

class ClassProperty:
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, instance, owner):
        return self.fget(owner)
    
def MeasureTime(func):
    """
    Measures the time it takes for a function to execute
    """
    def wrapper(*args, **kwargs):
        start = perf_counter()
        func(*args, **kwargs)
        end = perf_counter()
        print(f"{func.__name__} took {(end-start)/1000} seconds")
    return wrapper

def ForceArgType(*types):
    """
    Forces a function to have a specific argument type, throws error if argument type is not correct
    @param: types: list of types
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            param_types = [type(arg) for arg in args]     
            for i in range(len(types)):
                if not ErrorHandler.isTypes(types[i], (list, tuple)):
                    t = types[i] if isinstance(types[i], str) else types[i].__name__
                    if param_types[i].__name__ != t:  
                        str_Types = ",".join(["|".join([i.__name__ if not isinstance(i, str) else i for i in t]) if ErrorHandler.isTypes(t, [list, tuple]) else t if isinstance(t, str) else t.__name__ for t in types ])
                        str_pTypes = ",".join([t.__name__ for t in param_types])  
                        ErrorHandler.raiseError(TypeError, f"<{str_Types}> expected, got <{str_pTypes}>")
                    continue
                if param_types[i].__name__ != types[i]:
                    t = [i.__name__ if not isinstance(i, str) else i for i in types[i]]
                    if not param_types[i].__name__ in t:
                        str_Types = ",".join(["|".join([i.__name__ if not isinstance(i, str) else i for i in t]) if ErrorHandler.isTypes(t, [list, tuple]) else t if isinstance(t, str) else t.__name__ for t in types ])
                        str_pTypes = ",".join([t.__name__ for t in param_types])  
                        ErrorHandler.raiseError(TypeError, f"<{str_Types}> expected, got <{str_pTypes}>")
            return func(*args, **kwargs)
        return wrapper
    return decorator

