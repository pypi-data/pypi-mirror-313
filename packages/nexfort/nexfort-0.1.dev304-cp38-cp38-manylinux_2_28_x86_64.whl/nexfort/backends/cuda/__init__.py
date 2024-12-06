
import nexfort
if (nexfort._C_cuda is None):

    def apply_fx_passes(gm, *args, **kwargs):
        return gm
else:
    from . import op_registry
    from .fx_passes import apply_fx_passes
