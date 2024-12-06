import enum
import os
from typing import Union
import torch
import triton
import triton.language as tl
import nexfort_codegen_extension
from ..utils.env_var import parse_boolean_from_env
from .activations import _ActivationType2TorchMethod, _triton_activation_implementation, ActivationType
MAX_FP8_E4M3 = torch.finfo(torch.float8_e4m3fn).max
MIN_FP8_E4M3 = torch.finfo(torch.float8_e4m3fn).min
E5M2_MAX_POS = torch.finfo(torch.float8_e5m2).max
E5M2_MIN_POS = torch.finfo(torch.float8_e5m2).min
EPS = 1e-12
_TORCH_DTYPE_TO_TRITON_DTYPE = {torch.float64: tl.float64, torch.float: tl.float32, torch.float16: tl.float16, torch.float8_e4m3fn: tl.float8e4nv, torch.float8_e5m2: tl.float8e5, torch.int32: tl.int32, torch.int8: tl.int8}

class QuantType(enum.Enum):
    PER_TOKEN = 'per_token'
    PER_TENSOR = 'per_tensor'
    DIRECT_QUANT = 'direct_quant'
TRITON_GE_V3: tl.constexpr = triton.__version__ >= '3.0.0'

@triton.jit
def clamp_min_2_0(x, min_val):
    tl.static_assert(False, 'placeholder')

@triton.jit
def clamp_max_2_0(x, max_val):
    tl.static_assert(False, 'placeholder')

@triton.jit
def clamp_2_0(x, min_val, max_val):
    tl.static_assert(False, 'placeholder')
if TRITON_GE_V3:

    @triton.jit
    def clamp_min_3_0(x, min_val):
        tl.static_assert(False, 'placeholder')

    @triton.jit
    def clamp_max_3_0(x, max_val):
        tl.static_assert(False, 'placeholder')

    @triton.jit
    def clamp_3_0(x, min_val, max_val):
        tl.static_assert(False, 'placeholder')

@triton.jit
def _deprecated_per_tensor_quantize_kernel(x_ptr, max_ptr, y_ptr, scale_ptr, n_elements, q_min, q_max, eps, out_dtype: tl.constexpr, BLOCK_SIZE: tl.constexpr, TRITON_V3: tl.constexpr):
    tl.static_assert(False, 'placeholder')

def deprecated_per_tensor_quantize(x, quant_dtype, q_min, q_max, eps, act_method=ActivationType.IDENTITY):
    x = _ActivationType2TorchMethod[act_method](x)
    max_val = x.abs().amax()
    scale = torch.empty(1, dtype=torch.float32, device=x.device)
    y = torch.empty(x.size(), dtype=quant_dtype, device=x.device)
    N = x.shape[-1]
    n_elements = x.numel()
    BLOCK_SIZE = min(triton.next_power_of_2(N), 8192)
    grid = lambda meta: (triton.cdiv(n_elements, meta['BLOCK_SIZE']),)
    num_warps = 4 if BLOCK_SIZE < 2048 else 8 if BLOCK_SIZE < 4096 else 16
    _deprecated_per_tensor_quantize_kernel[grid](x, max_val, y, scale, n_elements, q_min, q_max, eps=eps, out_dtype=_TORCH_DTYPE_TO_TRITON_DTYPE[quant_dtype], BLOCK_SIZE=BLOCK_SIZE, TRITON_V3=TRITON_GE_V3, num_warps=num_warps)
    return (y, scale)

@triton.jit
def _per_tensor_quantize_kernel(x_ptr, max_ptr, y_ptr, scale_ptr, x_stride_b, x_stride_h, x_stride_r, x_stride_c, y_stride_b, y_stride_h, y_stride_r, y_stride_c, N, q_min, q_max, eps, out_dtype: tl.constexpr, BLOCK_SIZE: tl.constexpr, TRITON_V3: tl.constexpr):
    tl.static_assert(False, 'placeholder')

