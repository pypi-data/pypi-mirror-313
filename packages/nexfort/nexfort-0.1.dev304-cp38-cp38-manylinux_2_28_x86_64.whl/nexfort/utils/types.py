
import torch

def is_type(dtype, t):
    return (getattr(torch, t, None) == dtype)

def is_fp8_type(dtype):
    return (dtype.is_floating_point and (dtype.itemsize == 1))

def is_8bit_type(dtype):
    return (dtype.itemsize == 1)
