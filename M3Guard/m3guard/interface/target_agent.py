# m3guard/interface/target_agent.py
from typing import Any, Dict, Optional
import logging

class TargetAgentInterface:
    """Interface for interacting with target agents."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def get_output(self, 
                        target_agent: Optional[Any], 
                        user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        For benchmark purposes, we'll simulate agent output.
        In production, this would interface with an actual agent.
        """
        try:
            # For benchmarking, we'll just pass through the input
            # since we're testing the guardrail's ability to detect issues
            return {
                'status': 'success',
                'content': user_input,
                'type': 'benchmark'
            }
        except Exception as e:
            self.logger.error(f"Error getting target agent output: {str(e)}")
            raise