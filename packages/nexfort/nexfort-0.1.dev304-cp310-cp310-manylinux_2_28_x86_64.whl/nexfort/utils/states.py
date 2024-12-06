import os
import torch
import nexfort

def set_env_var(name, value):
    if value is None:
        if name in os.environ:
            del os.environ[name]
    else:
        if isinstance(value, bool):
            value = '1' if value else '0'
        else:
            value = str(value)
        os.environ[name] = value

def has_env_var(name):
    return name in os.environ

def get_env_var(name, default=None):
    return os.environ.get(name, default)

def get_env_int(name, default=None):
    val = os.environ.get(name, None)
    if val is None:
        return default
    return int(val)

def get_env_bool(name, default=None):
    val = os.environ.get(name, None)
    if val is None:
        return default
    if val == '1':
        return True
    return False

def remove_env_var(name):
    if name in os.environ:
        del os.environ[name]

def stash_obj_in_tls(key, arg):
    torch._C._stash_obj_in_tls(key, arg)

def set_obj_in_tls(key, arg):
    nexfort._C.set_obj_in_tls(key, arg)

def has_tls_obj(key):
    return nexfort._C.is_obj_in_tls(key)

def get_obj_in_tls(key, *args, accept_none=False):

    def inner():
        return nexfort._C.get_obj_in_tls(key)
    assert len(args) <= 1
    if args:
        obj = inner() if has_tls_obj(key) else args[0]
    else:
        obj = inner()
    if obj is None:
        if accept_none:
            return None
        if args:
            return args[0]
        raise ValueError(f'TLS object {key} is None')
    return obj

def remove_obj_in_tls(key):
    nexfort._C.remove_obj_in_tls(key)