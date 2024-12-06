from typing import List, Optional
import torch

def get_devices_from_module(module: torch.nn.Module):
    """Returns a list of devices from a module"""
    devices = set()
    for p in module.parameters():
        devices.add(p.device.type)
    return list(devices)

def get_devices_from_graph_module(gm: torch.fx.GraphModule, example_inputs: Optional[List[torch.Tensor]]=None):
    fake_inputs = [node.meta.get('val') for node in gm.graph.nodes if node.op == 'placeholder']
    fake_inputs = [t for t in fake_inputs if isinstance(t, torch.Tensor)]
    devices = {*get_devices_from_tensors([x for x in fake_inputs if isinstance(x, torch.Tensor)]), *get_devices_from_module(gm)}
    if not devices and example_inputs is not None:
        devices = get_devices_from_tensors([x for x in example_inputs if isinstance(x, torch.Tensor)])
    return list(devices)

def get_devices_from_tensors(tensors: List[torch.Tensor]):
    """Returns a list of devices from a list of tensors"""
    devices = set()
    for t in tensors:
        devices.add(t.device.type)
    return list(devices)