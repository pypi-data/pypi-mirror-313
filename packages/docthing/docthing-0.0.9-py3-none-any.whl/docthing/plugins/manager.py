# SPDX-License-Identifier: MIT
''' BEGIN FILE DOCUMENTATION (level: 2)
All the methods exposed by a Plugin implementing the `PluginInterface`
should not be called manually. Instead, they should be called by the
`PluginManager` class.

A `PluginManager` is responsible for managing the lifecycle of plugins.
It provides methods to enable and disable plugins, as well as to get a
list of all the enabled plugins.

The `PluginManager` class is intended to be instantiated one for each
_plugin type_. For example, there are currently two types of plugins
in `docthing` currently: [`ExporterPlugin`](@ExporterPlugin)s and
[`MetaInterpreterPlugin`](@MetaInterpreterPlugin)s (which are provided
as abstract classes for implementation).

> Note: if you are planning to add a new plugin to `docthing` which
> implements one of these two interfaces, you should not bother with
> understanding deeply the way the `PluginManager` class works.

Once all plugins are enabled, the `PluginManager` will be able to
let the user iterate over all them to perform some action.
END FILE DOCUMENTATION '''

import os
import importlib.util
import inspect
from typing import Union, List

from .plugin_interface import PluginInterface
from ..util import get_docthing_plugin_dir


class PluginManager:
    def __init__(self, plugin_type, builtin_plugins=[]):
        '''
        Initialize the PluginManager with the specified plugin type.
        '''
        self.plugin_dir = get_docthing_plugin_dir(plugin_type)
        self.plugins = builtin_plugins

    def enable_plugins(self,
                       plugins: Union[str, List[str]] = 'all',
                       configs: dict = {}) -> None:
        '''
        Enable all plugins from the specified directory.

            Args:
                plugins (str or list): The name of a plugin or the list of
                names of the plugins to enable or 'all' to enable all plugins.
                config (dict): The configuration dictionary.
        '''
        if plugins != 'all' and not isinstance(plugins, list):
            if isinstance(plugins, str):
                plugins = [plugins]
            else:
                raise ValueError('Plugins must be a list of plugin names.')

        # Load all plugins from the plugin directory
        for f in self._get_plugins_from_plugin_dir():
            self._load_from_file(os.path.join(self.plugin_dir, f))

        if plugins == 'all':
            for plugin in self.plugins:
                c = {"config": configs.get(plugin.get_name(), {})}
                plugin.enable(**c)
            return

        avail_plugins = [p.get_name() for p in self.plugins]
        unavailable_plugins = [p for p in plugins if p not in avail_plugins]
        if len(unavailable_plugins) > 0:
            print('Warning: some plugins were not found: ' +
                  f'{", ".join(unavailable_plugins)}')

        # Enable the specified plugins
        for plugin in self.plugins:
            if plugin.get_name() in plugins:
                c = {"config": configs.get(plugin.get_name(), {})}
                plugin.enable(**c)

    def _get_plugins_from_plugin_dir(self):
        res = []
        if os.path.isdir(self.plugin_dir):
            for filename in os.listdir(self.plugin_dir):
                if filename.endswith('.py'):
                    res.append(filename)
        return res

    def get_plugins(self):
        '''
        Return the list of enabled plugins.
        '''
        return self.plugins

    def disable_plugins(self):
        '''
        Disable all plugins.
        '''
        for plugin in self.plugins:
            plugin.disable()

    def _load_from_file(self, filepath):
        '''
        Load and verify a single plugin.
        '''
        module_name = os.path.splitext(os.path.basename(filepath))[0]

        # Load the module from file
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Inspect module for classes
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # Check if the class is a subclass of PluginInterface and not the
            # abstract class itself
            if issubclass(obj, PluginInterface) and obj is not PluginInterface:
                print(f'Found plugin: {name}')
                self.plugins.append(obj())  # Instantiate the plugin class
