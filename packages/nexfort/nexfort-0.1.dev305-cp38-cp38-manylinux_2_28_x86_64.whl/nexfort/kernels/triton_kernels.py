
import triton
import triton.language as tl
import nexfort_codegen_extension
from .activations import _triton_activation_implementation
from .cached_autotuner import cached_autotune, cached_heuristics
from .utils import matmul_allow_tf32

@triton.jit
def _triton_layer_norm_fwd(Y, X, W, B, R_old, R_new, y_stride_r, y_stride_c, x_stride_r, x_stride_c, r_stride_r, r_stride_c, new_r_stride_r, new_r_stride_c, N, eps, HAS_WEIGHT: tl.constexpr, HAS_BIAS: tl.constexpr, HAS_RESIDUAL: tl.constexpr, RETURN_RESIDUAL: tl.constexpr, BLOCK_SIZE: tl.constexpr):
    tl.static_assert(False, 'placeholder')

@triton.jit
def _triton_rms_norm_fwd(Y, X, W, B, R_old, R_new, y_stride_r, y_stride_c, x_stride_r, x_stride_c, r_stride_r, r_stride_c, new_r_stride_r, new_r_stride_c, N, eps, HAS_WEIGHT: tl.constexpr, HAS_BIAS: tl.constexpr, HAS_RESIDUAL: tl.constexpr, RETURN_RESIDUAL: tl.constexpr, BLOCK_SIZE: tl.constexpr):
    tl.static_assert(False, 'placeholder')

@triton.jit
def _triton_rms_norm_4d_kernel(Y, X, W, B, z, h, m, k, y_stride_z, y_stride_h, y_stride_m, y_stride_k, x_stride_z, x_stride_h, x_stride_m, x_stride_k, eps, HAS_WEIGHT: tl.constexpr, HAS_BIAS: tl.constexpr, BLOCK_SIZE: tl.constexpr):
    tl.static_assert(False, 'placeholder')

@triton.jit
def _fuse_layer_norm_broadcast_add_mul_residual_kernel(Y, X, W, B, A, R, shift, y_stride_r, y_stride_c, x_stride_r, x_stride_c, N, eps, HAS_WEIGHT: tl.constexpr, HAS_BIAS: tl.constexpr, BLOCK_SIZE: tl.constexpr):
    tl.static_assert(False, 'placeholder')

@triton.jit
def _apply_rope_kernel(xq_ptr, xk_ptr, freqs_cis_ptr, xq_out_ptr, xk_out_ptr, B, M, N, stride_qa, stride_qb, stride_qc, stride_qd, stride_qe, stride_qf, stride_ka, stride_kb, stride_kc, stride_kd, stride_ke, stride_kf, stride_fa, stride_fb, stride_fc, stride_fd, stride_fe, stride_ff, BLOCK_SIZE: tl.constexpr):
    tl.static_assert(False, 'placeholder')

@triton.jit
def _apply_rotary_emb(xq_ptr, xk_ptr, cos_ptr, sin_ptr, xq_out_ptr, xk_out_ptr, B, M, N, stride_qa, stride_qb, stride_qc, stride_qd, stride_qe, stride_ka, stride_kb, stride_kc, stride_kd, stride_ke, stride_ca, stride_cb, stride_cc, stride_cd, stride_ce, stride_sa, stride_sb, stride_sc, stride_sd, stride_se, BLOCK_SIZE: tl.constexpr):
    tl.static_assert(False, 'placeholder')

