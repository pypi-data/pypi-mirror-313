from typing import List, Optional
import torch
from nexfort.utils import checks
from nexfort.utils.logging import logger
aten = torch.ops.aten
nexfort_cuda = torch.ops.nexfort_cuda
if checks.is_inductor_supported():
    from torch._inductor import ir
    from torch._inductor.lowering import fallback_handler, register_lowering
    from torch._inductor.virtualized import V
    if hasattr(nexfort_cuda, 'cudnn_convolution_bias_add_act'):

        @register_lowering(nexfort_cuda.cudnn_convolution_bias_add_act)
        def cudnn_convolution_bias_add_act_lowering(x: ir.TensorBox, weight: ir.TensorBox, bias: Optional[ir.TensorBox], z: Optional[ir.TensorBox], alpha: float, stride: List[int], padding: List[int], dilation: List[int], transposed: bool, output_padding: List[int], groups: int, act: str):
            from torch._inductor.kernel.conv import conv_layout
            kwargs = {'stride': stride, 'padding': padding, 'dilation': dilation, 'transposed': transposed, 'output_padding': output_padding, 'groups': groups}
            (out_chan, in_chan, *kernel_shape) = V.graph.sizevars.evaluate_static_shapes(weight.get_size())
            ndim = len(kernel_shape)
            x.realize()
            weight.realize()
            if bias is not None:
                bias.realize()
                bias.freeze_layout()
                V.graph.sizevars.evaluate_static_shapes(bias.get_size())
            if z is not None:
                z.realize()
            layout_opt = False
            from torch._inductor import config as inductor_config
            if inductor_config.layout_optimization:
                if getattr(inductor_config, 'force_layout_optimization', False):
                    layout_opt = True
                elif weight.get_device().type == 'cuda' and checks.cuda_capability_compare('ge', 7, 0):
                    layout_opt = True
            layout = None
            if layout_opt:
                if ndim == 2:
                    V.graph.num_channels_last_conv += 1
                    x = ir.ExternKernel.require_channels_last(x)
                    weight = ir.ExternKernel.require_channels_last(weight)
                    layout = conv_layout(x, weight, None, **kwargs)
                else:
                    layout = conv_layout(x, weight, None, **kwargs)
                    req_stride_order = ir.get_stride_order(V.graph.sizevars.size_hints(layout.stride))
                    x = ir.ExternKernel.require_stride_order(x, req_stride_order)
                    weight = ir.ExternKernel.require_stride_order(weight, req_stride_order)
            e = None
            try:
                if layout is None:
                    layout = conv_layout(x, weight, None, **kwargs)
            except TypeError as e:
                logger.debug(f'Failed to get stride order for cudnn_convolution_bias_add_act by calling conv_layout: {e}')
            if layout is None:
                try:
                    layout = ir.FixedLayout(weight.get_device(), weight.get_dtype(), weight.get_size(), weight.get_stride())
                except TypeError as e:
                    logger.debug(f'Failed to get layout for cudnn_convolution_bias_add_act by calling FixedLayout: {e}')
            if layout is None:
                logger.warning(f'Failed to get layout for cudnn_convolution_bias_add_act, performance might suffer: {e}')
            else:
                req_stride_order = ir.get_stride_order(V.graph.sizevars.size_hints(layout.stride))
                x = ir.ExternKernel.require_stride_order(x, req_stride_order)
                weight = ir.ExternKernel.require_stride_order(weight, req_stride_order)
                if z is not None:
                    z = ir.ExternKernel.require_stride_order(z, req_stride_order)
            return fallback_handler(nexfort_cuda.cudnn_convolution_bias_add_act.default, add_to_fallback_set=False)(x, weight, bias, z, alpha, stride, padding, dilation, transposed, output_padding, groups, act)
    if hasattr(nexfort_cuda, 'cudnn_convolution_reshape_bias'):

        @register_lowering(nexfort_cuda.cudnn_convolution_reshape_bias)
        def cudnn_convolution_reshape_bias_lowering(dim: int, bias: ir.TensorBox):
            shape = [1] * dim
            shape[1] = -1
            return ir.TensorBox(ir.View.create(bias.data, shape))