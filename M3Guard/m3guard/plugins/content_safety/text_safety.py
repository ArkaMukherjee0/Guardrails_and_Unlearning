# m3guard/plugins/content_safety/text_safety.py
from typing import Any, Dict, Optional
from ..base import BasePlugin, PluginResult
import re

class TextSafetyPlugin(BasePlugin):
    """Basic text content safety checker."""
    
    @property
    def plugin_type(self) -> str:
        return "content_safety"
    
    async def check(self, user_input: Dict[str, Any], target_output: Dict[str, Any]) -> PluginResult:
        # Check text content in both input and output
        text_to_check = []
        if 'text' in user_input:
            text_to_check.append(user_input['text'])
        if 'text' in target_output:
            text_to_check.append(target_output['text'])
            
        # Perform safety checks
        for text in text_to_check:
            # Implement your text safety checks here
            if self._contains_unsafe_content(text):
                return PluginResult(
                    is_safe=False,
                    confidence=0.9,
                    reason="Unsafe content detected",
                    details={"text": text}
                )
                
        return PluginResult(is_safe=True, confidence=1.0)
    
    def _contains_unsafe_content(self, text: str) -> bool:
        # Implement your safety checking logic here
        return False