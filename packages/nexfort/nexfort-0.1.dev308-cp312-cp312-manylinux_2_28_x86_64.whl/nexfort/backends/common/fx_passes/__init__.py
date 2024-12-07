import functools
from typing import List
import torch
from nexfort.fx_compiler import config as fx_config
from nexfort.utils.fx_passes import clean_up_graph_after_modifications, get_node_arg, match_call_function_input_has_users, replace_pattern_with_filters, skip_pass_if_has_no_call_function
from nexfort.utils.logging import logger
from nexfort.utils.memory_format import suggest_memory_format
from .freezing import fx_pass_freeze
from .functionalize import fx_pass_functionalize
aten = torch.ops.aten

def apply_fx_passes(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:
    common_config = fx_config.common
    if common_config.disable:
        logger.debug('Skipping all common passes because it is disabled')
        return gm
    if common_config.freezing and (fx_config.jit.disable or not fx_config.jit.freezing):
        gm = fx_pass_freeze(gm, example_inputs)
    elif common_config.cse:
        from torch.fx.passes.dialect.common.cse_pass import CSEPass, get_CSE_banned_ops
        banned_ops = get_CSE_banned_ops()
        P_default = CSEPass(banned_ops=banned_ops)
        gm = P_default(gm).graph_module
    if common_config.functionalize:
        gm = fx_pass_functionalize(gm, example_inputs)
    if common_config.remove_dropout and (not torch.is_grad_enabled()):
        gm = fx_pass_remove_dropout(gm, example_inputs)
    if common_config.remove_contiguous:
        gm = fx_pass_remove_contiguous(gm, example_inputs)
    if common_config.remove_clone_preserve_format:
        gm = fx_pass_remove_clone_preserve_format(gm, example_inputs)
    if common_config.transform_view_to_reshape:
        gm = fx_pass_transform_view_to_reshape(gm, example_inputs)
    if common_config.remove_simple_arith:
        gm = fx_pass_remove_simple_arith(gm, example_inputs)
    if common_config.lower_conv:
        gm = fx_pass_lower_conv(gm, example_inputs)
    if common_config.optimize_gelu:
        gm = fx_pass_optimize_gelu(gm, example_inputs)
    return gm

@skip_pass_if_has_no_call_function([aten.dropout.default])
def fx_pass_remove_dropout(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:
    to_erase = []
    for node in gm.graph.nodes:
        if node.op == 'call_function' and node.target == aten.dropout.default:
            node.replace_all_uses_with(node.args[0])
            to_erase.append(node)
    for node in to_erase:
        gm.graph.erase_node(node)
    logger.debug(f'Removed {len(to_erase)} dropout ops')
    if to_erase:
        gm = clean_up_graph_after_modifications(gm)
    return gm

@skip_pass_if_has_no_call_function([aten.contiguous.default])
def fx_pass_remove_contiguous(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:
    to_erase = []
    for node in gm.graph.nodes:
        if node.op == 'call_function' and node.target == aten.contiguous.default:
            node.replace_all_uses_with(node.args[0])
            to_erase.append(node)
    for node in to_erase:
        gm.graph.erase_node(node)
    logger.debug(f'Removed {len(to_erase)} contiguous ops')
    if to_erase:
        gm = clean_up_graph_after_modifications(gm)
    return gm

@skip_pass_if_has_no_call_function([aten.clone.default])
def fx_pass_remove_clone_preserve_format(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:
    target = aten.clone.default

    def pattern_1(x: torch.Tensor, memory_format: torch.memory_format):
        return target(x, memory_format=memory_format)

    def replacement_1(x: torch.Tensor, memory_format: torch.memory_format):
        return x

    def pattern_2(x: torch.Tensor):
        return target(x)

    def replacement_2(x: torch.Tensor):
        return x

    def is_preserve_memory_format(match, original_graph: torch.fx.Graph, pattern_graph: torch.fx.Graph) -> bool:
        for node in match.nodes_map.values():
            if node.op == 'call_function' and node.target == target:
                if 'memory_format' not in node.kwargs or node.kwargs['memory_format'] == torch.preserve_format:
                    return True
                val = node.args[0].meta.get('val')
                return val is not None and suggest_memory_format(val) == node.kwargs['memory_format']
        return False
    gm = replace_pattern_with_filters(gm, pattern_1, replacement_1, match_filters=[is_preserve_memory_format, functools.partial(match_call_function_input_has_users, target=target, users=1)], name='remove_clone_preserve_format_1')
    gm = replace_pattern_with_filters(gm, pattern_2, replacement_2, match_filters=[is_preserve_memory_format, functools.partial(match_call_function_input_has_users, target=target, users=1)], name='remove_clone_preserve_format_2')
    return gm

@skip_pass_if_has_no_call_function([[aten.view.default], [aten._unsafe_view.default]])
def fx_pass_transform_view_to_reshape(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:

    def pattern_view(x: torch.Tensor, shape: List[int]):
        return aten.view.default(x, shape)

    def pattern__unsafe_view(x: torch.Tensor, shape: List[int]):
        return aten._unsafe_view.default(x, shape)

    def replacement(x: torch.Tensor, shape: List[int]):
        return aten.reshape.default(x, shape)
    gm = replace_pattern_with_filters(gm, pattern_view, replacement, match_filters=[functools.partial(match_call_function_input_has_users, target=aten.view.default, users=1)], name='transform_view_to_reshape')
    gm = replace_pattern_with_filters(gm, pattern__unsafe_view, replacement, match_filters=[functools.partial(match_call_function_input_has_users, target=aten._unsafe_view.default, users=1)], name='transform__unsafe_view_to_reshape')
    return gm

def fx_pass_remove_simple_arith(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:
    to_erase = []
    for node in gm.graph.nodes:
        if node.op == 'call_function':
            if len(node.args) != 2:
                continue
            if node.target in (aten.add.Tensor, aten.sub.Tensor):
                if isinstance(node.args[0], (int, float)) and node.args[0] == 0 and (len(node.args[1].users) == 1):
                    node.replace_all_uses_with(node.args[1])
                    to_erase.append(node)
                elif isinstance(node.args[1], (int, float)) and node.args[1] == 0 and (len(node.args[0].users) == 1):
                    node.replace_all_uses_with(node.args[0])
                    to_erase.append(node)
            elif node.target == aten.mul.Tensor:
                if isinstance(node.args[0], (int, float)) and node.args[0] == 1 and (len(node.args[1].users) == 1):
                    node.replace_all_uses_with(node.args[1])
                    to_erase.append(node)
                elif isinstance(node.args[1], (int, float)) and node.args[1] == 1 and (len(node.args[0].users) == 1):
                    node.replace_all_uses_with(node.args[0])
                    to_erase.append(node)
            elif node.target == aten.div.Tensor:
                if isinstance(node.args[1], (int, float)) and node.args[1] == 1 and (len(node.args[0].users) == 1):
                    node.replace_all_uses_with(node.args[0])
                    to_erase.append(node)
    for node in to_erase:
        gm.graph.erase_node(node)
    logger.debug(f'Removed {len(to_erase)} simple arithmetic ops')
    if to_erase:
        gm = clean_up_graph_after_modifications(gm)
    return gm

@skip_pass_if_has_no_call_function([[aten.conv1d.default], [aten.conv2d.default], [aten.conv3d.default]])
def fx_pass_lower_conv(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:
    count = 0
    for node in gm.graph.nodes:
        if node.op == 'call_function' and node.target in (aten.conv1d.default, aten.conv2d.default, aten.conv3d.default):
            input = get_node_arg(node, 0, 'input')
            weight = get_node_arg(node, 1, 'weight')
            bias = get_node_arg(node, 2, 'bias')
            stride = get_node_arg(node, 3, 'stride', 1)
            padding = get_node_arg(node, 4, 'padding', 0)
            dilation = get_node_arg(node, 5, 'dilation', 1)
            groups = get_node_arg(node, 6, 'groups', 1)
            repeats = {aten.conv1d.default: 1, aten.conv2d.default: 2, aten.conv3d.default: 3}[node.target]

            def repeat(x):
                if isinstance(x, (list, tuple)):
                    return x
                return [x] * repeats
            stride = repeat(stride)
            padding = repeat(padding)
            dilation = repeat(dilation)
            node.target = aten.convolution.default
            node.args = (input, weight, bias, stride, padding, dilation, False, repeat(0), groups)
            node.kwargs = {}
            count += 1
    logger.debug(f'Lowered {count} call_function convs to convolution')
    if count > 0:
        gm = clean_up_graph_after_modifications(gm)
    return gm

def fx_pass_optimize_gelu(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:
    count = 0
    for node in gm.graph.nodes:
        if node.op == 'call_function' and node.target == aten.gelu.default:
            if 'approximate' not in node.kwargs:
                node.kwargs = {'approximate': 'tanh', **node.kwargs}
                count += 1
    logger.debug(f"Optimized {count} call_function gelu with approximate='tanh'")
    if count > 0:
        gm = clean_up_graph_after_modifications(gm)
    return gm