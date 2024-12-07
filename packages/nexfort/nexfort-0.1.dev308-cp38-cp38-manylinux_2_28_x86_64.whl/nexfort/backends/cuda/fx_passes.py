
from typing import List, Optional
import torch
from nexfort.fx_compiler import config as fx_config
from nexfort.utils.fx_passes import replace_pattern_with_filters, skip_pass_if_has_no_call_function, skip_pass_if_unavailable
from nexfort.utils.logging import logger
aten = torch.ops.aten
nexfort_cuda = torch.ops.nexfort_cuda

def apply_fx_passes(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:
    cuda_config = fx_config.cuda
    if cuda_config.disable:
        logger.debug('Skipping all CUDA passes because it is disabled')
        return gm
    if cuda_config.fuse_qkv_projections:
        fx_pass_optimize_fuse_qkv_projections(gm, example_inputs)
    if cuda_config.optimize_conv:
        gm = fx_pass_optimize_conv(gm, example_inputs)
    if cuda_config.optimize_lowp_gemm:
        gm = fx_pass_optimize_lowp_gemm(gm, example_inputs)
    if cuda_config.fuse_timestep_embedding:
        fx_pass_optimize_fuse_timestep_embedding(gm, example_inputs)
    return gm

def fx_pass_optimize_conv(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:
    gm = fx_pass_optimize_conv_bias_add_act(gm, example_inputs)
    gm = fx_pass_optimize_conv_bias_add(gm, example_inputs)
    gm = fx_pass_optimize_conv_bias_act(gm, example_inputs)
    gm = fx_pass_optimize_conv_bias(gm, example_inputs)
    return gm

@skip_pass_if_has_no_call_function([[aten.convolution.default, aten.sigmoid.default], [aten.convolution.default, aten.relu.default], [aten.convolution.default, aten.tanh.default]])
@skip_pass_if_unavailable('nexfort_cuda', 'cudnn_convolution_bias_add_act')
def fx_pass_optimize_conv_bias_add_act(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:
    for act in ['sigmoid', 'relu', 'tanh']:
        act_fn = getattr(aten, act).default

        def pattern_1(x: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor], stride: List[int], padding: List[int], dilation: List[int], is_transposed: bool, output_padding: List[int], groups: int, other: torch.Tensor):
            conv_out = aten.convolution.default(x, weight, bias, stride, padding, dilation, is_transposed, output_padding, groups)
            add_out = aten.add.Tensor(conv_out, other)
            act_out = act_fn(add_out)
            return act_out

        def pattern_2(x: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor], stride: List[int], padding: List[int], dilation: List[int], is_transposed: bool, output_padding: List[int], groups: int, other: torch.Tensor) -> torch.Tensor:
            conv_out = aten.convolution.default(x, weight, bias, stride, padding, dilation, is_transposed, output_padding, groups)
            add_out = aten.add.Tensor(other, conv_out)
            act_out = act_fn(add_out)
            return act_out

        def replacement(x: torch.Tensor, weight: torch.Tensor, bias: torch.Tensor, stride: List[int], padding: List[int], dilation: List[int], is_transposed: bool, output_padding: List[int], groups: int, other: torch.Tensor) -> torch.Tensor:
            return nexfort_cuda.cudnn_convolution_bias_add_act.default(x, weight, bias, other, None, stride, padding, dilation, is_transposed, output_padding, groups, act)
        gm = replace_pattern_with_filters(gm, pattern_1, replacement, name=f'optimize_conv_bias_add_{act}_1')
        gm = replace_pattern_with_filters(gm, pattern_2, replacement, name=f'optimize_conv_bias_add_{act}_2')
    return gm

@skip_pass_if_has_no_call_function(aten.convolution.default)
@skip_pass_if_unavailable('nexfort_cuda', 'cudnn_convolution_bias_add_act')
def fx_pass_optimize_conv_bias_add(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:

    def pattern_1(x: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor], stride: List[int], padding: List[int], dilation: List[int], is_transposed: bool, output_padding: List[int], groups: int, other: torch.Tensor):
        conv_out = aten.convolution.default(x, weight, bias, stride, padding, dilation, is_transposed, output_padding, groups)
        add_out = aten.add.Tensor(conv_out, other)
        return add_out

    def pattern_2(x: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor], stride: List[int], padding: List[int], dilation: List[int], is_transposed: bool, output_padding: List[int], groups: int, other: torch.Tensor) -> torch.Tensor:
        conv_out = aten.convolution.default(x, weight, bias, stride, padding, dilation, is_transposed, output_padding, groups)
        add_out = aten.add.Tensor(other, conv_out)
        return add_out

    def replacement(x: torch.Tensor, weight: torch.Tensor, bias: torch.Tensor, stride: List[int], padding: List[int], dilation: List[int], is_transposed: bool, output_padding: List[int], groups: int, other: torch.Tensor) -> torch.Tensor:
        return nexfort_cuda.cudnn_convolution_bias_add_act.default(x, weight, bias, other, None, stride, padding, dilation, is_transposed, output_padding, groups, None)
    gm = replace_pattern_with_filters(gm, pattern_1, replacement, name='optimize_conv_bias_add_1')
    gm = replace_pattern_with_filters(gm, pattern_2, replacement, name='optimize_conv_bias_add_2')
    return gm

