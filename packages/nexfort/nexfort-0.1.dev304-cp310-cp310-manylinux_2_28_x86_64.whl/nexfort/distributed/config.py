from dataclasses import dataclass, fields
import torch
import torch.distributed as dist
from packaging import version
from .logger import init_logger
logger = init_logger(__name__)
from typing import List, Optional, Union

def check_packages():
    import diffusers
    if not version.parse(diffusers.__version__) > version.parse('0.30.2'):
        raise RuntimeError('This project requires diffusers version > 0.30.2. Currently, you can not install a correct version of diffusers by pip install.Please install it from source code!')

def check_env():
    if version.parse(torch.version.cuda) < version.parse('11.3'):
        raise RuntimeError('NCCL CUDA Graph support requires CUDA 11.3 or above')
    if version.parse(version.parse(torch.__version__).base_version) < version.parse('2.2.0'):
        raise RuntimeError('CUDAGraph with NCCL support requires PyTorch 2.2.0 or above. If it is not released yet, please install nightly built PyTorch with `pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121`')

def is_power_of_2(n: int) -> bool:
    return n & n - 1 == 0 and n != 0

@dataclass
class ModelConfig:
    model: str
    download_dir: Optional[str] = None
    trust_remote_code: bool = False

@dataclass
class RuntimeConfig:
    warmup_steps: int = 1
    dtype: torch.dtype = torch.float16
    use_cuda_graph: bool = False
    use_parallel_vae: bool = False
    use_profiler: bool = False
    use_torch_compile: bool = False
    use_onediff: bool = False

    def __post_init__(self):
        check_packages()
        if self.use_cuda_graph:
            check_env()

@dataclass
class DataParallelConfig:
    dp_degree: int = 1
    use_cfg_parallel: bool = False

    def __post_init__(self):
        assert self.dp_degree >= 1, 'dp_degree must greater than or equal to 1'
        if self.use_cfg_parallel:
            self.cfg_degree = 2
        else:
            self.cfg_degree = 1
        assert self.dp_degree * self.cfg_degree <= dist.get_world_size(), 'dp_degree * cfg_degree must be less than or equal to world_size because of classifier free guidance'
        assert dist.get_world_size() % (self.dp_degree * self.cfg_degree) == 0, 'world_size must be divisible by dp_degree * cfg_degree'

@dataclass
class PipeFusionParallelConfig:
    pp_degree: int = 1
    num_pipeline_patch: Optional[int] = None
    attn_layer_num_for_pp: Optional[List[int]] = (None,)

    def __post_init__(self):
        assert self.pp_degree is not None and self.pp_degree >= 1, 'pipefusion_degree must be set and greater than 1 to use pipefusion'
        assert self.pp_degree <= dist.get_world_size(), 'pipefusion_degree must be less than or equal to world_size'
        if self.num_pipeline_patch is None:
            self.num_pipeline_patch = self.pp_degree
            logger.info(f'Pipeline patch number not set, using default value {self.pp_degree}')
        if self.attn_layer_num_for_pp is not None:
            logger.info(f'attn_layer_num_for_pp set, splitting attention layersto {self.attn_layer_num_for_pp}')
            assert len(self.attn_layer_num_for_pp) == self.pp_degree, 'attn_layer_num_for_pp must have the same length as pp_degree if not None'
        if self.pp_degree == 1 and self.num_pipeline_patch > 1:
            logger.warning('Pipefusion degree is 1, pipeline will not be used,num_pipeline_patch will be ignored')
            self.num_pipeline_patch = 1

@dataclass
class ParallelConfig:
    dp_config: DataParallelConfig
    pp_config: PipeFusionParallelConfig

    def __post_init__(self):
        assert self.dp_config is not None, 'dp_config must be set'
        assert self.pp_config is not None, 'pp_config must be set'
        parallel_world_size = self.dp_config.cfg_degree * self.pp_config.pp_degree
        world_size = dist.get_world_size()
        assert parallel_world_size == world_size, f'parallel_world_size {parallel_world_size} must be equal to world_size {world_size}'
        assert world_size % self.dp_config.cfg_degree == 0, 'world_size must be divisible by cfg_degree'
        assert world_size % self.pp_config.pp_degree == 0, 'world_size must be divisible by pp_degree'
        self.cfg_degree = self.dp_config.cfg_degree
        self.pp_degree = self.pp_config.pp_degree

@dataclass(frozen=True)
class EngineConfig:
    model_config: ModelConfig
    runtime_config: RuntimeConfig
    parallel_config: ParallelConfig

    def to_dict(self):
        """Return the configs as a dictionary, for use in **kwargs."""
        return dict(((field.name, getattr(self, field.name)) for field in fields(self)))

@dataclass
class InputConfig:
    height: int = 1024
    width: int = 1024
    num_frames: int = 49
    use_resolution_binning: bool = (True,)
    batch_size: Optional[int] = None
    prompt: Union[str, List[str]] = ''
    negative_prompt: Union[str, List[str]] = ''
    num_inference_steps: int = 20
    max_sequence_length: int = 256
    seed: int = 42
    output_type: str = 'pil'

    def __post_init__(self):
        if isinstance(self.prompt, list):
            assert len(self.prompt) == len(self.negative_prompt) or len(self.negative_prompt) == 0, 'prompts and negative_prompts must have the same quantities'
            self.batch_size = self.batch_size or len(self.prompt)
        else:
            self.batch_size = self.batch_size or 1
        assert self.output_type in ['pil', 'latent', 'pt'], "output_pil must be either 'pil' or 'latent'"