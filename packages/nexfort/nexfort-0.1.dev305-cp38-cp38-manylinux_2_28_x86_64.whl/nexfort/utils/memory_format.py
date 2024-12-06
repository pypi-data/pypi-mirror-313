
from typing import Sequence
import torch
TensorLikeType = torch.Tensor

def are_strides_like_channels_last(shape: Sequence[int], strides: Sequence[int]) -> bool:
    ndim = len(shape)
    if (ndim == 4):
        dim_order = [1, 3, 2, 0]
    elif (ndim == 5):
        dim_order = [1, 4, 3, 2, 0]
    else:
        return False
    if (strides[1] == 0):
        return False
    min = 0
    for d in dim_order:
        if (shape[d] == 0):
            return False
        if (strides[d] < min):
            return False
        if ((d == 0) and (min == strides[1])):
            return False
        min = strides[d]
        if (strides[d] > 1):
            min *= shape[d]
    return True

def suggest_memory_format(x: TensorLikeType) -> torch.memory_format:
    if (x.layout != torch.strided):
        return torch.contiguous_format
    if are_strides_like_channels_last(x.shape, x.stride()):
        return (torch.channels_last if (x.ndim == 4) else torch.channels_last_3d)
    return torch.contiguous_format

def apply_memory_format(obj, memory_format=torch.preserve_format):

    def convert(t):
        dim = t.ndim
        if (memory_format == torch.channels_last):
            if (dim == 4):
                return t.to(memory_format=torch.channels_last)
            else:
                return t
        elif (memory_format == torch.channels_last_3d):
            return t
        else:
            return t.to(memory_format=memory_format)
    if isinstance(obj, torch.Tensor):
        return convert(obj)
    elif isinstance(obj, torch.nn.Module):
        return obj._apply(convert)
    else:
        return obj
