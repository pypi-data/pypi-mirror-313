
import os
import shutil

def main():
    try:
        from torch._inductor.utils import cache_dir
    except ImportError:
        from torch._inductor.runtime.runtime_utils import cache_dir
    if os.path.exists(cache_dir()):
        shutil.rmtree(cache_dir())
if (__name__ == '__main__'):
    main()
