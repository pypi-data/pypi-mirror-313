
from nexfort.utils.logging import logger

def recursive_getattr(obj, attr, default=None):
    attrs = attr.split('.')
    for attr in attrs:
        if (not hasattr(obj, attr)):
            return default
        obj = getattr(obj, attr, default)
    return obj

def recursive_setattr(obj, attr, value):
    attrs = attr.split('.')
    for attr in attrs[:(- 1)]:
        obj = getattr(obj, attr)
    setattr(obj, attrs[(- 1)], value)

def recursive_apply(obj, attr, fn, *, verbose=False):
    value = recursive_getattr(obj, attr, None)
    if (value is not None):
        logger.info(f'Applying {fn} to {attr}')
        recursive_setattr(obj, attr, fn(value))

def multi_recursive_apply(obj, attrs, fn, *, ignores=(), verbose=False):
    ignores = set(ignores)
    for attr in attrs:
        if (attr in ignores):
            continue
        recursive_apply(obj, attr, fn, verbose=verbose)
