
import math
from typing import List
import torch
import torch_npu
from nexfort.utils.fx_passes import replace_pattern_with_filters
from ..soc_version import get_soc_version, SocVersion
aten = torch.ops.aten

def fx_pass_fuse_attention(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:

    def pattern(query: torch.Tensor, key: torch.Tensor, value: torch.Tensor, shape_0: List[int], shape_1: List[int], shape_2: List[int], shape: List[int]):
        reshape_query = aten.reshape.default(query, shape_0)
        transpose_query = aten.transpose.int(reshape_query, 1, 2)
        reshape_key = aten.reshape.default(key, shape_1)
        transpose_key = aten.transpose.int(reshape_key, 1, 2)
        reshape_value = aten.reshape.default(value, shape_2)
        transpose_value = aten.transpose.int(reshape_value, 1, 2)
        out = aten.scaled_dot_product_attention.default(transpose_query, transpose_key, transpose_value)
        transpose_out = aten.transpose.int(out, 1, 2)
        reshape_out = aten.reshape.default(transpose_out, shape)
        return reshape_out

    def replacement(query: torch.Tensor, key: torch.Tensor, value: torch.Tensor, shape_0: List[int], shape_1: List[int], shape_2: List[int], shape: List[int]):
        return torch_npu.npu_prompt_flash_attention(query, key, value, num_heads=shape_0[(- 2)], scale_value=(1 / math.sqrt(shape_0[(- 1)])), input_layout='BSH')

    def filter(match, original_graph: torch.fx.Graph, pattern_graph: torch.fx.Graph):
        shape_0 = match.placeholder_nodes[3]
        if ((get_soc_version() > SocVersion.Ascend910B1) and (shape_0[(- 1)] <= 256)):
            return True
        return False
    gm = replace_pattern_with_filters(gm, pattern, replacement, match_filters=[filter], name='fuse_attention')
    return gm
