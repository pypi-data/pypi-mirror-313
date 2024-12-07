def check_torch_version():
    import torch
    torch_version = torch.__version__
    if torch_version == '2.4.0+cu121':
        return
    else:
        raise Exception(f"The torch version(torch==2.4.0+cu121) of nexfort's compilation environment conflicts with the current environment(torch=={torch_version})!\nYou can handle this exception in one of two ways:\n1. Reinstall nextort using one of the following commands:\n   a. For CN users\n      python3 -m pip uninstall nexfort -y && python3 -m pip --no-cache-dir install --pre nexfort -f https://nexfort-whl.oss-cn-beijing.aliyuncs.com/torch{torch_version.split('+')[0]}/{torch_version.split('+')[1]}/\n   b. For NA/EU users\n      python3 -m pip uninstall nexfort -y && python3 -m pip --no-cache-dir install --pre nexfort -f https://github.com/siliconflow/nexfort_releases/releases/expanded_assets/torch{torch_version.split('+')[0]}_{torch_version.split('+')[1]}\n2. Install torch with version 2.4.0+cu121")

def check_triton_version():
    import triton
    triton_version = triton.__version__
    if triton_version == '3.0.0':
        return
    else:
        raise Exception(f"The triton version(triton==3.0.0) of nexfort's compilation environment conflicts with the current environment(triton=={triton_version})! Please install triton with version 3.0.0")