import sys
import torch
from packaging import version

def torch_version_compare(op, v):
    return getattr(version.parse(torch.__version__).release, f'__{op}__')(version.parse(v).release)

def is_inductor_supported():
    try:
        from torch._dynamo import is_inductor_supported
    except ImportError:
        from torch._dynamo import is_dynamo_supported
        return is_dynamo_supported() and sys.platform != 'win32'
    else:
        return is_inductor_supported()

def has_triton():
    try:
        from torch.utils._triton import has_triton
    except ImportError:
        from torch._inductor.utils import has_triton
    return has_triton()

def triton_version_compare(op, v):
    if not has_triton():
        return None
    import triton
    return getattr(version.parse(triton.__version__).release, f'__{op}__')(version.parse(v).release)

def is_nvidia_cuda():
    return torch.version.hip is None and torch.cuda.is_available()

def cuda_capability_compare(op, major, minor, *, device=None):
    if not is_nvidia_cuda():
        return None
    return getattr(torch.cuda.get_device_capability(device), f'__{op}__')((major, minor))

def torch_cuda_version():
    if torch.version.cuda is None:
        return (0, 0)
    cuda_version = str(torch.version.cuda)
    return tuple((int(x) for x in cuda_version.split('.')))[:2]

def torch_cuda_version_compare(op, major, minor):
    return getattr(torch_cuda_version(), f'__{op}__')((major, minor))