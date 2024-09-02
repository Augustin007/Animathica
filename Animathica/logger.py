import logging
import functools
from collections import deque
from typing import Callable, Any

# Initialize a stack to keep track of nested function calls
_call_stack :deque = deque()

log_flags: dict[str,int] = {}

max_stack_size = 30

def log(level: int, msg: str) -> None:
    '''Logs a message at a specific logging level with the call stack included.'''
    if len(_call_stack) > max_stack_size:
        raise RecursionError('Recursion limit exceeded')
    stack_msg = ' -> '.join(_call_stack)
    full_msg = f' STACK[{stack_msg}]: {msg}' if stack_msg else msg
    logging.log(level, full_msg)

def log_function(level: int):
    '''Decorator for logging function calls at a specific logging level.'''
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            func_name = func.__name__
            log_at = log_flags.get(func_name, level)
            if hasattr(func, 'log_name'):
                func_name = func.log_name
            _call_stack.append(func_name)
            try:
                if args:
                    if kwargs:
                        log(log_at, f'{func_name} called with args {args!r} and kwargs {kwargs!r}')
                    else:
                        log(log_at, f'{func_name} called with args {args!r}')
                elif kwargs:
                    log(log_at, f'{func_name} called with kwargs {kwargs!r}')
                else:
                    log(log_at, f'{func_name} called')
            except RecursionError:
                log(logging.WARN, f'Entering {func_name}, failed to log arguments')
            try:
                result = func(*args, **kwargs)
                if result is None:
                    log(log_at, f'Exiting {func_name}')
                else:
                    try:
                        log(log_at, f'Exiting {func_name} with value {result!r}')
                    except RecursionError:
                        log(logging.WARN, 'Exiting {func_name}. Failed to log result')
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
            if attr_name.startswith('__') and attr_name.endswith('__'):
                continue
            if isinstance(attr_value, type):
                continue
            if callable(attr_value):
                try:
                    attr_value.log_name = cls.__name__ + '.' + attr_name
                except AttributeError:
                    log(logging.DEBUG, f'Func {attr_name} not logged')
                decorated_attr = log_function(level)(attr_value)
                setattr(cls, attr_name, decorated_attr)
        return cls
    return decorator

