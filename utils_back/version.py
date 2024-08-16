import warnings  
from functools import wraps  
def deprecated(func):  
    """This is a decorator to mark functions as deprecated."""  
    @wraps(func)  
    def wrapped_function(*args, **kwargs):  
        warnings.warn(  
            f"{func.__name__} is deprecated and may be removed in future versions.",  
            category=DeprecationWarning,  
            stacklevel=2  
        )  
        return func(*args, **kwargs)  
    
    return wrapped_function 