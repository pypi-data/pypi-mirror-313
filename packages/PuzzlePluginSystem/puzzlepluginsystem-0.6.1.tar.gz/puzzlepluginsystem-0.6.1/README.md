Puzzle Plugin System
=======================

This repo helps implementing a plugin system for Python applications. It uses [setuptools](https://github.com/pypa/setuptools) `entry points` for plugin discovery and [blinker](https://github.com/jek/blinker) `signals` to propagate events between loosely connected components.
Both aspects are strictly separated so you can use the setuptools part without blinker signalling (or the other way around).


Events and Signals (blinker)
--------------------------------

Plugins can "connect" (register) to specific blinker signals. When the main application triggers a signal a subscribed plugin handler is called.

Example application:

```python
# "myapp.plugins" module
from schwarz.puzzle_plugins import SignalRegistry

registry = SignalRegistry()

class AppSignal:
    foo = 'myapp:foo'

# need to trigger plugin registration here (see "Plugin Discovery" section below)

# trigger a signal to call some plugin code and get the returned value
result = registry.call_plugin(AppSignal.foo, signal_kwargs={'a': 137})
```


This is plugin code (e.g. `myplugin.py`):

```python
from schwarz.puzzle_plugins import connect_signals, disconnect_signals
from myapp.plugins import AppSignal

class MyPlugin:
    def __init__(self, registry):
        self._connected_signals = None
        self._registry = registry

    def signal_map(self):
        return {
            AppSignal.foo: handle_foo,
        }


# The main application must call this function on startup.
# See "Plugin Discovery" section on how to do this.
def initialize(context, registry):
    plugin = MyPlugin(registry)
    plugin._connected_signals = connect_signals(plugin.signal_map(), registry)
    context['plugin'] = plugin

def terminate(context):
    plugin = context['plugin']
    disconnect_signals(plugin._connected_signals, plugin._registry)
    plugin._registry = None
    plugin._connected_signals = None


# --- actual plugin functionality -----------------------------------------
def handle_foo(sender, a=21):
    return a * 2
```


### SignalRegistry: triggering plugin functionality

`registry.call_plugins(signal_name, signal_kwargs={…}, expect_single_result=False)` is convenience method to get return values from all plugins registered for the specified signal.

If you pass `expect_single_result=True` this means you still get only a single (scalar) result value. If multiple plugins return a non-`None` value `ValueError` is raised.



Plugin Discovery (setuptools)
--------------------------------

The blinker signalling above requires that plugins subscribe to specific signals before the main application triggers a signal. When all plugins are known while writing the main application you can just insert the right calls in the startup routine and everything will be fine.

However I believe the more common scenario (and usually main motivation to introduce a plugin system) is to *separate* plugins from the main application. For example several customers could use the same base software but different plugins which add customer-specific functionality. In this situation the main application must be able to discover and activate available plugins. This is done with the help of setuptools' `entry points`.


### Example:

Create a separate setuptools-project for your plugin. Add your code (for example as shown in the "Events and Signals" section above).

```python
# file: setup.cfg
[options.entry_points]
myapp.plugins =
    MyPlugin = my_plugin
```

The `my_plugin` module must contain two functions which are called by the main application:

 * `initialize(context, registry)`
 * `terminate(context)`

`context` is just a dict where the plugin can store arbitrary state. The main application will keep the `context` and pass the same instance to `terminate()`.


The main application needs to initialize the plugins at startup. If you use blinker-based signalling you must keep the `plugin_loader` instance during the whole lifetime of the application. When the instance is garbage collected all blinker signal connections will be lost.

```python
from schwarz.puzzle_plugins import parse_list_str, PluginLoader
from myapp.plugins import registry

def initialize_plugins():
    # This string is usually stored in the application config.
    # Use "*" to enable all plugins.
    plugin_config_str = 'MyPlugin, OtherPlugin'
    enabled_plugins = parse_list_str(plugin_config_str)
    plugin_loader = PluginLoader('myapp.plugins', enabled_plugins=enabled_plugins)
    plugin_loader.initialize_plugins(registry)
    return plugin_loader
```

