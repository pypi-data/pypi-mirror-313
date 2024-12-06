from typing import List
import torch
from nexfort.fx_compiler import config as fx_config
from nexfort.utils.fx_passes import clean_up_graph_after_modifications, skip_pass_if_has_no_call_function
from nexfort.utils.logging import logger
from nexfort.utils.memory_format import suggest_memory_format
aten = torch.ops.aten

def apply_fx_passes(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:
    post_config = fx_config.post
    if post_config.disable:
        logger.debug('Skipping all post passes because it is disabled')
        return gm
    if post_config.hotfix_native_group_norm and fx_config.inductor.disable:
        gm = fx_pass_hotfix_group_norm(gm, example_inputs)
    return gm

@skip_pass_if_has_no_call_function(aten.native_group_norm.default)
def fx_pass_hotfix_group_norm(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:
    count = 0
    target = aten.native_group_norm.default
    for node in gm.graph.nodes:
        if node.op == 'call_function' and node.target == target:
            input = node.args[0]
            val = input.meta.get('val')
            if val is None:
                memory_format = torch.contiguous_format
            else:
                memory_format = suggest_memory_format(val) if val.device.type == 'cpu' else torch.contiguous_format
                if val.is_contiguous(memory_format=memory_format):
                    continue
            with gm.graph.inserting_before(node):
                conti: torch.fx.Node = gm.graph.call_function(the_function=aten.contiguous.default, args=(input,), kwargs={'memory_format': memory_format})
                (_, *ngm_args) = node.args
                node.args = (conti, *ngm_args)
            count += 1
    logger.debug(f'Hotfix native_group_norm: {count} nodes are fixed')
    if count > 0:
        gm = clean_up_graph_after_modifications(gm)
    return gm