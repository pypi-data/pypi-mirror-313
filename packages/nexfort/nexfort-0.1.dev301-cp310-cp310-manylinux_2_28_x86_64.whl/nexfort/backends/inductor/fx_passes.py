import functools
from typing import List, Optional
import torch
from nexfort.fx_compiler import config as fx_config
from nexfort.utils import type_utils, types
from nexfort.utils.checks import has_triton
from nexfort.utils.fx_passes import clean_up_graph_after_modifications, get_node_arg, match_call_function_input_has_users, replace_pattern_with_filters, run_shape_prop, skip_pass_if_has_no_call_function, skip_pass_if_unavailable
from nexfort.utils.logging import logger
aten = torch.ops.aten
nexfort_inductor = torch.ops.nexfort_inductor
nexfort_cuda = torch.ops.nexfort_cuda

def apply_fx_passes(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:
    inductor_config = fx_config.inductor
    if inductor_config.disable:
        logger.debug('Skipping all inductor passes because it is disabled')
        return gm
    if not has_triton():
        logger.warning('Triton is not available, skipping all inductor passes')
        return gm
    from torch._inductor import config as inductor_config_
    from nexfort.inductor.utils import use_triton_template
    use_triton_template_ = use_triton_template()
    if inductor_config.transform_linear_out_dtype_to_linear_epilogue:
        gm = fx_pass_transform_linear_out_dtype_to_linear_epilogue(gm, example_inputs)
    if inductor_config.remove_clone_contiguous_format:
        gm = fx_pass_remove_clone_contiguous_format(gm, example_inputs)
    if inductor_config.optimize_geglu and use_triton_template_:
        gm = fx_pass_optimize_geglu_by_linear(gm, example_inputs)
    if inductor_config.optimize_linear_epilogue:
        gm = fx_pass_optimize_lineaer_epilogue(gm, example_inputs)
    if inductor_config.optimize_scaled_linear and (not inductor_config_.cpp_wrapper):
        gm = fx_pass_optimize_scaled_linear(gm, example_inputs)
    return gm

def broadcastable(fr, to):
    try:
        fr.expand_as(to)
    except RuntimeError:
        return False
    return True

@skip_pass_if_unavailable('nexfort_inductor', 'linear_out_dtype')
@skip_pass_if_unavailable('nexfort_inductor', 'linear_epilogue')
def fx_pass_transform_linear_out_dtype_to_linear_epilogue(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:
    target = nexfort_inductor.linear_out_dtype.default
    count = 0
    for node in gm.graph.nodes:
        if not (node.op == 'call_function' and node.target == target):
            continue
        input = get_node_arg(node, 0, 'input')
        weight = get_node_arg(node, 1, 'weight')
        bias = get_node_arg(node, 2, 'bias')
        out_dtype = get_node_arg(node, 3, 'out_dtype')
        epilogue_ops = []
        epilogue_tensor_args = []
        epilogue_scalar_args = []
        if out_dtype is not None:
            epilogue_ops.append('to_dtype')
            epilogue_tensor_args.append(None)
            epilogue_scalar_args.append(int(type_utils.JitScalarType.from_dtype(out_dtype)))
        node.target = nexfort_inductor.linear_epilogue.default
        node.args = (input, weight, bias, epilogue_ops, epilogue_tensor_args, epilogue_scalar_args)
        node.kwargs = {}
        count += 1
    logger.debug(f'Transform linear_out_dtype to linear_epilogue: {count} nodes are transformed')
    if count > 0:
        gm = clean_up_graph_after_modifications(gm)
    return gm

@skip_pass_if_has_no_call_function([aten.clone.default])
def fx_pass_remove_clone_contiguous_format(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:
    target = aten.clone.default

    def pattern(x: torch.Tensor, memory_format: torch.memory_format):
        return target(x, memory_format=memory_format)

    def replacement(x: torch.Tensor, memory_format: torch.memory_format):
        return x

    def is_contiguous_memory_format(match, original_graph: torch.fx.Graph, pattern_graph: torch.fx.Graph) -> bool:
        for node in match.nodes_map.values():
            if node.op == 'call_function' and node.target == target:
                return node.kwargs.get('memory_format') == torch.contiguous_format
        return False
    return replace_pattern_with_filters(gm, pattern, replacement, match_filters=[is_contiguous_memory_format, functools.partial(match_call_function_input_has_users, target=target, users=1)], name='remove_clone_contiguous_format')

@skip_pass_if_has_no_call_function([aten.linear.default, aten.split.Tensor, aten.gelu.default])
@skip_pass_if_unavailable('nexfort_inductor', 'geglu')
def fx_pass_optimize_geglu_by_linear(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:

    def pattern(input: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor], split_size: int, dim: int):
        linear_out = aten.linear.default(input, weight, bias)
        chunk_out = aten.split.Tensor(linear_out, split_size, dim)
        getitem_0 = chunk_out[0]
        getitem_1 = chunk_out[1]
        gelu_out = aten.gelu.default(getitem_1, approximate='tanh')
        mul_out = aten.mul.Tensor(getitem_0, gelu_out)
        return mul_out

    def replacement(input: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor], split_size: int, dim: int):
        input_b = input.size(0)
        input_m = input.size(1)
        input_k = input.size(2)
        input = aten.reshape.default(input, [-1, input_k])
        t_out = aten.t.default(weight)
        gelu_out = nexfort_inductor.geglu.default(input, t_out, bias)
        reshape_out_2 = aten.reshape.default(gelu_out, [input_b, input_m, -1])
        return reshape_out_2
    gm = replace_pattern_with_filters(gm, pattern, replacement, name='optimize_geglu_by_linear')
    return gm

@skip_pass_if_has_no_call_function(aten.linear.default)
@skip_pass_if_unavailable('nexfort_inductor', 'linear_epilogue')
def fx_pass_optimize_lineaer_epilogue(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:
    target = aten.linear.default
    count = 0
    shape_prop_called = False
    for node in gm.graph.nodes:
        if not (node.op == 'call_function' and node.target == target):
            continue
        if not shape_prop_called:
            run_shape_prop(gm, example_inputs)
            shape_prop_called = True
        input = get_node_arg(node, 0, 'input')
        weight = get_node_arg(node, 1, 'weight')
        bias = get_node_arg(node, 2, 'bias')
        output_val = node.meta.get('val')
        if not isinstance(output_val, torch.Tensor):
            continue
        if output_val.ndim not in (2, 3):
            continue
        epilogue_nodes = []
        epilogue_ops = []
        epilogue_tensor_args = []
        epilogue_scalar_args = []
        if output_val.device.type == 'cuda' and torch.version.hip is None and all((hasattr(nexfort_cuda, x) for x in ('cublas_lowp_linear', 'cublas_lowp_linear_add', 'cublas_lowp_linear_activation'))):
            has_to_dtype_fp8 = False
            current_node = node
            while len(current_node.users) == 1:
                prev_node = current_node
                current_node = next(iter(current_node.users))
                if current_node.op != 'call_function':
                    break
                if len(epilogue_nodes) >= 1 or (len(epilogue_nodes) == 0 and current_node.target not in (aten.relu.default, aten.relu_.default, aten.gelu.default, aten.gelu_.default, aten.add.Tensor, aten.add_.Tensor)):
                    break
                unary_op_name = {aten.relu.default: 'relu', aten.relu_.default: 'relu', aten.sigmoid.default: 'sigmoid', aten.sigmoid_.default: 'sigmoid', aten.silu.default: 'silu', aten.silu_.default: 'silu', aten.tanh.default: 'tanh', aten.tanh_.default: 'tanh', aten.gelu.default: 'gelu', aten.gelu_.default: 'gelu', aten.neg.default: 'neg', aten.neg_.default: 'neg', aten.abs.default: 'abs', aten.abs_.default: 'abs', aten.log.default: 'log', aten.log_.default: 'log'}.get(current_node.target)
                binary_op_name = {aten._to_copy.default: 'to_dtype', aten.add.Tensor: 'add', aten.add_.Tensor: 'add_', aten.sub.Tensor: 'sub', aten.sub_.Tensor: 'sub_', aten.mul.Tensor: 'mul', aten.mul_.Tensor: 'mul_', aten.div.Tensor: 'div', aten.div_.Tensor: 'div_', aten.clamp_min.Tensor: 'clamp_min', aten.clamp_min_.Tensor: 'clamp_min_', aten.clamp_max.Tensor: 'clamp_max', aten.clamp_max_.Tensor: 'clamp_max_', aten.clamp_min.default: 'clamp_min', aten.clamp_min_.default: 'clamp_min_', aten.clamp_max.default: 'clamp_max', aten.clamp_max_.default: 'clamp_max_', aten.maximum.default: 'maximum', aten.minimum.default: 'minimum', aten.pow.Tensor_Tensor: 'pow', aten.pow_.Tensor: 'pow_', aten.pow.Tensor_Scalar: 'pow', aten.pow_.Scalar: 'pow_'}.get(current_node.target)
                if unary_op_name is not None:
                    epilogue_nodes.append(current_node)
                    epilogue_ops.append(unary_op_name)
                    epilogue_tensor_args.append(None)
                    epilogue_scalar_args.append(None)
                elif binary_op_name is not None:
                    left_arg = get_node_arg(current_node, 0)
                    right_arg = get_node_arg(current_node, 1)
                    if left_arg == prev_node and right_arg == prev_node:
                        break
                    elif left_arg == prev_node:
                        other_arg = right_arg
                    elif right_arg == prev_node:
                        if binary_op_name.endswith('_'):
                            break
                        other_arg = left_arg
                    else:
                        break
                    if binary_op_name == 'to_dtype':
                        if has_to_dtype_fp8:
                            break
                        if len(current_node.kwargs) > 1:
                            break
                        dtype = current_node.kwargs.get('dtype')
                        if dtype is None:
                            break
                        epilogue_tensor_args.append(None)
                        epilogue_scalar_args.append(int(type_utils.JitScalarType.from_dtype(dtype)))
                        if types.is_fp8_type(dtype):
                            has_to_dtype_fp8 = True
                    elif isinstance(other_arg, (int, float)):
                        epilogue_tensor_args.append(None)
                        epilogue_scalar_args.append(other_arg)
                    elif isinstance(other_arg, torch.fx.Node):
                        other_arg_val = other_arg.meta.get('val')
                        if not isinstance(other_arg_val, torch.Tensor):
                            break
                        if other_arg_val.device != output_val.device:
                            break
                        if not broadcastable(other_arg_val, output_val):
                            break
                        epilogue_tensor_args.append(other_arg)
                        epilogue_scalar_args.append(None)
                    else:
                        break
                    epilogue_nodes.append(current_node)
                    if binary_op_name.endswith('_'):
                        binary_op_name = binary_op_name[:-1]
                    if binary_op_name in ('sub', 'div', 'clamp_min', 'clamp_max', 'pow') and right_arg == prev_node:
                        binary_op_name = f'r{binary_op_name}'
                    epilogue_ops.append(binary_op_name)
                else:
                    break
        nodes = [node] + epilogue_nodes
        nodes[-1].target = nexfort_inductor.linear_epilogue.default
        nodes[-1].args = (input, weight, bias, epilogue_ops, epilogue_tensor_args, epilogue_scalar_args)
        nodes[-1].kwargs = {}
        for n in reversed(epilogue_nodes[:-1]):
            gm.graph.erase_node(n)
        count += 1
    logger.debug(f'Optimize linear_epilogue: {count} nodes are optimized')
    if count > 0:
        gm = clean_up_graph_after_modifications(gm)
    return gm

@skip_pass_if_unavailable('nexfort_inductor', 'scaled_linear')
def fx_pass_optimize_scaled_linear(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]):
    target = nexfort_inductor.scaled_linear.default
    count = 0
    shape_prop_called = False
    for node in gm.graph.nodes:
        if not (node.op == 'call_function' and node.target == target):
            continue
        if not shape_prop_called:
            run_shape_prop(gm, example_inputs)
            shape_prop_called = True
        input = get_node_arg(node, 0, 'input')
        weight = get_node_arg(node, 1, 'weight')
        bias = get_node_arg(node, 2, 'bias')
        out_dtype = get_node_arg(node, 3, 'out_dtype')
        scale_a = get_node_arg(node, 4, 'scale_a')
        scale_b = get_node_arg(node, 5, 'scale_b')
        scale_result = get_node_arg(node, 6, 'scale_result')
        use_fast_accum = get_node_arg(node, 7, 'use_fast_accum', False)
        output_val = node.meta.get('val')
        add_node = None
        activation_node = None
        add_arg = None
        activation_arg = None
        if output_val.device.type == 'cuda' and torch.version.hip is None and hasattr(nexfort_cuda, 'cublas_scaled_linear_add_activation'):
            current_node = node
            while len(current_node.users) == 1:
                prev_node = current_node
                current_node = next(iter(current_node.users))
                if current_node.op != 'call_function':
                    break
                if current_node.target in (aten.add.Tensor, aten.add_.Tensor):
                    if add_node is not None:
                        break
                    if not isinstance(output_val, torch.Tensor) or types.is_fp8_type(output_val.dtype):
                        break
                    left_arg = get_node_arg(current_node, 0)
                    right_arg = get_node_arg(current_node, 1)
                    other_arg = None
                    if left_arg != prev_node:
                        other_arg = left_arg
                    elif right_arg != prev_node:
                        other_arg = right_arg
                    if other_arg is not None:
                        has_seen = False
                        for n in gm.graph.nodes:
                            if n is node:
                                break
                            if n is other_arg:
                                has_seen = True
                                break
                        if not has_seen:
                            break
                        other_arg_val = other_arg.meta.get('val')
                        if isinstance(other_arg_val, torch.Tensor) and other_arg_val.device == output_val.device and (other_arg_val.dtype == output_val.dtype) and (other_arg_val.shape == output_val.shape):
                            add_node = current_node
                            add_arg = other_arg
                    if add_node is None:
                        break
                else:
                    if False:
                        activation_arg = {aten.relu.default: 'relu', aten.relu_.default: 'relu', aten.gelu.default: 'gelu', aten.gelu_.default: 'gelu'}.get(current_node.target)
                        if activation_arg is not None:
                            activation_node = current_node
                    break
        epilogue_nodes = [n for n in [add_node, activation_node] if n is not None]
        nodes = [node] + epilogue_nodes
        nodes[-1].target = nexfort_inductor.scaled_linear_add_activation.default
        nodes[-1].args = (input, weight, bias, add_arg, activation_arg, out_dtype, scale_a, scale_b, scale_result, use_fast_accum)
        nodes[-1].kwargs = {}
        for n in reversed(epilogue_nodes[:-1]):
            gm.graph.erase_node(n)
        count += 1
    logger.debug(f'Optimize scaled_linear: {count} nodes are optimized')
    if count > 0:
        gm = clean_up_graph_after_modifications(gm)
    return gm