import inspect
import logging


def debug(msg: str, *args, **kwargs) -> str:
    module_name = __get_logger_caller_module_name()
    logger = logging.getLogger(module_name)
    logger.debug(msg, *args, **kwargs)
    return module_name


def info(msg: str, *args, **kwargs) -> str:
    module_name = __get_logger_caller_module_name()
    logger = logging.getLogger(module_name)
    logger.info(msg, *args, **kwargs)
    return module_name


def warning(msg: str, *args, **kwargs) -> str:
    module_name = __get_logger_caller_module_name()
    logger = logging.getLogger(module_name)
    logger.warning(msg, *args, **kwargs)
    return module_name


warn = warning


def error(msg: str, *args, **kwargs) -> str:
    module_name = __get_logger_caller_module_name()
    logger = logging.getLogger(module_name)
    logger.error(msg, *args, **kwargs)
    return module_name


def critical(msg: str, *args, **kwargs) -> str:
    module_name = __get_logger_caller_module_name()
    logger = logging.getLogger(module_name)
    logger.critical(msg, *args, **kwargs)
    return module_name


fatal = critical


def exception(msg: str, *args, **kwargs) -> str:
    module_name = __get_logger_caller_module_name()
    logger = logging.getLogger(module_name)
    logger.exception(msg, *args, **kwargs)
    return module_name


# Must be directly invoked only by debug, info, etc. in this module
def __get_logger_caller_module_name() -> str:
    frames = inspect.stack()
    if len(frames) < 3:
        return ""  # cause degeneration to root logger

    # 0: this frame, 1: caller frame (logger), 2: caller's caller frame (logging function)
    caller_frame = frames[2]
    module = inspect.getmodule(caller_frame[0])
    if module is None:
        return ""
    return module.__name__