@skip_pass_if_has_no_call_function([[aten.convolution.default, aten.sigmoid.default], [aten.convolution.default, aten.relu.default], [aten.convolution.default, aten.tanh.default]])
@skip_pass_if_unavailable('nexfort_cuda', 'cudnn_convolution_bias_add_act')
def fx_pass_optimize_conv_bias_act(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:
    for act in ['sigmoid', 'relu', 'tanh']:
        act_fn = getattr(aten, act).default

        def pattern(x: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor], stride: List[int], padding: List[int], dilation: List[int], is_transposed: bool, output_padding: List[int], groups: int):
            conv_out = aten.convolution.default(x, weight, bias, stride, padding, dilation, is_transposed, output_padding, groups)
            act_out = act_fn(conv_out)
            return act_out

        def replacement(x: torch.Tensor, weight: torch.Tensor, bias: torch.Tensor, stride: List[int], padding: List[int], dilation: List[int], is_transposed: bool, output_padding: List[int], groups: int) -> torch.Tensor:
            return nexfort_cuda.cudnn_convolution_bias_add_act.default(x, weight, bias, None, None, stride, padding, dilation, is_transposed, output_padding, groups, act)
        gm = replace_pattern_with_filters(gm, pattern, replacement, name=f'optimize_conv_bias_{act}')
    return gm

@skip_pass_if_has_no_call_function(aten.convolution.default)
@skip_pass_if_unavailable('nexfort_cuda', 'cudnn_convolution_bias_add_act')
def fx_pass_optimize_conv_bias(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:

    def pattern(x: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor], stride: List[int], padding: List[int], dilation: List[int], is_transposed: bool, output_padding: List[int], groups: int) -> torch.Tensor:
        return aten.convolution.default(x, weight, bias, stride, padding, dilation, is_transposed, output_padding, groups)

    def replacement(x: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor], stride: List[int], padding: List[int], dilation: List[int], is_transposed: bool, output_padding: List[int], groups: int) -> torch.Tensor:
        return nexfort_cuda.cudnn_convolution_bias_add_act.default(x, weight, bias, None, None, stride, padding, dilation, is_transposed, output_padding, groups, None)
    gm = replace_pattern_with_filters(gm, pattern, replacement, name='optimize_conv_bias')
    return gm

