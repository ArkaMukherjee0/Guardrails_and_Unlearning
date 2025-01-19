# m3guard/plugins/utils.py
from typing import List, Dict, Any
from .base import PluginResult

def aggregate_plugin_results(results: Dict[str, List[PluginResult]]) -> bool:
    """Aggregate results from multiple plugins."""
    is_safe = True
    reasons = []
    
    for plugin_type, plugin_results in results.items():
        for result in plugin_results:
            if not result.is_safe and result.confidence > 0.5:  # Configurable threshold
                is_safe = False
                if result.reason:
                    reasons.append(result.reason)
                    
    return is_safe, reasons

def get_highest_confidence_result(results: List[PluginResult]) -> PluginResult:
    """Get the result with highest confidence."""
    return max(results, key=lambda x: x.confidence)