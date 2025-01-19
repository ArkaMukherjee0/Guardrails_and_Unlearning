# m3guard/__init__.py
# M3GUARD/m3guard/__init__.py
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if project_root not in sys.path:
   sys.path.insert(0, project_root)
#print(project_root)
    
from m3guard.core.agent import M3GuardAgent
from m3guard.core.config import M3GuardConfig
from m3guard.multimodal.guardian import MultimodalGuardian

__version__ = "0.1.0"

__all__ = [
    "M3GuardAgent",
    "M3GuardConfig",
    "MultimodalGuardian"
]