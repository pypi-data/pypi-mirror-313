
import importlib.util
import os
import sys
import torch
from .utils.env_var import parse_boolean_from_env
if parse_boolean_from_env('NEXFORT_FORCE_CHECK_TORCH_VERSION', default_value=True):
    from .check_compiled_env_meta import check_torch_version
    check_torch_version()
if parse_boolean_from_env('NEXFORT_FORCE_CHECK_TRITON_VERSION', default_value=True):
    from .check_compiled_env_meta import check_triton_version
    check_triton_version()
from nexfort.utils.env_var import parse_integer_from_env
for (extension, notice) in [['_C', None], ['_C_inductor', None], ['_C_cuda', 'Or is it compatible with your CUDA Toolkit installation?'], ['_C_cutlass', 'Or is it compatible with your CUDA Toolkit installation?']]:
    if (importlib.util.find_spec(f'nexfort.{extension}') is None):
        exec(f'{extension} = None')
        continue
    try:
        exec(f'import nexfort.{extension} as {extension}')
    except ImportError:
        print('Unable to load nexfort.{extension} module. Is it compatible with your PyTorch installation?', file=sys.stderr)
        if (notice is not None):
            print(notice, file=sys.stderr)
        raise
try:
    from ._version import version as __version__, version_tuple
except ImportError:
    __version__ = 'unknown version'
    version_tuple = (0, 0, 'unknown version')
_nexfort_debug_level = parse_integer_from_env('NEXFORT_DEBUG', 0)
if (_nexfort_debug_level >= 1):
    from nexfort.utils.logging import logger
    if (_nexfort_debug_level >= 3):
        logger.setLevel('DEBUG')
    else:
        import logging
        logger.setLevel((logging.INFO - _nexfort_debug_level))
