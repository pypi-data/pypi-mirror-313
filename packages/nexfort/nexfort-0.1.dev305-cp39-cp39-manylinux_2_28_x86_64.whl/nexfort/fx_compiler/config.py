import os
import sys
from nexfort.utils import checks

def optional_bool_from_env(name, default=None):
    val = os.environ.get(name, None)
    if val is None:
        return default
    if val == '1':
        return True
    return False
graph_cache = os.environ.get('NEXFORT_GRAPH_CACHE', '0') == '1'
ignore_warnings = os.environ.get('NEXFORT_FX_IGNORE_WARNINGS', '1') == '1'
dump_graph = os.environ.get('NEXFORT_FX_DUMP_GRAPH') == '1'
cudagraphs = os.environ.get('NEXFORT_FX_CUDAGRAPHS') == '1'
disable_custom_passes = os.environ.get('NEXFORT_FX_DISABLE_CUSTOM_PASSES') == '1'
pre_dispatch = os.environ.get('NEXFORT_FX_PRE_DISPATCH', '1') == '1'
yield_to_mixed_mm = os.environ.get('NEXFORT_FX_YIELD_TO_MIXED_MM') == '1'
gemm_use_fast_accum = os.environ.get('NEXFORT_GEMM_USE_FAST_ACCUM') == '1'

class overrides:
    conv_benchmark = optional_bool_from_env('NEXFORT_FX_CONV_BENCHMARK')
    conv_allow_tf32 = optional_bool_from_env('NEXFORT_FX_CONV_ALLOW_TF32')
    matmul_allow_tf32 = optional_bool_from_env('NEXFORT_FX_MATMUL_ALLOW_TF32')
    matmul_allow_fp16_reduction = optional_bool_from_env('NEXFORT_FX_MATMUL_ALLOW_FP16_REDUCTION')
    matmul_allow_bf16_reduction = optional_bool_from_env('NEXFORT_FX_MATMUL_ALLOW_BF16_REDUCTION')

class pre_aot:
    disable = True

class common:
    disable = False
    freezing = False
    cse = True
    functionalize = False
    remove_dropout = False
    lower_conv = False
    remove_contiguous = True
    remove_clone_preserve_format = True
    transform_view_to_reshape = True
    remove_simple_arith = True
    optimize_gelu = True

class post:
    disable = False
    hotfix_native_group_norm = True

def init_inductor_options():
    options = {'aggressive_fusion': True, 'epilogue_fusion_first': True, 'triton.unique_kernel_names': os.environ.get('TORCHINDUCTOR_UNIQUE_KERNEL_NAMES', '1') == '1'}
    if checks.is_inductor_supported():
        from torch._inductor import config as inductor_config
        if hasattr(inductor_config, 'always_keep_tensor_constants'):
            options['always_keep_tensor_constants'] = True
    return options

class inductor:
    disable = not checks.is_inductor_supported()
    mode = None
    options = init_inductor_options()
    dynamic = None
    unquantized_linear_use_triton_template = False
    fp8_linear_use_triton_template = False
    max_autotune_cublaslt_algos = 2
    max_autotune_cublaslt_int8_gemm = True
    transform_linear_out_dtype_to_linear_epilogue = True
    remove_clone_contiguous_format = True
    optimize_geglu = True
    optimize_attention = True
    optimize_linear_epilogue = False
    optimize_scaled_linear = True
    enable_cudnn_sdpa = os.environ.get('NEXFORT_FX_ENABLE_CUDNN_SDPA', '1') == '1'
    force_cudnn_sdpa = os.environ.get('NEXFORT_FX_FORCE_CUDNN_SDPA') == '1'
    force_triton_sdpa = os.environ.get('NEXFORT_FX_FORCE_TRITON_SDPA') == '1'

class cuda:
    disable = False
    fuse_qkv_projections = True
    optimize_conv = True
    optimize_lowp_gemm = True
    optimize_scaled_gemm = True
    fuse_timestep_embedding = os.environ.get('NEXFORT_FUSE_TIMESTEP_EMBEDDING', '1') == '1'

class jit:
    disable = True
    check_trace = False
    strict = False
    freezing = False
    optimize_for_inference = False
    disable_optimized_execution = os.environ.get('NEXFORT_FX_JIT_DISABLE_OPTIMIZED_EXECUTION') == '1'

class triton:
    enable_fast_math = True
    fuse_attention_allow_fp16_reduction = True
    max_num_imprecise_acc = None
_save_config_ignore = {}
try:
    from torch.utils._config_module import install_config_module
except ImportError:
    from torch._dynamo.config_utils import install_config_module
install_config_module(sys.modules[__name__])