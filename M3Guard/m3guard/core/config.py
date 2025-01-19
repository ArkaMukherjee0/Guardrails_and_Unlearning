# m3guard/config.py
from dataclasses import dataclass
from typing import List, Dict, Optional
import yaml

@dataclass
class MultimodalConfig:
    enable_image_checks: bool = True
    enable_text_checks: bool = True
    image_check_types: List[str] = None
    text_check_types: List[str] = None

@dataclass
class MemoryConfig:
    episodic_retention: int = 1000
    enable_semantic_patterns: bool = True
    working_memory_window: int = 10
    vector_store_type: str = "faiss"

@dataclass
class M3GuardConfig:
    multimodal: MultimodalConfig
    memory: MemoryConfig
    plugins: Dict[str, Dict]
    autonomous_mode: bool = False
    
    @classmethod
    def from_yaml(cls, config_path: str) -> 'M3GuardConfig':
        with open(config_path, 'r') as f:
            config_dict = yaml.safe_load(f)
            
        multimodal = MultimodalConfig(**config_dict.get('multimodal', {}))
        memory = MemoryConfig(**config_dict.get('memory', {}))
        plugins = config_dict.get('plugins', {})
        
        return cls(
            multimodal=multimodal,
            memory=memory,
            plugins=plugins,
            autonomous_mode=config_dict.get('autonomous_mode', False)
        )

    @classmethod
    def default(cls) -> 'M3GuardConfig':
        return cls(
            multimodal=MultimodalConfig(),
            memory=MemoryConfig(),
            plugins={},
            autonomous_mode=False
        )