def fx_pass_optimize_lowp_gemm(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:
    gm = fx_pass_optimize_matmul(gm, example_inputs)
    gm = fx_pass_optimize_linear_activation(gm, example_inputs)
    gm = fx_pass_optimize_linear_add(gm, example_inputs)
    gm = fx_pass_optimize_linear(gm, example_inputs)
    gm = fx_pass_optimize_linear_activation_by_addmm(gm, example_inputs)
    gm = fx_pass_optimize_linear_add_by_addmm(gm, example_inputs)
    gm = fx_pass_optimize_addmm_add(gm, example_inputs)
    gm = fx_pass_optimize_addmm_activation(gm, example_inputs)
    gm = fx_pass_optimize_addmm(gm, example_inputs)
    gm = fx_pass_optimize_linear_activation_by_mm(gm, example_inputs)
    gm = fx_pass_optimize_linear_add_by_mm(gm, example_inputs)
    if (not fx_config.yield_to_mixed_mm):
        gm = fx_pass_optimize_addmm_by_mm(gm, example_inputs)
        gm = fx_pass_optimize_mm(gm, example_inputs)
    gm = fx_pass_optimize_baddbmm_by_bmm(gm, example_inputs)
    gm = fx_pass_optimize_bmm(gm, example_inputs)
    gm = fx_pass_optimize_baddbmm(gm, example_inputs)
    return gm

@skip_pass_if_has_no_call_function(aten.matmul.default)
@skip_pass_if_unavailable('nexfort_cuda', 'cublas_lowp_matmul')
def fx_pass_optimize_matmul(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:

    def pattern(this: torch.Tensor, other: torch.Tensor) -> torch.Tensor:
        return aten.matmul.default(this, other)

    def replacement(this: torch.Tensor, other: torch.Tensor) -> torch.Tensor:
        return nexfort_cuda.cublas_lowp_matmul.default(this, other)
    gm = replace_pattern_with_filters(gm, pattern, replacement, name='optimize_matmul')
    return gm

@skip_pass_if_has_no_call_function(aten.addmm.default)
@skip_pass_if_unavailable('nexfort_cuda', 'cublas_lowp_addmm')
def fx_pass_optimize_addmm(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:

    def pattern(input: torch.Tensor, mat1: torch.Tensor, mat2: torch.Tensor) -> torch.Tensor:
        return aten.addmm.default(input, mat1, mat2)

    def replacement(input: torch.Tensor, mat1: torch.Tensor, mat2: torch.Tensor) -> torch.Tensor:
        return nexfort_cuda.cublas_lowp_addmm.default(input, mat1, mat2, 1, 1)
    gm = replace_pattern_with_filters(gm, pattern, replacement, name='optimize_lowp_addmm')
    return gm

@skip_pass_if_has_no_call_function(aten.mm.default)
@skip_pass_if_unavailable('nexfort_cuda', 'cublas_lowp_addmm')
def fx_pass_optimize_addmm_by_mm(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:

    def pattern_1(input: torch.Tensor, mat2: torch.Tensor, other: torch.Tensor) -> torch.Tensor:
        mm_out = aten.mm.default(input, mat2)
        add_out = aten.add.Tensor(mm_out, other)
        return add_out

    def pattern_2(input: torch.Tensor, mat2: torch.Tensor, other: torch.Tensor) -> torch.Tensor:
        mm_out = aten.mm.default(input, mat2)
        add_out = aten.add.Tensor(other, mm_out)
        return add_out

    def replacement(input: torch.Tensor, mat2: torch.Tensor, other: torch.Tensor) -> torch.Tensor:
        return nexfort_cuda.cublas_lowp_addmm.default(input, other, mat2, 1, 1)
    gm = replace_pattern_with_filters(gm, pattern_1, replacement, name='optimize_lowp_addmm_by_mm_1')
    gm = replace_pattern_with_filters(gm, pattern_2, replacement, name='optimize_lowp_addmm_by_mm_2')
    return gm

@skip_pass_if_has_no_call_function(aten.addmm.default)
@skip_pass_if_unavailable('nexfort_cuda', 'cublas_lowp_addmm_add')
def fx_pass_optimize_addmm_add(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:

    def pattern_1(input: torch.Tensor, mat1: torch.Tensor, mat2: torch.Tensor, other: torch.Tensor) -> torch.Tensor:
        addmm_out = aten.addmm.default(input, mat1, mat2)
        add_out = aten.add.Tensor(addmm_out, other)
        return add_out

    def pattern_2(input: torch.Tensor, mat1: torch.Tensor, mat2: torch.Tensor, other: torch.Tensor) -> torch.Tensor:
        addmm_out = aten.addmm.default(input, mat1, mat2)
        add_out = aten.add.Tensor(other, addmm_out)
        return add_out

    def replacement(input: torch.Tensor, mat1: torch.Tensor, mat2: torch.Tensor, other: torch.Tensor) -> torch.Tensor:
        return nexfort_cuda.cublas_lowp_addmm_add.default(input, mat1, mat2, other, 1, 1, 1)
    gm = replace_pattern_with_filters(gm, pattern_1, replacement, name='optimize_lowp_addmm_add_1')
    gm = replace_pattern_with_filters(gm, pattern_2, replacement, name='optimize_lowp_addmm_add_2')
    return gm

@skip_pass_if_has_no_call_function([[aten.addmm.default, aten.relu.default], [aten.addmm.default, aten.gelu.default]])
@skip_pass_if_unavailable('nexfort_cuda', 'cublas_lowp_addmm_activation')
def fx_pass_optimize_addmm_activation(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:

    def pattern_relu(input: torch.Tensor, mat1: torch.Tensor, mat2: torch.Tensor) -> torch.Tensor:
        addmm_out = aten.addmm.default(input, mat1, mat2)
        relu_out = aten.relu.default(addmm_out)
        return relu_out

    def replacement_relu(input: torch.Tensor, mat1: torch.Tensor, mat2: torch.Tensor) -> torch.Tensor:
        return nexfort_cuda.cublas_lowp_addmm_activation.default(input, mat1, mat2, 1, 1, False)

    def pattern_gelu(input: torch.Tensor, mat1: torch.Tensor, mat2: torch.Tensor) -> torch.Tensor:
        addmm_out = aten.addmm.default(input, mat1, mat2)
        gelu_out = aten.gelu.default(addmm_out, approximate='tanh')
        return gelu_out

    def replacement_gelu(input: torch.Tensor, mat1: torch.Tensor, mat2: torch.Tensor) -> torch.Tensor:
        return nexfort_cuda.cublas_lowp_addmm_activation.default(input, mat1, mat2, 1, 1, True)
    gm = replace_pattern_with_filters(gm, pattern_relu, replacement_relu, name='optimize_lowp_addmm_relu')
    gm = replace_pattern_with_filters(gm, pattern_gelu, replacement_gelu, name='optimize_lowp_addmm_gelu')
    return gm

@skip_pass_if_has_no_call_function(aten.mm.default)
@skip_pass_if_unavailable('nexfort_cuda', 'cublas_lowp_mm')
def fx_pass_optimize_mm(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:

    def pattern(input: torch.Tensor, mat2: torch.Tensor) -> torch.Tensor:
        return aten.mm.default(input, mat2)

    def replacement(input: torch.Tensor, mat2: torch.Tensor) -> torch.Tensor:
        return nexfort_cuda.cublas_lowp_mm.default(input, mat2)
    gm = replace_pattern_with_filters(gm, pattern, replacement, name='optimize_lowp_mm')
    return gm

@skip_pass_if_has_no_call_function(aten.baddbmm.default)
@skip_pass_if_unavailable('nexfort_cuda', 'cublas_lowp_baddbmm')
def fx_pass_optimize_baddbmm(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:

    def pattern(input: torch.Tensor, batch1: torch.Tensor, batch2: torch.Tensor) -> torch.Tensor:
        return aten.baddbmm.default(input, batch1, batch2)

    def replacement(input: torch.Tensor, batch1: torch.Tensor, batch2: torch.Tensor) -> torch.Tensor:
        return nexfort_cuda.cublas_lowp_baddbmm.default(input, batch1, batch2, 1, 1)
    gm = replace_pattern_with_filters(gm, pattern, replacement, name='optimize_lowp_baddbmm')
    return gm

@skip_pass_if_has_no_call_function(aten.bmm.default)
@skip_pass_if_unavailable('nexfort_cuda', 'cublas_lowp_baddbmm')
def fx_pass_optimize_baddbmm_by_bmm(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:

    def pattern_1(input: torch.Tensor, batch1: torch.Tensor, batch2: torch.Tensor) -> torch.Tensor:
        bmm_out = aten.bmm.default(batch1, batch2)
        add_out = aten.add.Tensor(bmm_out, input)
        return add_out

    def pattern_2(input: torch.Tensor, batch1: torch.Tensor, batch2: torch.Tensor) -> torch.Tensor:
        bmm_out = aten.bmm.default(batch1, batch2)
        add_out = aten.add.Tensor(input, bmm_out)
        return add_out

    def replacement(input: torch.Tensor, batch1: torch.Tensor, batch2: torch.Tensor) -> torch.Tensor:
        return nexfort_cuda.cublas_lowp_baddbmm.default(input, batch1, batch2, 1, 1)
    gm = replace_pattern_with_filters(gm, pattern_1, replacement, name='optimize_lowp_baddbmm_1')
    gm = replace_pattern_with_filters(gm, pattern_2, replacement, name='optimize_lowp_baddbmm_2')
    return gm

@skip_pass_if_has_no_call_function(aten.bmm.default)
@skip_pass_if_unavailable('nexfort_cuda', 'cublas_lowp_bmm')
def fx_pass_optimize_bmm(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:

    def pattern(input: torch.Tensor, mat2: torch.Tensor) -> torch.Tensor:
        return aten.bmm.default(input, mat2)

    def replacement(input: torch.Tensor, mat2: torch.Tensor) -> torch.Tensor:
        return nexfort_cuda.cublas_lowp_bmm.default(input, mat2)
    gm = replace_pattern_with_filters(gm, pattern, replacement, name='optimize_lowp_bmm')
    return gm

@skip_pass_if_has_no_call_function(aten.linear.default)
@skip_pass_if_unavailable('nexfort_cuda', 'cublas_lowp_linear')
def fx_pass_optimize_linear(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:

    def pattern(input: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor]) -> torch.Tensor:
        linear_out = aten.linear.default(input, weight, bias)
        return linear_out

    def replacement(input: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor]) -> torch.Tensor:
        return nexfort_cuda.cublas_lowp_linear.default(input, weight, bias)
    gm = replace_pattern_with_filters(gm, pattern, replacement, name='optimize_lowp_linear')
    return gm

@skip_pass_if_has_no_call_function([[aten.linear.default, aten.relu.default], [aten.linear.default, aten.gelu.default]])
@skip_pass_if_unavailable('nexfort_cuda', 'cublas_lowp_linear_activation')
def fx_pass_optimize_linear_activation(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:

    def pattern_relu(input: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor]) -> torch.Tensor:
        linear_out = aten.linear.default(input, weight, bias)
        relu_out = aten.relu.default(linear_out)
        return relu_out

    def replacement_relu(input: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor]) -> torch.Tensor:
        return nexfort_cuda.cublas_lowp_linear_activation.default(input, weight, bias, False)

    def pattern_gelu(input: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor]) -> torch.Tensor:
        linear_out = aten.linear.default(input, weight, bias)
        gelu_out = aten.gelu.default(linear_out, approximate='tanh')
        return gelu_out

    def replacement_gelu(input: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor]) -> torch.Tensor:
        return nexfort_cuda.cublas_lowp_linear_activation.default(input, weight, bias, True)
    gm = replace_pattern_with_filters(gm, pattern_relu, replacement_relu, name='optimize_lowp_linear_relu_by_addmm')
    gm = replace_pattern_with_filters(gm, pattern_gelu, replacement_gelu, name='optimize_lowp_linear_gelu')
    return gm

@skip_pass_if_has_no_call_function([aten.linear.default])
@skip_pass_if_unavailable('nexfort_cuda', 'cublas_lowp_linear_add')
def fx_pass_optimize_linear_add(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:

    def pattern_1(input: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor], other: torch.Tensor) -> torch.Tensor:
        linear_out = aten.linear.default(input, weight, bias)
        add_out = aten.add.Tensor(linear_out, other)
        return add_out

    def pattern_2(input: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor], other: torch.Tensor) -> torch.Tensor:
        linear_out = aten.linear.default(input, weight, bias)
        add_out = aten.add.Tensor(other, linear_out)
        return add_out

    def replacement(input: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor], other: torch.Tensor) -> torch.Tensor:
        return nexfort_cuda.cublas_lowp_linear_add.default(input, weight, other, bias, 1)
    gm = replace_pattern_with_filters(gm, pattern_1, replacement, name='optimize_lowp_linear_add_1')
    gm = replace_pattern_with_filters(gm, pattern_2, replacement, name='optimize_lowp_linear_add_2')
    return gm

@skip_pass_if_has_no_call_function(aten.addmm.default)
@skip_pass_if_unavailable('nexfort_cuda', 'cublas_lowp_linear')
def fx_pass_optimize_linear_by_addmm(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:

    def pattern(input: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor], shape_1: List[int], shape_2: List[int]) -> torch.Tensor:
        reshape_out_1 = aten.reshape.default(input, shape_1)
        t_out = aten.t.default(weight)
        addmm_out = aten.addmm.default(bias, reshape_out_1, t_out)
        reshape_out_2 = aten.reshape.default(addmm_out, shape_2)
        return reshape_out_2

    def replacement(input: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor], shape_1: List[int], shape_2: List[int]) -> torch.Tensor:
        return nexfort_cuda.cublas_lowp_linear.default(input, weight, bias)
    gm = replace_pattern_with_filters(gm, pattern, replacement, name='optimize_lowp_linear_by_addmm')
    return gm

@skip_pass_if_has_no_call_function([[aten.addmm.default, aten.relu.default], [aten.addmm.default, aten.gelu.default]])
@skip_pass_if_unavailable('nexfort_cuda', 'cublas_lowp_linear_activation')
def fx_pass_optimize_linear_activation_by_addmm(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:

    def pattern_relu(input: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor], shape_1: List[int], shape_2: List[int]) -> torch.Tensor:
        reshape_out_1 = aten.reshape.default(input, shape_1)
        t_out = aten.t.default(weight)
        addmm_out = aten.addmm.default(bias, reshape_out_1, t_out)
        reshape_out_2 = aten.reshape.default(addmm_out, shape_2)
        relu_out = aten.relu.default(reshape_out_2)
        return relu_out

    def replacement_relu(input: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor], shape_1: List[int], shape_2: List[int]) -> torch.Tensor:
        return nexfort_cuda.cublas_lowp_linear_activation.default(input, weight, bias, False)

    def pattern_gelu(input: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor], shape_1: List[int], shape_2: List[int]) -> torch.Tensor:
        reshape_out_1 = aten.reshape.default(input, shape_1)
        t_out = aten.t.default(weight)
        addmm_out = aten.addmm.default(bias, reshape_out_1, t_out)
        reshape_out_2 = aten.reshape.default(addmm_out, shape_2)
        gelu_out = aten.gelu.default(reshape_out_2, approximate='tanh')
        return gelu_out

    def replacement_gelu(input: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor], shape_1: List[int], shape_2: List[int]) -> torch.Tensor:
        return nexfort_cuda.cublas_lowp_linear_activation.default(input, weight, bias, True)
    gm = replace_pattern_with_filters(gm, pattern_relu, replacement_relu, name='optimize_lowp_linear_relu_by_addmm')
    gm = replace_pattern_with_filters(gm, pattern_gelu, replacement_gelu, name='optimize_lowp_linear_gelu_by_addmm')
    return gm

