from enum import Enum

class SocVersion(int, Enum):
    UnsupportedSocVersion = -1
    Ascend910PremiumA = 100
    Ascend910ProA = 101
    Ascend910A = 102
    Ascend910ProB = 103
    Ascend910B = 104
    Ascend310P1 = 200
    Ascend310P2 = 201
    Ascend310P3 = 202
    Ascend310P4 = 203
    Ascend910B1 = 220
    Ascend910B2 = 221
    Ascend910B2C = 222
    Ascend910B3 = 223
    Ascend910B4 = 224
    Ascend310B1 = 240
    Ascend310B2 = 241
    Ascend310B3 = 242
    Ascend310B4 = 243
    Ascend910C1 = 250
    Ascend910C2 = 251
    Ascend910C3 = 252
    Ascend910C4 = 253
    Ascend910D1 = 260
_SocVersionDict = {'Ascend910PremiumA': SocVersion.Ascend910PremiumA, 'Ascend910ProA': SocVersion.Ascend910ProA, 'Ascend910A': SocVersion.Ascend910A, 'Ascend910ProB': SocVersion.Ascend910ProB, 'Ascend910B': SocVersion.Ascend910B, 'Ascend310P1': SocVersion.Ascend310P1, 'Ascend310P2': SocVersion.Ascend310P2, 'Ascend310P3': SocVersion.Ascend310P3, 'Ascend310P4': SocVersion.Ascend310P4, 'Ascend910B1': SocVersion.Ascend910B1, 'Ascend910B2': SocVersion.Ascend910B2, 'Ascend910B2C': SocVersion.Ascend910B2C, 'Ascend910B3': SocVersion.Ascend910B3, 'Ascend910B4': SocVersion.Ascend910B4, 'Ascend310B1': SocVersion.Ascend310B1, 'Ascend310B2': SocVersion.Ascend310B2, 'Ascend310B3': SocVersion.Ascend310B3, 'Ascend310B4': SocVersion.Ascend310B4, 'Ascend910C1': SocVersion.Ascend910C1, 'Ascend910C2': SocVersion.Ascend910C2, 'Ascend910C3': SocVersion.Ascend910C3, 'Ascend910C4': SocVersion.Ascend910C4, 'Ascend910D1': SocVersion.Ascend910D1}
_SocVersion = None

def get_soc_version():
    global _SocVersion
    if _SocVersion is None:
        import torch_npu
        _SocVersion = _SocVersionDict.get(torch_npu.npu.get_device_name(), SocVersion.UnsupportedSocVersion)
    return _SocVersion