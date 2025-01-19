# m3guard/memory/working_memory.py
from typing import Any, Dict, List, Optional, Deque
from collections import deque
from .base import BaseMemory

class WorkingMemory(BaseMemory):
    """Maintains current context and recent interactions."""
    
    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.recent_interactions = deque(maxlen=window_size)
        self.current_context = {}
        
    def store(self, data: Dict[str, Any]) -> bool:
        """Update working memory with new interaction."""
        self.recent_interactions.append(data)
        self._update_context(data)
        return True
        
    def retrieve(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get current context and recent interactions."""
        return [{
            'current_context': self.current_context,
            'recent_interactions': list(self.recent_interactions)
        }]
    
    def _update_context(self, data: Dict[str, Any]):
        """Update current context based on new interaction."""
        # Update session context
        self.current_context.update({
            'last_interaction_type': data['interaction']['type'],
            'current_user': data['interaction'].get('user'),
            'active_constraints': data.get('constraints', []),
            'recent_violations': self._get_recent_violations()
        })
    
    def _get_recent_violations(self) -> List[Dict[str, Any]]:
        """Get list of recent safety violations."""
        return [
            interaction['decision'] 
            for interaction in self.recent_interactions
            if not interaction['decision']['outcome']['is_safe']
        ]
    
    def clear(self) -> None:
        """Clear working memory."""
        self.recent_interactions.clear()
        self.current_context.clear()