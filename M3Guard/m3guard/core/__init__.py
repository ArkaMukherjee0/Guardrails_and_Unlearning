# m3guard/core/__init__.py

import os
import sys

# Go up TWO levels to reach M3Guard directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from m3guard.core.agent import M3GuardAgent
from m3guard.core.config import M3GuardConfig

__all__ = [
    "M3GuardAgent",
    "M3GuardConfig"
]