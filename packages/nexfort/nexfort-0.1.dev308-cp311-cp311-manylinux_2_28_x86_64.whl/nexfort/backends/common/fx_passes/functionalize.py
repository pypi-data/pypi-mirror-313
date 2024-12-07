"""
Also check torch.fx.passes.reinplace
"""
from typing import List
import torch
from nexfort.utils.fx_passes import clean_up_graph_after_modifications
from nexfort.utils.logging import logger

def _schemas_match(functional_schema, inplace_schema):
    names_match = not functional_schema.name.endswith('_') and inplace_schema.name[:-1] == functional_schema.name
    arg_types_match = len(functional_schema.arguments) == len(inplace_schema.arguments) and all((a1.type == a2.type for a1, a2 in zip(functional_schema.arguments, inplace_schema.arguments)))
    assert inplace_schema.arguments[0].alias_info is not None and inplace_schema.arguments[0].alias_info.is_write
    assert all((a.alias_info is None for a in inplace_schema.arguments[1:]))
    return names_match and arg_types_match

def maybe_get_functional_op(op):
    if not isinstance(op, torch._ops.OpOverload):
        return None
    op_namespace = op.__module__.split('.')[-1]
    op_base_name = op.overloadpacket.__name__
    maybe_namespace_module = getattr(torch.ops, op_namespace)
    maybe_functional_op = None if maybe_namespace_module is None else getattr(maybe_namespace_module, f'{op_base_name[:-1]}', None)
    if maybe_functional_op is None:
        return None
    functional_overloads = [getattr(maybe_functional_op, overload_name) for overload_name in maybe_functional_op.overloads()]
    functional_overloads_with_matching_schemas = [f for f in functional_overloads if _schemas_match(f._schema, op._schema)]
    if len(functional_overloads_with_matching_schemas) == 0:
        return None
    assert len(functional_overloads_with_matching_schemas) == 1
    functional_op = functional_overloads_with_matching_schemas[0]
    return functional_op

def fx_pass_functionalize(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:
    count = 0
    for node in gm.graph.nodes:
        if node.op != 'call_function':
            continue
        if not isinstance(node.target, torch._ops.OpOverload):
            continue
        if len(node.target._schema.arguments) < 1:
            continue
        if type(node.target._schema.arguments[0].type) is not torch.TensorType:
            continue
        if not node.target.overloadpacket.__name__.endswith('_'):
            continue
        if not (len(node.args) > 0 and isinstance(node.args[0], torch.fx.Node) and (len(node.args[0].users) == 1)):
            continue
        functional_op = maybe_get_functional_op(node.target)
        if functional_op is None:
            continue
        node.target = functional_op
        count += 1
    logger.debug(f'Transform {count} inplace ops to functional ops')
    if count > 0:
        gm = clean_up_graph_after_modifications(gm)
    return gm