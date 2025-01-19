# m3guard/plugins/manager.py
from typing import Dict, List, Type, Any
import importlib
import logging
from .base import BasePlugin, PluginResult

class PluginManager:
    """Manages the plugin ecosystem for M3Guard."""
    
    def __init__(self):
        self.plugins: Dict[str, List[BasePlugin]] = {}
        self.logger = logging.getLogger(__name__)
        
    def register_plugin(self, plugin: BasePlugin) -> bool:
        """Register a new plugin."""
        try:
            plugin_type = plugin.plugin_type
            if plugin_type not in self.plugins:
                self.plugins[plugin_type] = []
            self.plugins[plugin_type].append(plugin)
            self.logger.info(f"Registered plugin: {plugin.__class__.__name__}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register plugin: {str(e)}")
            return False
            
    def load_plugin_from_path(self, plugin_path: str, config: Dict[str, Any] = None) -> bool:
        """Load a plugin from a Python path."""
        try:
            module_path, class_name = plugin_path.rsplit('.', 1)
            module = importlib.import_module(module_path)
            plugin_class = getattr(module, class_name)
            plugin = plugin_class(config)
            return self.register_plugin(plugin)
        except Exception as e:
            self.logger.error(f"Failed to load plugin from {plugin_path}: {str(e)}")
            return False
            
    async def run_checks(self, 
                        user_input: Dict[str, Any], 
                        target_output: Dict[str, Any]) -> Dict[str, List[PluginResult]]:
        """Run all registered plugins."""
        results = {}
        
        for plugin_type, plugins in self.plugins.items():
            results[plugin_type] = []
            for plugin in plugins:
                try:
                    result = await plugin.check(user_input, target_output)
                    results[plugin_type].append(result)
                except Exception as e:
                    self.logger.error(f"Plugin {plugin.__class__.__name__} failed: {str(e)}")
                    
        return results
    
    def get_plugins_by_type(self, plugin_type: str) -> List[BasePlugin]:
        """Get all plugins of a specific type."""
        return self.plugins.get(plugin_type, [])