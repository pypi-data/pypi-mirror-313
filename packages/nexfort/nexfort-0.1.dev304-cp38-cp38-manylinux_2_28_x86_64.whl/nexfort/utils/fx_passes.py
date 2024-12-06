
import functools
from typing import List
import torch
from torch._dynamo.utils import detect_fake_mode
from torch.fx.passes.shape_prop import ShapeProp
from nexfort.utils.logging import logger

def run_shape_prop(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:
    fake_mode = detect_fake_mode(example_inputs)
    ShapeProp(gm, fake_mode=fake_mode).propagate(*example_inputs)

def clean_up_graph_after_modifications(gm: torch.fx.GraphModule) -> torch.fx.GraphModule:
    'Runs dead-code elimination, linting, and recompilation for graph, in-place'
    gm.graph.eliminate_dead_code()
    gm.graph.lint()
    gm.recompile()
    return gm

def get_tensor_placeholders(gm: torch.fx.GraphModule) -> List[torch.fx.Node]:
    'Returns placeholder nodes of GraphModule which are torch.Tensor types'
    placeholders = [node for node in gm.graph.nodes if ((node.op == 'placeholder') and isinstance(node.type, type) and issubclass(node.type, torch.Tensor))]
    return placeholders

def skip_pass_if_unavailable(namespace, op):

    def decorator(pass_):

        @functools.wraps(pass_)
        def wrapper(gm, *args, **kwargs):
            if (not hasattr(torch.ops, namespace)):
                logger.debug(f"Skipping {getattr(pass_, '__name__', pass_)} because the required op namespace {namespace} is not available")
                return gm
            if (not hasattr(getattr(torch.ops, namespace), op)):
                logger.debug(f"Skipping {getattr(pass_, '__name__', pass_)} because the required op {namespace}.{op} is not available")
                return gm
            return pass_(gm, *args, **kwargs)
        return wrapper
    return decorator

def skip_pass_if_has_no_call_function(target):

    def decorator(pass_):

        @functools.wraps(pass_)
        def wrapper(gm, *args, **kwargs):
            if (not graph_has_call_function(gm.graph, target)):
                logger.debug(f'Skipping {pass_.__name__} because the required call_function {target} does not exist in the graph')
                return gm
            return pass_(gm, *args, **kwargs)
        return wrapper
    return decorator

def replace_pattern_with_filters(gm, pattern, replacement, *, match_filters=None, ignore_literals=False, name='unknown'):
    replaced_patterns = torch.fx.subgraph_rewriter.replace_pattern_with_filters(gm, pattern, replacement, match_filters=match_filters, ignore_literals=ignore_literals)
    logger.debug(f'Applied {len(replaced_patterns)} matches for {name} pattern replacement')
    if replaced_patterns:
        gm = clean_up_graph_after_modifications(gm)
    return gm

def match_call_function_input_has_users(match, original_graph: torch.fx.Graph, pattern_graph: torch.fx.Graph, *, target, users, index=0) -> bool:
    for node in match.nodes_map.values():
        if ((node.op == 'call_function') and (node.target == target)):
            if (len(node.args) <= index):
                return False
            if (not isinstance(node.args[index], torch.fx.Node)):
                return False
            return (len(node.args[index].users) == users)
    return False

def graph_has_call_function(graph: torch.fx.Graph, target) -> bool:
    if isinstance(target, (list, tuple)):
        if (len(target) == 0):
            return True
        elif (len(target) == 1):
            return graph_has_call_function(graph, target[0])
        elif isinstance(target[0], (list, tuple)):
            return any((graph_has_call_function(graph, t) for t in target))
        targets = set(target)
        for node in graph.nodes:
            if ((node.op == 'call_function') and (node.target in targets)):
                targets.remove(node.target)
                if (not targets):
                    return True
        return False
    else:
        for node in graph.nodes:
            if ((node.op == 'call_function') and (node.target == target)):
                return True
        return False

def get_node_arg(node, idx=0, name=None, default=None):
    if (idx < len(node.args)):
        return node.args[idx]
    if (name is None):
        return default
    return node.kwargs.get(name, default)