@cached_autotune(configs=[triton.Config({'BLOCK_M': 128, 'BLOCK_N': 256, 'BLOCK_K': 32, 'GROUP_SIZE_M': 8}, num_stages=3, num_warps=8), triton.Config({'BLOCK_M': 256, 'BLOCK_N': 128, 'BLOCK_K': 32, 'GROUP_SIZE_M': 8}, num_stages=3, num_warps=8), triton.Config({'BLOCK_M': 256, 'BLOCK_N': 64, 'BLOCK_K': 32, 'GROUP_SIZE_M': 8}, num_stages=3, num_warps=8), triton.Config({'BLOCK_M': 128, 'BLOCK_N': 256, 'BLOCK_K': 64, 'GROUP_SIZE_M': 8}, num_stages=3, num_warps=8), triton.Config({'BLOCK_M': 64, 'BLOCK_N': 256, 'BLOCK_K': 32, 'GROUP_SIZE_M': 8}, num_stages=4, num_warps=4), triton.Config({'BLOCK_M': 128, 'BLOCK_N': 128, 'BLOCK_K': 32, 'GROUP_SIZE_M': 8}, num_stages=4, num_warps=4), triton.Config({'BLOCK_M': 128, 'BLOCK_N': 64, 'BLOCK_K': 32, 'GROUP_SIZE_M': 8}, num_stages=4, num_warps=4), triton.Config({'BLOCK_M': 64, 'BLOCK_N': 128, 'BLOCK_K': 32, 'GROUP_SIZE_M': 8}, num_stages=4, num_warps=4), triton.Config({'BLOCK_M': 128, 'BLOCK_N': 32, 'BLOCK_K': 32, 'GROUP_SIZE_M': 8}, num_stages=4, num_warps=4), triton.Config({'BLOCK_M': 64, 'BLOCK_N': 32, 'BLOCK_K': 32, 'GROUP_SIZE_M': 8}, num_stages=5, num_warps=2), triton.Config({'BLOCK_M': 32, 'BLOCK_N': 64, 'BLOCK_K': 32, 'GROUP_SIZE_M': 8}, num_stages=5, num_warps=2)], key=['M_for_tune', 'N', 'K'])
@cached_heuristics({'EVEN_K': (lambda args: ((args['K'] % args['BLOCK_K']) == 0)), 'ALLOW_TF32': (lambda args: matmul_allow_tf32())})
@triton.jit
def _fuse_linear_mul_residual_kernel(X, W, B, L, S, R, Y, M_for_tune, M, N, K, stride_sn, stride_am, stride_ak, stride_bk, stride_bn, stride_lm, stride_ln, stride_rm, stride_rn, stride_cm, stride_cn, HAS_BIAS: tl.constexpr, BLOCK_M: tl.constexpr, BLOCK_N: tl.constexpr, BLOCK_K: tl.constexpr, GROUP_SIZE_M: tl.constexpr, EVEN_K: tl.constexpr, ACC_TYPE: tl.constexpr, ALLOW_TF32: tl.constexpr):
    tl.static_assert(False, 'placeholder')

@cached_autotune(configs=[triton.Config({'BLOCK_M': 128, 'BLOCK_N': 256, 'BLOCK_K': 128, 'GROUP_SIZE_M': 8}, num_stages=3, num_warps=8), triton.Config({'BLOCK_M': 256, 'BLOCK_N': 128, 'BLOCK_K': 128, 'GROUP_SIZE_M': 8}, num_stages=3, num_warps=8), triton.Config({'BLOCK_M': 256, 'BLOCK_N': 64, 'BLOCK_K': 128, 'GROUP_SIZE_M': 8}, num_stages=4, num_warps=4), triton.Config({'BLOCK_M': 64, 'BLOCK_N': 256, 'BLOCK_K': 128, 'GROUP_SIZE_M': 8}, num_stages=4, num_warps=4), triton.Config({'BLOCK_M': 128, 'BLOCK_N': 128, 'BLOCK_K': 128, 'GROUP_SIZE_M': 8}, num_stages=4, num_warps=4), triton.Config({'BLOCK_M': 128, 'BLOCK_N': 64, 'BLOCK_K': 64, 'GROUP_SIZE_M': 8}, num_stages=4, num_warps=4), triton.Config({'BLOCK_M': 64, 'BLOCK_N': 128, 'BLOCK_K': 64, 'GROUP_SIZE_M': 8}, num_stages=4, num_warps=4), triton.Config({'BLOCK_M': 128, 'BLOCK_N': 32, 'BLOCK_K': 64, 'GROUP_SIZE_M': 8}, num_stages=4, num_warps=4), triton.Config({'BLOCK_M': 64, 'BLOCK_N': 32, 'BLOCK_K': 64, 'GROUP_SIZE_M': 8}, num_stages=5, num_warps=2)], key=['M_for_tune', 'N', 'K'])
@cached_heuristics({'EVEN_K': (lambda args: ((args['K'] % args['BLOCK_K']) == 0)), 'ALLOW_TF32': (lambda args: matmul_allow_tf32())})
@triton.jit
def _fuse_quant_fp8_linear_mul_residual_kernel(X, X_S, W, W_S, B, L, S, R, Y, M_for_tune, M, N, K, stride_xsb, stride_sb, stride_sn, stride_ab, stride_am, stride_ak, stride_bk, stride_bn, stride_lb, stride_lm, stride_ln, stride_rb, stride_rm, stride_rn, stride_cb, stride_cm, stride_cn, HAS_BIAS: tl.constexpr, BLOCK_M: tl.constexpr, BLOCK_N: tl.constexpr, BLOCK_K: tl.constexpr, GROUP_SIZE_M: tl.constexpr, EVEN_K: tl.constexpr, ACT_PER_TENSOR: tl.constexpr, WEIGHT_PER_TENSOR: tl.constexpr, ALLOW_TF32: tl.constexpr):
    tl.static_assert(False, 'placeholder')