def per_tensor_quantize(x, quant_dtype, q_min, q_max, eps, act_method=ActivationType.IDENTITY):
    x = _ActivationType2TorchMethod[act_method](x)
    max_val = x.abs().amax()
    scale = torch.empty(1, dtype=torch.float32, device=x.device)
    out_shape = x.shape
    y = torch.empty(out_shape, device=x.device, dtype=quant_dtype)
    dims = x.dim()
    if dims == 4:
        (B, H, M, N) = x.shape
        stride_xb = x.stride(0)
        stride_yb = y.stride(0)
        stride_xh = x.stride(1)
        stride_yh = y.stride(1)
    elif dims == 3:
        (B, M, N) = x.shape
        H = 1
        stride_xb = x.stride(0)
        stride_yb = y.stride(0)
        stride_xh = 0
        stride_yh = 0
    elif dims == 2:
        B = 1
        H = 1
        (M, N) = x.shape
        stride_xb = 0
        stride_yb = 0
        stride_xh = 0
        stride_yh = 0
    else:
        raise NotImplementedError('Only support 2-D or 3-D tensor for now!')
    BLOCK_SIZE = triton.next_power_of_2(N)
    _per_tensor_quantize_kernel[M, H, B](x, max_val, y, scale, stride_xb, stride_xh, x.stride(-2), x.stride(-1), stride_yb, stride_yh, y.stride(-2), y.stride(-1), N, q_min, q_max, eps, out_dtype=_TORCH_DTYPE_TO_TRITON_DTYPE[quant_dtype], BLOCK_SIZE=BLOCK_SIZE, TRITON_V3=TRITON_GE_V3)
    return (y, scale)

@triton.jit
def _per_token_quantize_kernel(x_ptr, y_ptr, scale_ptr, x_stride_b, x_stride_h, x_stride_r, x_stride_c, y_stride_b, y_stride_h, y_stride_r, y_stride_c, scale_stride_b, scale_stride_h, scale_stride, N, q_min, q_max, eps, out_dtype: tl.constexpr, BLOCK_SIZE: tl.constexpr, ACTIVATION_METHOD: tl.constexpr, TRITON_V3: tl.constexpr):
    tl.static_assert(False, 'placeholder')

def per_token_quantize(x, quant_dtype, q_min, q_max, eps, act_method=ActivationType.IDENTITY):
    out_shape = x.shape
    scale_shape = x.shape[:-1] + (1,)
    y = torch.empty(out_shape, device=x.device, dtype=quant_dtype)
    scale = torch.empty(scale_shape, device=x.device, dtype=torch.float32)
    dims = x.dim()
    if dims == 4:
        (B, H, M, N) = x.shape
        stride_xb = x.stride(0)
        stride_yb = y.stride(0)
        stride_sb = scale.stride(0)
        stride_xh = x.stride(1)
        stride_yh = y.stride(1)
        stride_sh = scale.stride(1)
    elif dims == 3:
        (B, M, N) = x.shape
        H = 1
        stride_xb = x.stride(0)
        stride_yb = y.stride(0)
        stride_sb = scale.stride(0)
        stride_xh = 0
        stride_yh = 0
        stride_sh = 0
    elif dims == 2:
        B = 1
        H = 1
        (M, N) = x.shape
        stride_xb = 0
        stride_yb = 0
        stride_sb = 0
        stride_xh = 0
        stride_yh = 0
        stride_sh = 0
    else:
        raise NotImplementedError('Only support 2-D or 3-D tensor for now!')
    BLOCK_SIZE = triton.next_power_of_2(N)
    _per_token_quantize_kernel[M, H, B](x, y, scale, stride_xb, stride_xh, x.stride(-2), x.stride(-1), stride_yb, stride_yh, y.stride(-2), y.stride(-1), stride_sb, stride_sh, scale.stride(-2), N, q_min, q_max, eps, out_dtype=_TORCH_DTYPE_TO_TRITON_DTYPE[quant_dtype], BLOCK_SIZE=BLOCK_SIZE, ACTIVATION_METHOD=act_method, TRITON_V3=TRITON_GE_V3)
    return (y, scale)

