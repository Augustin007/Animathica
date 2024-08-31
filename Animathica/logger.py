import logging
import functools
from collections import deque
from typing import Callable, Any

# Initialize a stack to keep track of nested function calls
_call_stack = deque()

def log(level: int, msg: str) -> None:
    '''Logs a message at a specific logging level with the call stack included.'''
    stack_msg = ' -> '.join(_call_stack)
    full_msg = f' STACK[{stack_msg}]: {msg}' if stack_msg else msg
    logging.log(level, full_msg)

def log_function(level: int):
    '''Decorator for logging function calls at a specific logging level.'''
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            func_name = func.__name__
            _call_stack.append(func_name)
            try:
                log(level, f'Entering {func_name}')
                log(level, f'{func_name} called with args {args!r} and kwargs {kwargs!r}')
            except:
                log(logging.WARN, 'Failed to log')
            try:
                result = func(*args, **kwargs)
                try:
                    log(level, f'Exiting {func_name}')
                    log(level, f'Exiting {func_name} with value {result!r}')
                except:
                    log(logging.WARN, 'Failed to log')
                return result
            finally:
                _call_stack.pop()

        return wrapper
    return decorator

def log_skip(func):
    func.skip = True
    return func

def log_class(level: int):
    '''Decorator for logging all method calls in a class at a specific logging level.'''
    def decorator(cls):
        for attr_name, attr_value in cls.__dict__.items():
            if hasattr(attr_value, 'skip'):
                if attr_value.skip:
                    continue
            if attr_name in ('__str__', '__repr__'):
                continue
            if isinstance(attr_value, type):
                continue
            if callable(attr_value):
                decorated_attr = log_function(level)(attr_value)
                setattr(cls, attr_name, decorated_attr)
        return cls
    return decorator