@cached_autotune(configs=[triton.Config({'BLOCK_M': 128, 'BLOCK_N': 256, 'BLOCK_K': 32, 'GROUP_SIZE_M': 8}, num_stages=3, num_warps=8), triton.Config({'BLOCK_M': 256, 'BLOCK_N': 128, 'BLOCK_K': 32, 'GROUP_SIZE_M': 8}, num_stages=3, num_warps=8), triton.Config({'BLOCK_M': 256, 'BLOCK_N': 64, 'BLOCK_K': 32, 'GROUP_SIZE_M': 8}, num_stages=3, num_warps=8), triton.Config({'BLOCK_M': 128, 'BLOCK_N': 256, 'BLOCK_K': 64, 'GROUP_SIZE_M': 8}, num_stages=3, num_warps=8), triton.Config({'BLOCK_M': 64, 'BLOCK_N': 256, 'BLOCK_K': 32, 'GROUP_SIZE_M': 8}, num_stages=4, num_warps=4), triton.Config({'BLOCK_M': 128, 'BLOCK_N': 128, 'BLOCK_K': 32, 'GROUP_SIZE_M': 8}, num_stages=4, num_warps=4), triton.Config({'BLOCK_M': 128, 'BLOCK_N': 64, 'BLOCK_K': 32, 'GROUP_SIZE_M': 8}, num_stages=4, num_warps=4), triton.Config({'BLOCK_M': 64, 'BLOCK_N': 128, 'BLOCK_K': 32, 'GROUP_SIZE_M': 8}, num_stages=4, num_warps=4), triton.Config({'BLOCK_M': 128, 'BLOCK_N': 32, 'BLOCK_K': 32, 'GROUP_SIZE_M': 8}, num_stages=4, num_warps=4), triton.Config({'BLOCK_M': 64, 'BLOCK_N': 32, 'BLOCK_K': 32, 'GROUP_SIZE_M': 8}, num_stages=5, num_warps=2), triton.Config({'BLOCK_M': 32, 'BLOCK_N': 64, 'BLOCK_K': 32, 'GROUP_SIZE_M': 8}, num_stages=5, num_warps=2)], key=['M_for_tune', 'N', 'K'])
@cached_heuristics({'EVEN_K': (lambda args: ((args['K'] % args['BLOCK_K']) == 0)), 'ALLOW_TF32': (lambda args: matmul_allow_tf32())})
@triton.jit
def _act_and_matmul_and_act_kernel(X, W, B, L, Y, M_for_tune, M, N, K, stride_am, stride_ak, stride_bk, stride_bn, stride_lm, stride_ln, stride_cm, stride_cn, HAS_BIAS: tl.constexpr, BLOCK_M: tl.constexpr, BLOCK_N: tl.constexpr, BLOCK_K: tl.constexpr, GROUP_SIZE_M: tl.constexpr, EVEN_K: tl.constexpr, PRE_ACTIVATION_METHOD: tl.constexpr, POST_ACTIVATION_METHOD: tl.constexpr, ACC_TYPE: tl.constexpr, ALLOW_TF32: tl.constexpr):
    tl.static_assert(False, 'placeholder')

