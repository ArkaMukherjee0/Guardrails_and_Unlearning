# m3guard/plugins/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dataclasses import dataclass

@dataclass
class PluginResult:
    is_safe: bool
    confidence: float
    reason: Optional[str] = None
    details: Dict[str, Any] = None

class BasePlugin(ABC):
    """Base class for all M3Guard plugins."""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        
    @property
    @abstractmethod
    def plugin_type(self) -> str:
        """Return the type of plugin."""
        pass
        
    @abstractmethod
    async def check(self, 
                   user_input: Dict[str, Any], 
                   target_output: Dict[str, Any]) -> PluginResult:
        """Perform the safety check."""
        pass
    
    def cleanup(self):
        """Optional cleanup method."""
        pass