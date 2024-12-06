import logging
import traceback
from functools import wraps

logger = logging.getLogger('error')


def handle_errors(func: callable):
    """Decorator that catches any exceptions raised by the decorated function and logs them.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The decorated function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            function_name = func.__name__ if hasattr(
                func, '__name__') else 'Unknown callable object'
            logger.error(f'{function_name}: {e}')
            logger.info(traceback.format_exc())
        finally:
            return result
    return wrapper


def handle_none_return(default_type: str):
    """Decorator that replaces `None` return values with default values depending on the desired type.

    Args:
        default_type (str): The desired default value type. Must be one of 'dict', 'list', 'float', or 'int'.

    Returns:
        callable: The decorator function.
    """
    if default_type == 'dict':
        default_value = {}
    elif default_type == 'list':
        default_value = []
    elif default_type in ('int', 'float'):
        default_value = 0
    else:
        default_value = None

    def decorator(func: callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if result is None:
                result = default_value
            return result
        return wrapper
    return decorator
