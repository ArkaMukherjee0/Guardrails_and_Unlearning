# m3guard/memory/memory_manager.py
from typing import Any, Dict, List, Optional
import os
import sys

# Go up TWO levels to reach M3Guard directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from m3guard.memory.episodic_memory import EpisodicMemory
from m3guard.memory.semantic_memory import SemanticMemory
from m3guard.memory.working_memory import WorkingMemory
from m3guard.core.config import MemoryConfig
import time

class MemoryManager:
    """Orchestrates different types of memory systems."""
    
    def __init__(self, config: MemoryConfig):
        self.config = config
        self.episodic = EpisodicMemory(max_entries=config.episodic_retention)
        self.semantic = SemanticMemory() if config.enable_semantic_patterns else None
        self.working = WorkingMemory(window_size=config.working_memory_window)
        
    def update(
        self,
        user_input: Dict[str, Any],
        target_output: Dict[str, Any],
        safety_result: Dict[str, Any]
    ) -> None:
        """Update all memory systems with new interaction."""
        interaction_data = {
            'interaction': {
                'input': user_input,
                'output': target_output,
                'type': self._determine_interaction_type(user_input)
            },
            'decision': {
                'outcome': safety_result,
                'timestamp': time.time()
            }
        }
        
        # Update all memory systems
        self.episodic.store(interaction_data)
        if self.semantic:
            self.semantic.store(interaction_data)
        self.working.store(interaction_data)
        
    def query_memory(
        self,
        query: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Query all memory systems for relevant information."""
        return {
            'episodic': self.episodic.retrieve(query),
            'semantic': self.semantic.retrieve(query) if self.semantic else None,
            'working': self.working.retrieve(query)
        }
        
    def _determine_interaction_type(self, user_input: Dict[str, Any]) -> str:
        """Determine the type of interaction based on input."""
        if 'image' in user_input and 'text' in user_input:
            return 'multimodal'
        elif 'image' in user_input:
            return 'image'
        return 'text'