def fp8_quantize(x: Union[torch.HalfTensor, torch.BFloat16Tensor], fp8_dtype: torch.dtype=torch.float8_e4m3fn, quant_type: QuantType=QuantType.PER_TENSOR):
    q_max = MAX_FP8_E4M3 if fp8_dtype == torch.float8_e4m3fn else E5M2_MAX_POS
    q_min = MIN_FP8_E4M3 if fp8_dtype == torch.float8_e4m3fn else E5M2_MIN_POS
    if quant_type == QuantType.PER_TENSOR:
        (fp8_x, fp8_scale) = per_tensor_quantize(x, fp8_dtype, q_min, q_max, EPS)
    elif quant_type == QuantType.PER_TOKEN:
        (fp8_x, fp8_scale) = per_token_quantize(x, fp8_dtype, q_min, q_max, EPS)
    elif quant_type == QuantType.DIRECT_QUANT:
        fp8_x = x.to(fp8_dtype)
        fp8_scale = None
    else:
        raise ValueError(f'quant_type={quant_type!r} is invaild value!')
    return (fp8_x, fp8_scale)

def act_and_fp8_quantize(x: Union[torch.HalfTensor, torch.BFloat16Tensor], fp8_dtype: torch.dtype=torch.float8_e4m3fn, quant_type: QuantType=QuantType.PER_TENSOR, act_method: ActivationType=ActivationType.IDENTITY):
    q_max = MAX_FP8_E4M3 if fp8_dtype == torch.float8_e4m3fn else E5M2_MAX_POS
    q_min = MIN_FP8_E4M3 if fp8_dtype == torch.float8_e4m3fn else E5M2_MIN_POS
    if quant_type == QuantType.PER_TENSOR:
        (fp8_x, fp8_scale) = per_tensor_quantize(x, fp8_dtype, q_min, q_max, EPS, act_method=act_method)
    elif quant_type == QuantType.PER_TOKEN:
        (fp8_x, fp8_scale) = per_token_quantize(x, fp8_dtype, q_min, q_max, EPS, act_method=act_method)
    elif quant_type == QuantType.DIRECT_QUANT:
        fp8_x = _ActivationType2TorchMethod[act_method](x).to(fp8_dtype)
        fp8_scale = None
    else:
        raise ValueError(f'quant_type={quant_type!r} is invaild value!')
    return (fp8_x, fp8_scale)

def acc_type(dtype, allow_low_precision=True):
    if dtype == torch.float16:
        if allow_low_precision and torch.backends.cuda.matmul.allow_fp16_reduced_precision_reduction and (torch.version.hip is None):
            return tl.float16
        else:
            return tl.float32
    elif dtype == torch.bfloat16:
        return tl.float32
    elif dtype == torch.float8_e4m3fn or dtype == torch.float8_e5m2:
        return tl.float32
    elif dtype == torch.int8:
        return tl.int32
    else:
        return getattr(tl, f'{dtype}'.replace('torch.', ''))

def enabled_triton_autotune_cache():
    return parse_boolean_from_env('NEXFORT_ENABLE_TRITON_AUTOTUNE_CACHE', default_value=True)

def force_torch_flash_attention():
    return parse_boolean_from_env('NEXFORT_FORCE_TORCH_FLASH_ATTENTION', default_value=False)

def enabled_fp8_quantize_attention():
    return parse_boolean_from_env('NEXFORT_ENABLE_FP8_QUANTIZE_ATTENTION', default_value=True)

def enabled_fuse_attention_fp16_reduction():
    return parse_boolean_from_env('NEXFORT_ENABLE_FUSE_ATTENTION_FP16_REDUCTION', default_value=True)

def enabled_matmul_fp16_reduction():
    return parse_boolean_from_env('NEXFORT_ENABLE_MATMUL_FP16_REDUCTION', default_value=True)

def fp8_quantize_attention_type():
    quant_type = os.getenv('NEXFORT_ATTENTION_FP8_QUANTIZE_TYPE', default='direct_quant')
    assert quant_type in ('per_token', 'per_tensor', 'direct_quant'), f'Valid values of NEXFORT_ATTENTION_FP8_QUANTIZE_TYPE are [per_token, per_tensor, direct_quant], but got {quant_type}'
    return QuantType(quant_type)

def force_torch_scaled_mm():
    return parse_boolean_from_env('NEXFORT_FORCE_TORCH_SCALED_MM', default_value=False)

def matmul_allow_tf32():
    return parse_boolean_from_env('NEXFORT_FX_MATMUL_ALLOW_TF32', default_value=False)