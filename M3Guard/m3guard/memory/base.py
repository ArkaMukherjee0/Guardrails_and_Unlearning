# m3guard/memory/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import datetime

class BaseMemory(ABC):
    """Abstract base class for all memory types."""
    
    @abstractmethod
    def store(self, data: Dict[str, Any]) -> bool:
        """Store data in memory."""
        pass
    
    @abstractmethod
    def retrieve(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Retrieve data from memory."""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear memory."""
        pass