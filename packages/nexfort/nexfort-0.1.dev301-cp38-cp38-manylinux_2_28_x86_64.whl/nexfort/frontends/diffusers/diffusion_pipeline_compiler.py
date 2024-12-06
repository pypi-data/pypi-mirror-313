
import functools
import torch
from nexfort.compilers import nexfort_compile
from nexfort.utils.attributes import multi_recursive_apply
from nexfort.utils.memory_format import apply_memory_format

def compile_pipe(pipe, *, ignores=(), config=None, fuse_qkv_projections=False, memory_format=torch.preserve_format, quantize=False, quantize_config=None):
    if fuse_qkv_projections:
        pipe = fuse_qkv_projections_in_pipe(pipe)
    pipe = convert_pipe_to_memory_format(pipe, ignores=ignores, memory_format=memory_format)
    if quantize:
        if (quantize_config is None):
            quantize_config = {}
        pipe = quantize_pipe(pipe, ignores=ignores, **quantize_config)
    if (config is None):
        config = {}
    pipe = pure_compile_pipe(pipe, ignores=ignores, **config)
    return pipe

def pure_compile_pipe(pipe, *, ignores=(), **config):
    parts = ['text_encoder', 'text_encoder_2', 'image_encoder', 'unet', 'controlnet', 'fast_unet', 'prior', 'decoder', 'transformer', 'vqgan.down_blocks', 'vqgan.up_blocks', 'vae.decoder', 'vae.encoder']
    multi_recursive_apply(pipe, parts, functools.partial(nexfort_compile, **config), ignores=ignores, verbose=True)
    return pipe

def fuse_qkv_projections_in_pipe(pipe):
    if hasattr(pipe, 'fuse_qkv_projections'):
        pipe.fuse_qkv_projections()
    return pipe

def convert_pipe_to_memory_format(pipe, *, ignores=(), memory_format=torch.preserve_format):
    if (memory_format == torch.preserve_format):
        return pipe
    parts = ['unet', 'controlnet', 'fast_unet', 'prior', 'decoder', 'transformer', 'vqgan', 'vae']
    multi_recursive_apply(pipe, parts, functools.partial(apply_memory_format, memory_format=memory_format), ignores=ignores, verbose=True)
    return pipe

def quantize_pipe(pipe, *, ignores=(), **kwargs):
    from nexfort.quantization import quantize
    parts = ['unet', 'controlnet', 'fast_unet', 'prior', 'decoder', 'transformer']
    multi_recursive_apply(pipe, parts, functools.partial(quantize, **kwargs), ignores=ignores, verbose=True)
    return pipe