@skip_pass_if_has_no_call_function([aten.addmm.default])
@skip_pass_if_unavailable('nexfort_cuda', 'cublas_lowp_linear_add')
def fx_pass_optimize_linear_add_by_addmm(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:

    def pattern_1(input: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor], other: torch.Tensor, shape_1: List[int], shape_2: List[int]) -> torch.Tensor:
        reshape_out_1 = aten.reshape.default(input, shape_1)
        t_out = aten.t.default(weight)
        addmm_out = aten.addmm.default(bias, reshape_out_1, t_out)
        reshape_out_2 = aten.reshape.default(addmm_out, shape_2)
        add_out = aten.add.Tensor(reshape_out_2, other)
        return add_out

    def pattern_2(input: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor], other: torch.Tensor, shape_1: List[int], shape_2: List[int]) -> torch.Tensor:
        reshape_out_1 = aten.reshape.default(input, shape_1)
        t_out = aten.t.default(weight)
        addmm_out = aten.addmm.default(bias, reshape_out_1, t_out)
        reshape_out_2 = aten.reshape.default(addmm_out, shape_2)
        add_out = aten.add.Tensor(other, reshape_out_2)
        return add_out

    def replacement(input: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor], other: torch.Tensor, shape_1: List[int], shape_2: List[int]) -> torch.Tensor:
        return nexfort_cuda.cublas_lowp_linear_add.default(input, weight, other, bias, 1)
    gm = replace_pattern_with_filters(gm, pattern_1, replacement, name='optimize_lowp_linear_add_by_addmm_1')
    gm = replace_pattern_with_filters(gm, pattern_2, replacement, name='optimize_lowp_linear_add_by_addmm_2')
    return gm

