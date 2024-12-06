
import triton
import triton.language as tl
import nexfort_codegen_extension
from .cached_autotuner import cached_autotune, cached_heuristics
configs = [triton.Config({'BLOCK_M': BM, 'BLOCK_N': BN}, num_stages=s, num_warps=w) for BM in [64, 128] for BN in [32, 64, 128] for w in [2, 4, 8] for s in [1, 2, 3, 4]]

def keep(conf):
    BLOCK_M = conf.kwargs['BLOCK_M']
    BLOCK_N = conf.kwargs['BLOCK_N']
    if (((BLOCK_M * BLOCK_N) < (128 * 128)) and (conf.num_warps == 8)):
        return False
    return True

@triton.jit
def _attn_fwd_inner(acc, l_i, m_i, q, K_block_ptr, V_block_ptr, start_m, qk_scale, stride_kn, stride_kk, stride_vk, stride_vn, BLOCK_M: tl.constexpr, HEAD_DIM: tl.constexpr, BLOCK_N: tl.constexpr, STAGE: tl.constexpr, offs_m: tl.constexpr, offs_n: tl.constexpr, SEQLEN_K: tl.constexpr, ACC_TYPE: tl.constexpr, QK_ACC_TYPE: tl.constexpr, EVEN_K: tl.constexpr):
    tl.static_assert(False, 'placeholder')

@cached_autotune(list(filter(keep, configs)), key=['N_CTX_for_tune', 'HEAD_DIM'])
@cached_heuristics({'EVEN_K': (lambda args: ((args['SEQLEN_K'] % args['BLOCK_N']) == 0))})
@triton.jit
def _fuse_attn_kernel(Q, K, V, sm_scale, Out, stride_qz, stride_qh, stride_qm, stride_qk, stride_kz, stride_kh, stride_kn, stride_kk, stride_vz, stride_vh, stride_vk, stride_vn, stride_oz, stride_oh, stride_om, stride_on, Z, H, N_CTX_for_tune, N_CTX, SEQLEN_K, HEAD_DIM: tl.constexpr, BLOCK_M: tl.constexpr, BLOCK_N: tl.constexpr, STAGE: tl.constexpr, ACC_TYPE: tl.constexpr, QK_ACC_TYPE: tl.constexpr, EVEN_K: tl.constexpr):
    tl.static_assert(False, 'placeholder')

@cached_autotune(list(filter(keep, configs)), key=['N_CTX_for_tune', 'HEAD_DIM'])
@cached_heuristics({'EVEN_K': (lambda args: ((args['SEQLEN_K'] % args['BLOCK_N']) == 0))})
@triton.jit
def _per_tensor_fp8_quant_fuse_attn_kernel(Q, K, V, q_scale, k_scale, sm_scale, Out, stride_qz, stride_qh, stride_qm, stride_qk, stride_kz, stride_kh, stride_kn, stride_kk, stride_vz, stride_vh, stride_vk, stride_vn, stride_oz, stride_oh, stride_om, stride_on, Z, H, N_CTX_for_tune, N_CTX, SEQLEN_K, HEAD_DIM: tl.constexpr, BLOCK_M: tl.constexpr, BLOCK_N: tl.constexpr, STAGE: tl.constexpr, ACC_TYPE: tl.constexpr, QK_ACC_TYPE: tl.constexpr, EVEN_K: tl.constexpr):
    tl.static_assert(False, 'placeholder')

@triton.jit
def _per_token_quant_attn_fwd_inner(acc, l_i, m_i, q, K_block_ptr, V_block_ptr, K_scale_block_ptr, q_scale, stride_kn, stride_kk, stride_vk, stride_vn, start_m, sm_scale, BLOCK_M: tl.constexpr, HEAD_DIM: tl.constexpr, BLOCK_N: tl.constexpr, STAGE: tl.constexpr, offs_m: tl.constexpr, offs_n: tl.constexpr, SEQLEN_K: tl.constexpr, ACC_TYPE: tl.constexpr, QK_ACC_TYPE: tl.constexpr, EVEN_K: tl.constexpr):
    tl.static_assert(False, 'placeholder')

@cached_autotune(list(filter(keep, configs)), key=['N_CTX_for_tune', 'HEAD_DIM'])
@cached_heuristics({'EVEN_K': (lambda args: ((args['SEQLEN_K'] % args['BLOCK_N']) == 0))})
@triton.jit
def _per_token_fp8_quant_fuse_attn_kernel(Q, K, V, Q_scale, K_scale, sm_scale, Out, stride_qz, stride_qh, stride_qm, stride_qk, stride_kz, stride_kh, stride_kn, stride_kk, stride_vz, stride_vh, stride_vk, stride_vn, stride_oz, stride_oh, stride_om, stride_on, stride_q_scalez, stride_q_scaleh, stride_q_scalem, stride_k_scalez, stride_k_scaleh, stride_k_scalem, Z, H, N_CTX_for_tune, N_CTX, SEQLEN_K, HEAD_DIM: tl.constexpr, BLOCK_M: tl.constexpr, BLOCK_N: tl.constexpr, STAGE: tl.constexpr, ACC_TYPE: tl.constexpr, QK_ACC_TYPE: tl.constexpr, EVEN_K: tl.constexpr):
    tl.static_assert(False, 'placeholder')
