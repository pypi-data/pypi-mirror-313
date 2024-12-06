import inspect
import time
from functools import wraps
import torch
_time_cost_deepth = 1

class time_cost:
    """
    simple cost time code ranges using a decorator.
    """

    def __init__(self, *, debug_level=0, on_gpu=False):
        import nexfort
        self._enable = nexfort._nexfort_debug_level >= debug_level
        self.on_gpu = on_gpu

    def __call__(self, func):

        @wraps(func)
        def clocked(*args, **kwargs):
            if not self._enable:
                return func(*args, **kwargs)
            global _time_cost_deepth
            module = inspect.getmodule(func)
            print(f'{'==' * _time_cost_deepth}> function {module.__name__}.{func.__name__} try to run...')
            _time_cost_deepth += 1
            if not self.on_gpu:
                start_time = time.time()
            else:
                start = torch.cuda.Event(enable_timing=True)
                start.record()
            out = func(*args, **kwargs)
            if not self.on_gpu:
                end_time = time.time()
                dur = end_time - start_time
            else:
                end = torch.cuda.Event(enable_timing=True)
                end.record()
                end.synchronize()
                dur = start.elapsed_time(end) / 1000.0
            _time_cost_deepth -= 1
            cuda_mem_max_used = torch.cuda.max_memory_allocated() / 1024 ** 3
            cuda_mem_max_reserved = torch.cuda.max_memory_reserved() / 1024 ** 3
            print(f'Max used CUDA memory : {cuda_mem_max_used:.3f}GiB')
            print(f'Max reserved CUDA memory : {cuda_mem_max_reserved:.3f}GiB')
            print(f'<{'==' * _time_cost_deepth} function {module.__name__}.{func.__name__} finish run, cost {dur} seconds')
            return out
        return clocked