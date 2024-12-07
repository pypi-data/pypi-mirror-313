from workflow.utils import PluginManager
from workflow.plugins import install_plugins

global_plugin_manager = PluginManager()
install_plugins(global_plugin_manager)