
# Plugin Support for FemtoScale Designs
# Author: Jacob Thomas Messer Redmond and ChatGPT-4o
# UUID: 900100000013

# plugin_support.py

import os
import importlib.util
import logging
from abc import ABC, abstractmethod

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Abstract base class for plugins
class PluginBase(ABC):
    @abstractmethod
    def initialize(self):
        """Initialize the plugin"""
        pass

    @abstractmethod
    def execute(self, data):
        """Execute the plugin's main functionality"""
        pass

    @abstractmethod
    def terminate(self):
        """Terminate the plugin"""
        pass

# Plugin registry
class PluginRegistry:
    def __init__(self):
        self.plugins = {}

    def register(self, plugin_id, plugin_instance):
        if plugin_id in self.plugins:
            raise ValueError(f"Plugin with id {plugin_id} is already registered.")
        self.plugins[plugin_id] = plugin_instance
        logger.info(f"Registered plugin: {plugin_id}")

    def get_plugin(self, plugin_id):
        return self.plugins.get(plugin_id, None)

    def remove_plugin(self, plugin_id):
        if plugin_id in self.plugins:
            del self.plugins[plugin_id]
            logger.info(f"Removed plugin: {plugin_id}")

# Global plugin registry instance
plugin_registry = PluginRegistry()

# Function to load plugins dynamically from a directory
def load_plugins(plugin_dir):
    for filename in os.listdir(plugin_dir):
        if filename.endswith(".py"):
            filepath = os.path.join(plugin_dir, filename)
            spec = importlib.util.spec_from_file_location(filename[:-3], filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)
                if isinstance(attribute, type) and issubclass(attribute, PluginBase) and attribute is not PluginBase:
                    plugin_instance = attribute()
                    plugin_id = filename[:-3]
                    plugin_registry.register(plugin_id, plugin_instance)

# Example plugin
class ExamplePlugin(PluginBase):
    def initialize(self):
        logger.info("Initializing ExamplePlugin")

    def execute(self, data):
        logger.info(f"Executing ExamplePlugin with data: {data}")

    def terminate(self):
        logger.info("Terminating ExamplePlugin")

# Registering and loading the example plugin for demonstration
if __name__ == "__main__":
    example_plugin = ExamplePlugin()
    plugin_registry.register("example_plugin", example_plugin)
    example_plugin.initialize()
    example_plugin.execute({"sample_data": 123})
    example_plugin.terminate()
