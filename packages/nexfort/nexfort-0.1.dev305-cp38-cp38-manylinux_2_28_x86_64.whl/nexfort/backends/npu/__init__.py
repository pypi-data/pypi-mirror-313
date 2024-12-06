
from typing import List
import torch
from .fx_passes import *

def apply_fx_passes(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:
    gm = fx_pass_fuse_attention(gm, example_inputs)
    gm = fx_pass_fuse_attention_qkv_projection(gm, example_inputs)
    gm = fx_pass_fuse_group_norm(gm, example_inputs)
    return gm
