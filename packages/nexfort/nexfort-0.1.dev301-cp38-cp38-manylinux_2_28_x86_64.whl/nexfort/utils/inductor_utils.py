

def reset_async_compile_process_pool():
    from torch._inductor.codecache import AsyncCompile
    if (AsyncCompile.process_pool.cache_info().currsize > 0):
        pool = AsyncCompile.process_pool()
        pool.shutdown(wait=True)
        AsyncCompile.process_pool.cache_clear()
        AsyncCompile.warm_pool()