@cached_autotune(configs=[triton.Config({'BLOCK_M': 128, 'BLOCK_N': 256, 'BLOCK_K': 128, 'GROUP_SIZE_M': 8}, num_stages=3, num_warps=8), triton.Config({'BLOCK_M': 256, 'BLOCK_N': 128, 'BLOCK_K': 128, 'GROUP_SIZE_M': 8}, num_stages=3, num_warps=8), triton.Config({'BLOCK_M': 256, 'BLOCK_N': 64, 'BLOCK_K': 128, 'GROUP_SIZE_M': 8}, num_stages=4, num_warps=4), triton.Config({'BLOCK_M': 64, 'BLOCK_N': 256, 'BLOCK_K': 128, 'GROUP_SIZE_M': 8}, num_stages=4, num_warps=4), triton.Config({'BLOCK_M': 128, 'BLOCK_N': 128, 'BLOCK_K': 128, 'GROUP_SIZE_M': 8}, num_stages=4, num_warps=4), triton.Config({'BLOCK_M': 128, 'BLOCK_N': 64, 'BLOCK_K': 64, 'GROUP_SIZE_M': 8}, num_stages=4, num_warps=4), triton.Config({'BLOCK_M': 64, 'BLOCK_N': 128, 'BLOCK_K': 64, 'GROUP_SIZE_M': 8}, num_stages=4, num_warps=4), triton.Config({'BLOCK_M': 128, 'BLOCK_N': 32, 'BLOCK_K': 64, 'GROUP_SIZE_M': 8}, num_stages=4, num_warps=4), triton.Config({'BLOCK_M': 64, 'BLOCK_N': 32, 'BLOCK_K': 64, 'GROUP_SIZE_M': 8}, num_stages=5, num_warps=2)], key=['M_for_tune', 'N', 'K'])
@cached_heuristics({'EVEN_K': (lambda args: ((args['K'] % args['BLOCK_K']) == 0)), 'ALLOW_TF32': (lambda args: matmul_allow_tf32())})
@triton.jit
def _quant_fp8_act_and_matmul_and_act_kernel(X, X_S, W, W_S, B, L, Y, M_for_tune, M, N, K, stride_xsb, stride_ab, stride_am, stride_ak, stride_bk, stride_bn, stride_lb, stride_lm, stride_ln, stride_cb, stride_cm, stride_cn, HAS_BIAS: tl.constexpr, BLOCK_M: tl.constexpr, BLOCK_N: tl.constexpr, BLOCK_K: tl.constexpr, GROUP_SIZE_M: tl.constexpr, EVEN_K: tl.constexpr, PRE_ACTIVATION_METHOD: tl.constexpr, POST_ACTIVATION_METHOD: tl.constexpr, ACT_PER_TENSOR: tl.constexpr, WEIGHT_PER_TENSOR: tl.constexpr, ALLOW_TF32: tl.constexpr):
    tl.static_assert(False, 'placeholder')

@triton.jit
def _fuse_mul_bias_scale_residual(x_ptr, x_s_ptr, w_s_ptr, b_ptr, s_ptr, r_ptr, y_ptr, N, stride_sn, stride_xm, stride_xn, stride_rm, stride_rn, stride_ym, stride_yn, HAS_BIAS: tl.constexpr, ACT_PER_TENSOR: tl.constexpr, WEIGHT_PER_TENSOR: tl.constexpr, BLOCK_SIZE: tl.constexpr, ACTIVATION_METHOD: tl.constexpr):
    tl.static_assert(False, 'placeholder')

@triton.jit
def _fuse_mul_bias_scale_residual_2d_or_3d(x_ptr, x_s_ptr, w_s_ptr, b_ptr, s_ptr, r_ptr, y_ptr, N, stride_xsb, stride_sb, stride_sn, stride_xb, stride_xm, stride_xn, stride_rb, stride_rm, stride_rn, stride_yb, stride_ym, stride_yn, HAS_BIAS: tl.constexpr, ACT_PER_TENSOR: tl.constexpr, WEIGHT_PER_TENSOR: tl.constexpr, BLOCK_SIZE: tl.constexpr, ACTIVATION_METHOD: tl.constexpr):
    tl.static_assert(False, 'placeholder')

@triton.jit
def _fuse_mul_bias_add_scale_residual(x_ptr, x_s_ptr, w_s_ptr, b_ptr, a_ptr, s_ptr, r_ptr, y_ptr, N, stride_sn, stride_xm, stride_xn, stride_am, stride_an, stride_rm, stride_rn, stride_ym, stride_yn, HAS_BIAS: tl.constexpr, ACT_PER_TENSOR: tl.constexpr, WEIGHT_PER_TENSOR: tl.constexpr, BLOCK_SIZE: tl.constexpr, ACTIVATION_METHOD: tl.constexpr):
    tl.static_assert(False, 'placeholder')

@triton.jit
def _fuse_mul_bias_add_scale_residual_2d_or_3d(x_ptr, x_s_ptr, w_s_ptr, b_ptr, a_ptr, s_ptr, r_ptr, y_ptr, N, stride_xsb, stride_sb, stride_sn, stride_xb, stride_xm, stride_xn, stride_ab, stride_am, stride_an, stride_rb, stride_rm, stride_rn, stride_yb, stride_ym, stride_yn, HAS_BIAS: tl.constexpr, ACT_PER_TENSOR: tl.constexpr, WEIGHT_PER_TENSOR: tl.constexpr, BLOCK_SIZE: tl.constexpr, ACTIVATION_METHOD: tl.constexpr):
    tl.static_assert(False, 'placeholder')
