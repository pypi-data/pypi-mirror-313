
import torch
import triton

def check_torch_meta():
    torch_version = torch.__version__
    if (torch_version == '2.4.0+cu121'):
        return
    else:
        raise Exception(f'''The torch version(torch==2.4.0+cu121) of nexfort's compilation environment conflicts with the current environment(torch=={torch_version})!
 You can handle this exception in one of two ways:
1. Reinstall nextort using the following command: python3 -m pip uninstall nexfort -y && python3 -m pip --no-cache-dir install --pre nexfort -f https://nexfort-whl.oss-cn-beijing.aliyuncs.com/torch{torch_version.split('+')[0]}/{torch_version.split('+')[1]}/
2. Install torch with version 2.4.0+cu121.''')

def check_triton_meta():
    triton_version = triton.__version__
    if (triton_version == '3.0.0'):
        return
    else:
        raise Exception(f"The triton version(triton==3.0.0) of nexfort's compilation environment conflicts with the current environment(triton=={triton_version})! Please install triton with version 3.0.0")
