import logging.handlers
import os, logging, json
from typing import TypeVar, Generic
from functools import wraps
from .config import config

T= TypeVar('T')

#region logging
class logger_path_filter(logging.Filter):
    def filter(self, record):
        record.pathname = record.pathname.replace(os.getcwd(),"")
        return True
def logger_instance(name: str) -> logging.Logger:
    logging.basicConfig(
        format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(pathname)s:%(funcName)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d:%H:%M:%S',
        level=logging.INFO)
    logger = logging.getLogger(name)
    logger.addFilter(logger_path_filter())
    return logger
_log: logging.Logger = locals().get("_loc", logger_instance(__name__))
#endregion

#region cache
class cache(Generic[T]):
    def _filepath() -> str:
        return os.path.join('.data',f'{T.__module__}.{T.__name__}.json')
    @staticmethod
    def get() -> list[T]:
        filepath: str = cache._filepath()
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                content = file.read()
            items: list[T] = json.loads(content)
            return items
        return None
    @staticmethod
    def set(items: list[T]):
        with open(cache._filepath(), 'w') as file:
            file.write(json.dumps(items))
    @staticmethod
    def clear():
        os.remove(cache._filepath())
#endregion

def _get_timer_wrapper(is_async=False):
    import time, sys
    def log_execution(start_time, func, args):
        end = time.time()
        _log.info("'%s -> %s' exec in %s sec\n%s\n---\n",
                  sys._getframe(2).f_code.co_qualname,
                  func.__name__,
                  end - start_time,
                  str(args[:1])[:100])
    if not config.runtime_options().debug:
        return lambda f: f
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = time.time()
            result = await func(*args, **kwargs)
            log_execution(start, func, args)
            return result
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            log_execution(start, func, args)
            return result
        return async_wrapper if is_async else sync_wrapper
    return decorator

def timer(func):
    return _get_timer_wrapper(is_async=False)(func)
def atimer(func):
    return _get_timer_wrapper(is_async=True)(func)






