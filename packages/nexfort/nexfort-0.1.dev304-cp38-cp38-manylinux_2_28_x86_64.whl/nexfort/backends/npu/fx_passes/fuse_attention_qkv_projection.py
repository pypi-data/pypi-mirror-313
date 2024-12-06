
from typing import List
import torch
import torch_npu
from nexfort.utils.fx_passes import replace_pattern_with_filters
aten = torch.ops.aten

def fx_pass_fuse_attention_qkv_projection(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:
    for mm in [aten.matmul.default, aten.mm.default]:

        def pattern0(q: torch.Tensor, wq: torch.Tensor, kv: torch.Tensor, wk: torch.Tensor, wv: torch.Tensor, num_heads: int, scale_value: float, input_layout: str):
            query = mm(q, wq)
            key = mm(kv, wk)
            value = mm(kv, wv)
            out = torch_npu.npu_prompt_flash_attention(query, key, value, num_heads=num_heads, scale_value=scale_value, input_layout=input_layout)
            return out

        def replacement0(q: torch.Tensor, wq: torch.Tensor, kv: torch.Tensor, wk: torch.Tensor, wv: torch.Tensor, num_heads: int, scale_value: float, input_layout: str):
            (query, key, value) = torch_npu.npu_grouped_matmul([q, kv, kv], [wq, wk, wv])
            out = torch_npu.npu_prompt_flash_attention(query, key, value, num_heads=num_heads, scale_value=scale_value, input_layout=input_layout)
            return out
        gm = replace_pattern_with_filters(gm, pattern0, replacement0, match_filters=[], name='fuse_cross_attention_qkv_projection')

        def pattern1(qkv: torch.Tensor, wq: torch.Tensor, wk: torch.Tensor, wv: torch.Tensor, num_heads: int, scale_value: float, input_layout: str):
            query = mm(qkv, wq)
            key = mm(qkv, wk)
            value = mm(qkv, wv)
            out = torch_npu.npu_prompt_flash_attention(query, key, value, num_heads=num_heads, scale_value=scale_value, input_layout=input_layout)
            return out

        def replacement1(qkv: torch.Tensor, wq: torch.Tensor, wk: torch.Tensor, wv: torch.Tensor, num_heads: int, scale_value: float, input_layout: str):
            (query, key, value) = torch_npu.npu_grouped_matmul([qkv, qkv, qkv], [wq, wk, wv])
            out = torch_npu.npu_prompt_flash_attention(query, key, value, num_heads=num_heads, scale_value=scale_value, input_layout=input_layout)
            return out
        gm = replace_pattern_with_filters(gm, pattern1, replacement1, match_filters=[], name='fuse_self_attention_qkv_projection')
    return gm