@skip_pass_if_has_no_call_function(aten.mm.default)
@skip_pass_if_unavailable('nexfort_cuda', 'cublas_lowp_linear')
def fx_pass_optimize_linear_by_mm(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:

    def pattern_1(input: torch.Tensor, weight: torch.Tensor, shape_1: List[int], shape_2: List[int]) -> torch.Tensor:
        reshape_out_1 = aten.reshape.default(input, shape_1)
        t_out = aten.t.default(weight)
        mm_out = aten.mm.default(reshape_out_1, t_out)
        reshape_out_2 = aten.reshape.default(mm_out, shape_2)
        return reshape_out_2

    def replacement_1(input: torch.Tensor, weight: torch.Tensor, shape_1: List[int], shape_2: List[int]) -> torch.Tensor:
        return nexfort_cuda.cublas_lowp_linear.default(input, weight, None)
    gm = replace_pattern_with_filters(gm, pattern_1, replacement_1, name='optimize_lowp_linear_by_mm')
    return gm

@skip_pass_if_has_no_call_function([[aten.mm.default, aten.relu.default], [aten.mm.default, aten.gelu.default]])
@skip_pass_if_unavailable('nexfort_cuda', 'cublas_lowp_linear_activation')
def fx_pass_optimize_linear_activation_by_mm(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:

    def pattern_relu(input: torch.Tensor, weight: torch.Tensor, shape_1: List[int], shape_2: List[int]) -> torch.Tensor:
        reshape_out_1 = aten.reshape.default(input, shape_1)
        t_out = aten.t.default(weight)
        mm_out = aten.mm.default(reshape_out_1, t_out)
        reshape_out_2 = aten.reshape.default(mm_out, shape_2)
        relu_out = aten.relu.default(reshape_out_2)
        return relu_out

    def replacement_relu(input: torch.Tensor, weight: torch.Tensor, shape_1: List[int], shape_2: List[int]) -> torch.Tensor:
        return nexfort_cuda.cublas_lowp_linear_activation.default(input, weight, None, False)

    def pattern_gelu(input: torch.Tensor, weight: torch.Tensor, shape_1: List[int], shape_2: List[int]) -> torch.Tensor:
        reshape_out_1 = aten.reshape.default(input, shape_1)
        t_out = aten.t.default(weight)
        mm_out = aten.mm.default(reshape_out_1, t_out)
        reshape_out_2 = aten.reshape.default(mm_out, shape_2)
        gelu_out = aten.gelu.default(reshape_out_2, approximate='tanh')
        return gelu_out

    def replacement_gelu(input: torch.Tensor, weight: torch.Tensor, shape_1: List[int], shape_2: List[int]) -> torch.Tensor:
        return nexfort_cuda.cublas_lowp_linear_activation.default(input, weight, None, True)
    gm = replace_pattern_with_filters(gm, pattern_relu, replacement_relu, name='optimize_lowp_linear_relu_by_mm')
    gm = replace_pattern_with_filters(gm, pattern_gelu, replacement_gelu, name='optimize_lowp_linear_gelu_by_mm')
    return gm

@skip_pass_if_has_no_call_function(aten.mm.default)
@skip_pass_if_unavailable('nexfort_cuda', 'cublas_lowp_linear_add')
def fx_pass_optimize_linear_add_by_mm(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:

    def pattern_1(input: torch.Tensor, weight: torch.Tensor, other: torch.Tensor, shape_1: List[int], shape_2: List[int]) -> torch.Tensor:
        reshape_out_1 = aten.reshape.default(input, shape_1)
        t_out = aten.t.default(weight)
        mm_out = aten.mm.default(reshape_out_1, t_out)
        reshape_out_2 = aten.reshape.default(mm_out, shape_2)
        add_out = aten.add.Tensor(reshape_out_2, other)
        return add_out

    def pattern_2(input: torch.Tensor, weight: torch.Tensor, other: torch.Tensor, shape_1: List[int], shape_2: List[int]) -> torch.Tensor:
        reshape_out_1 = aten.reshape.default(input, shape_1)
        t_out = aten.t.default(weight)
        mm_out = aten.mm.default(reshape_out_1, t_out)
        reshape_out_2 = aten.reshape.default(mm_out, shape_2)
        add_out = aten.add.Tensor(other, reshape_out_2)
        return add_out

    def replacement(input: torch.Tensor, weight: torch.Tensor, other: torch.Tensor, shape_1: List[int], shape_2: List[int]) -> torch.Tensor:
        return nexfort_cuda.cublas_lowp_linear_add.default(input, weight, other, None, 1)
    gm = replace_pattern_with_filters(gm, pattern_1, replacement, name='optimize_lowp_linear_add_by_mm_1')
    gm = replace_pattern_with_filters(gm, pattern_2, replacement, name='optimize_lowp_linear_add_by_mm_2')
    return gm

@skip_pass_if_unavailable('nexfort_cuda', 'cuda_timestep_embedding')
def fx_pass_optimize_fuse_timestep_embedding(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:

    def pattern_1(timesteps: torch.Tensor, dim: int, start: int, end: int, dtype: torch.float32, device: torch.device, pin_memory: bool, mul_scalar: float, div_scalar: float) -> torch.Tensor:
        arange = aten.arange.start(start, end, dtype=dtype, device=device, pin_memory=pin_memory)
        mul = aten.mul.Tensor(arange, mul_scalar)
        div = aten.div.Tensor(mul, div_scalar)
        exp = aten.exp.default(div)
        slice_1 = aten.slice.Tensor(timesteps, 0, 0, 9223372036854775807)
        unsqueeze = aten.unsqueeze.default(slice_1, 1)
        to_copy = aten._to_copy.default(unsqueeze, dtype=torch.float32)
        unsqueeze_1 = aten.unsqueeze.default(exp, 0)
        slice_2 = aten.slice.Tensor(unsqueeze_1, 1, 0, 9223372036854775807)
        mul_1 = aten.mul.Tensor(to_copy, slice_2)
        sin = aten.sin.default(mul_1)
        cos = aten.cos.default(mul_1)
        cat = aten.cat.default([sin, cos], (- 1))
        slice_3 = aten.slice.Tensor(cat, 0, 0, 9223372036854775807)
        slice_4 = aten.slice.Tensor(slice_3, 1, dim, 9223372036854775807)
        slice_5 = aten.slice.Tensor(slice_3, 1, 0, dim)
        cat_1 = aten.cat.default([slice_4, slice_5], (- 1))
        return cat_1

    def pattern_2(timesteps: torch.Tensor, dim: int, start: int, end: int, dtype: torch.float32, device: torch.device, pin_memory: bool, mul_scalar: float, div_scalar: float) -> torch.Tensor:
        arange = aten.arange.start(start, end, dtype=dtype, device=device, pin_memory=pin_memory)
        mul = aten.mul.Tensor(arange, mul_scalar)
        div = aten.div.Tensor(mul, div_scalar)
        exp = aten.exp.default(div)
        slice_1 = aten.slice.Tensor(timesteps, 0, 0, 9223372036854775807)
        unsqueeze = aten.unsqueeze.default(slice_1, 1)
        unsqueeze_1 = aten.unsqueeze.default(exp, 0)
        slice_2 = aten.slice.Tensor(unsqueeze_1, 1, 0, 9223372036854775807)
        mul_1 = aten.mul.Tensor(unsqueeze, slice_2)
        sin = aten.sin.default(mul_1)
        cos = aten.cos.default(mul_1)
        cat = aten.cat.default([sin, cos], (- 1))
        slice_3 = aten.slice.Tensor(cat, 0, 0, 9223372036854775807)
        slice_4 = aten.slice.Tensor(slice_3, 1, dim, 9223372036854775807)
        slice_5 = aten.slice.Tensor(slice_3, 1, 0, dim)
        cat_1 = aten.cat.default([slice_4, slice_5], (- 1))
        return cat_1

    def replacement(timesteps: torch.Tensor, dim: int, start: int, end: int, dtype: torch.float32, device: torch.device, pin_memory: bool, mul_scalar: float, div_scalar: float) -> torch.Tensor:
        n = aten.size.default(timesteps)[0]
        return nexfort_cuda.cuda_timestep_embedding.default(timesteps, n, dim, start, end, dtype, device, pin_memory, mul_scalar, div_scalar, 1, True)
    gm = replace_pattern_with_filters(gm, pattern_1, replacement, name='optimize_timestep_embedding_1')
    gm = replace_pattern_with_filters(gm, pattern_2, replacement, name='optimize_timestep_embedding_2')
    return gm

@skip_pass_if_unavailable('nexfort_cuda', 'cublas_lowp_linear')
def fx_pass_optimize_fuse_qkv_projections(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:

    def pattern_1(input: torch.Tensor, query_weight: torch.Tensor, key_weight: torch.Tensor, value_weight: torch.Tensor, shape: List[int]) -> torch.Tensor:
        query = aten.linear.default(input, query_weight)
        view_query = aten.reshape.default(query, shape)
        transposed_query = aten.transpose.int(view_query, 1, 2)
        key = aten.linear.default(input, key_weight)
        view_key = aten.reshape.default(key, shape)
        transposed_key = aten.transpose.int(view_key, 1, 2)
        value = aten.linear.default(input, value_weight)
        view_value = aten.reshape.default(value, shape)
        transposed_value = aten.transpose.int(view_value, 1, 2)
        attention = aten.scaled_dot_product_attention.default(transposed_query, transposed_key, transposed_value)
        return attention

    def replacement_1(input: torch.Tensor, query_weight: torch.Tensor, key_weight: torch.Tensor, value_weight: torch.Tensor, shape: List[int]) -> torch.Tensor:
        cat_weight = aten.cat.default([query_weight, key_weight, value_weight], 0)
        fused_qkv = aten.linear.default(input, cat_weight)
        (query, key, value) = aten.chunk.default(fused_qkv, 3, dim=(- 1))
        view_query = aten.reshape.default(query, shape)
        transposed_query = aten.transpose.int(view_query, 1, 2)
        view_key = aten.reshape.default(key, shape)
        transposed_key = aten.transpose.int(view_key, 1, 2)
        view_value = aten.reshape.default(value, shape)
        transposed_value = aten.transpose.int(view_value, 1, 2)
        attention = aten.scaled_dot_product_attention.default(transposed_query, transposed_key, transposed_value)
        return attention

    def pattern_2(input: torch.Tensor, query_weight: torch.Tensor, query_bias: torch.Tensor, key_weight: torch.Tensor, key_bias: torch.Tensor, value_weight: torch.Tensor, value_bias: torch.Tensor, shape: List[int]) -> torch.Tensor:
        query = aten.linear.default(input, query_weight, query_bias)
        view_query = aten.reshape.default(query, shape)
        transposed_query = aten.transpose.int(view_query, 1, 2)
        key = aten.linear.default(input, key_weight, key_bias)
        view_key = aten.reshape.default(key, shape)
        transposed_key = aten.transpose.int(view_key, 1, 2)
        value = aten.linear.default(input, value_weight, value_bias)
        view_value = aten.reshape.default(value, shape)
        transposed_value = aten.transpose.int(view_value, 1, 2)
        attention = aten.scaled_dot_product_attention.default(transposed_query, transposed_key, transposed_value)
        return attention

    def replacement_2(input: torch.Tensor, query_weight: torch.Tensor, query_bias: torch.Tensor, key_weight: torch.Tensor, key_bias: torch.Tensor, value_weight: torch.Tensor, value_bias: torch.Tensor, shape: List[int]) -> torch.Tensor:
        cat_weight = aten.cat.default([query_weight, key_weight, value_weight], 0)
        cat_bias = aten.cat.default([query_bias, key_bias, value_bias], 0)
        fused_qkv = aten.linear.default(input, cat_weight, cat_bias)
        (query, key, value) = aten.chunk.default(fused_qkv, 3, dim=(- 1))
        view_query = aten.reshape.default(query, shape)
        transposed_query = aten.transpose.int(view_query, 1, 2)
        view_key = aten.reshape.default(key, shape)
        transposed_key = aten.transpose.int(view_key, 1, 2)
        view_value = aten.reshape.default(value, shape)
        transposed_value = aten.transpose.int(view_value, 1, 2)
        attention = aten.scaled_dot_product_attention.default(transposed_query, transposed_key, transposed_value)
        return attention
    gm = replace_pattern_with_filters(gm, pattern_1, replacement_1, name='optimize_fuse_qkv_projections_1')
    gm = replace_pattern_with_filters(gm, pattern_2, replacement_2, name='optimize_fuse_qkv_projections_2')
    return gm
