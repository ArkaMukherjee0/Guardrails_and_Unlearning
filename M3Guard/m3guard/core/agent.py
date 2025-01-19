# m3guard/agent.py
import sys
import os
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from typing import Any, Dict, Optional, Tuple
import logging
from m3guard.plugins.manager import PluginManager
from m3guard.memory.memory_manager import MemoryManager
from m3guard.interface.target_agent import TargetAgentInterface
from m3guard.core.config import M3GuardConfig
from m3guard.core.config import MemoryConfig

class M3GuardAgent:
    def __init__(self, config_path: Optional[str] = None):
        """Initialize M3Guard agent with optional configuration."""
        self.config = (M3GuardConfig.from_yaml(config_path) 
                      if config_path else M3GuardConfig.default())
        
        self.logger = logging.getLogger(__name__)
        
        # Initialize components (these will be implemented later)
        self._init_components()
        
    def _init_components(self):
        """Initialize all major components based on configuration."""
        # These will be fully implemented when we create their respective classes
        self.memory_manager = MemoryManager(MemoryConfig)  # Will be MemoryManager
        self.plugin_manager = PluginManager()  # Will be PluginManager
        self.multimodal_guardian = None  # Will be MultimodalGuardian
        self.target_interface = TargetAgentInterface()  # Will be TargetAgentInterface
        
    async def guard_interaction(
        self,
        target_agent: Any,
        user_input: Dict[str, Any]
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Guard an interaction between user and target agent.
        
        Args:
            target_agent: The target agent to guard
            user_input: Dictionary containing user input (text/images)
            
        Returns:
            Tuple of (is_allowed: bool, response: Dict)
        """
        try:
            # 1. Validate input
            self._validate_input(user_input)
            
            # 2. Get target agent's proposed response
            target_output = await self.target_interface.get_output(
                target_agent, user_input
            )
            
            # 2. Run plugin checks
            plugin_results = await self.plugin_manager.run_checks(
                user_input, target_output
            )
            
            # 3. Update memory
            if self.memory_manager:
                self.memory_manager.update(user_input, target_output, plugin_results)
            
            # 4. Determine if interaction is safe
            is_safe = all(result.is_safe for results in plugin_results.values() 
                         for result in results)
                      
            # 5. Prepare response
            if is_safe:
                return True, {
                    'status': 'allowed',
                    'output': target_output,
                    'confidence': 1.0
                }
            else:
                return False, {
                    'status': 'blocked',
                    'reason': self._aggregate_reasons(plugin_results),
                    'confidence': self._get_max_confidence(plugin_results)
                }
                
        except Exception as e:
            self.logger.error(f"Error in guard_interaction: {str(e)}")
            return False, {
                'status': 'error',
                'reason': str(e),
                'confidence': 1.0
            }

    def _aggregate_reasons(self, plugin_results: Dict) -> str:
        """Aggregate reasons from multiple plugin results."""
        reasons = []
        for plugin_type, results in plugin_results.items():
            for result in results:
                if not result.is_safe and result.reason:
                    reasons.append(result.reason)
        return '; '.join(reasons) if reasons else "Unspecified safety concern"
    
    def _get_max_confidence(self, plugin_results: Dict) -> float:
        """Get maximum confidence from plugin results."""
        confidences = [
            result.confidence
            for results in plugin_results.values()
            for result in results
            if not result.is_safe
        ]
        return max(confidences) if confidences else 1.0
    
    async def _check_safety(
        self,
        user_input: Dict[str, Any],
        target_output: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Perform comprehensive safety checks on the interaction.
        Will be expanded when we implement plugins and multimodal guardian.
        """
        # This is a placeholder until we implement the full checking logic
        return {
            'is_safe': True,
            'reason': None,
            'details': {}
        }

    def _validate_input(self, user_input: Dict[str, Any]):
        """Validate the structure of user input."""
        # Basic validation - will be expanded
        if not isinstance(user_input, dict):
            raise ValueError("User input must be a dictionary")