# m3guard/constants.py
from enum import Enum

class ContentType(Enum):
    TEXT = "text"
    IMAGE = "image"
    MULTIMODAL = "multimodal"

class GuardStatus(Enum):
    ALLOWED = "allowed"
    BLOCKED = "blocked"
    ERROR = "error"

class MemoryType(Enum):
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    WORKING = "working"