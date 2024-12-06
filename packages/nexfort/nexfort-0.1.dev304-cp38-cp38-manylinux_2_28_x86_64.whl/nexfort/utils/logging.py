
import functools
import logging
_LOG_LEVELS = {'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARNING, 'error': logging.ERROR, 'critical': logging.CRITICAL}
_VLOG_LEVELS = [(logging.INFO - i) for i in range(1, 3)]

class VerboseLogger(logging.getLoggerClass()):

    def __init__(self, name):
        super().__init__(name)
        for (i, level) in enumerate(_VLOG_LEVELS):
            setattr(self, f'vinfo{(i + 1)}', (lambda msg, lvl=level, *args, **kwargs: self.log(lvl, msg, *args, **kwargs)))

class LoggerFactory():

    @staticmethod
    def create_logger(name=None, level=logging.INFO):
        'create a logger\n\n        Args:\n            name (str): name of the logger\n            level: level of logger\n\n        Raises:\n            ValueError is name is None\n        '
        if (name is None):
            raise ValueError('name for logger cannot be None')
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d:%(funcName)s] %(message)s')
        logging.setLoggerClass(VerboseLogger)
        logger_ = logging.getLogger(name)
        logger_.setLevel(level)
        logger_.propagate = False
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger_.addHandler(ch)
        return logger_
logger = LoggerFactory.create_logger(name='nexfort', level=logging.INFO)

@functools.lru_cache(None)
def warning_once(*args, **kwargs):
    "\n    This method is identical to `logger.warning()`, but will emit the warning with the same message only once\n\n    Note: The cache is for the function arguments, so 2 different callers using the same arguments will hit the cache.\n    The assumption here is that all warning messages are unique across the code. If they aren't then need to switch to\n    another type of cache that includes the caller frame information in the hashing function.\n    "
    logger.warning(*args, **kwargs)
logger.warning_once = warning_once

def print_configuration(args, name):
    logger.info('{}:'.format(name))
    for arg in sorted(vars(args)):
        dots = ('.' * (29 - len(arg)))
        logger.info('  {} {} {}'.format(arg, dots, getattr(args, arg)))

def get_current_level():
    "\n    Return logger's current log level\n    "
    return logger.getEffectiveLevel()

def should_log_le(max_log_level_str):
    '\n    Args:\n        max_log_level_str: maximum log level as a string\n\n    Returns ``True`` if the current log_level is less or equal to the specified log level. Otherwise ``False``.\n\n    Example:\n\n        ``should_log_le("info")`` will return ``True`` if the current log level is either ``logging.INFO`` or ``logging.DEBUG``\n    '
    if (not isinstance(max_log_level_str, str)):
        raise ValueError(f'{max_log_level_str} is not a string')
    max_log_level_str = max_log_level_str.lower()
    if (max_log_level_str not in _LOG_LEVELS):
        raise ValueError(f'{max_log_level_str} is not one of the `logging` levels')
    return (get_current_level() <= _LOG_LEVELS[max_log_level_str])
