# -*- coding: utf-8 -*-
# The source code in this file is covered by the CC0 v1.0 license.
# full license text: https://creativecommons.org/publicdomain/zero/1.0/
# SPDX-License-Identifier: CC0
# written by: Felix Schwarz (2014, 2015, 2019, 2020)

from __future__ import division, absolute_import, print_function, unicode_literals

from collections import OrderedDict
import logging
import re

import pkg_resources


__all__ = ['parse_list_str', 'PluginLoader']

class PluginLoader(object):
    def __init__(self, entry_point_name, enabled_plugins=('*',), log=None, working_set=None):
        self.entry_point_name = entry_point_name
        self.enabled_plugins = enabled_plugins
        self.log = log or logging.getLogger(__name__)
        self.working_set = working_set or pkg_resources.working_set
        self.activated_plugins = OrderedDict()
        self._plugin_contexts = {}
        self._initialized = False

    def init(self):
        self.activated_plugins = OrderedDict()
        # LATER/enhancement: two-pass initialization, gather all requirements,
        # build a directed acyclic graph and perform a topological sort to load
        # all plugins in the right order (in case plugins depend on each other)
        epoints = tuple(self.working_set.iter_entry_points(self.entry_point_name))
        self.log.debug('%d plugins for entry point "%s" found', len(epoints), self.entry_point_name)
        for epoint in epoints:
            plugin_id = epoint.name
            # LATER: check for duplicate plugin id
            if not self.is_plugin_enabled(plugin_id):
                self.log.debug('Skipping plugin %s: not enabled', self._plugin_info(epoint))
                continue
            self.activated_plugins[plugin_id] = self._plugin_from_entry_point(epoint)
            self.log.debug('Plugin loaded: %s', self._plugin_info(epoint))
        self._initialized = True

    def initialize_plugins(self, *args, **kwargs):
        if not self._initialized:
            self.init()
        for plugin_id, plugin in self.activated_plugins.items():
            context = {}
            plugin.initialize(context, *args, **kwargs)
            self._plugin_contexts[plugin_id] = context

    def terminate_plugin(self, plugin_id):
        plugin = self.activated_plugins[plugin_id]
        context = self._plugin_contexts[plugin_id]
        plugin.terminate(context)
        # TODO: remove from activated_plugins / _plugin_contexts

    def terminate_all_activated_plugins(self):
        for plugin_id in self.activated_plugins:
            self.terminate_plugin(plugin_id)

    def is_plugin_enabled(self, plugin_id):
        return (plugin_id in self.enabled_plugins) or ('*' in self.enabled_plugins)

    def _plugin_info(self, epoint):
        plugin_id = epoint.name
        dist = epoint.dist
        return '%s %s (%r, %s)' % (dist.project_name, dist.version, plugin_id, dist.location)

    def _plugin_from_entry_point(self, epoint):
        # LATER: catch exceptions while loading plugins
        module_or_function = epoint.load()
        if callable(module_or_function):
            plugin = module_or_function()
        else:
            # entry point specification referred to a module.
            plugin = module_or_function
        return plugin



def parse_list_str(setting_str):
    """
    Split a string like 'foo, bar' into ('foo', 'bar').
    Also handles 'irregular' spacing like "foo  ,bar".
    """
    return re.split(r'\s*,\s*', setting_str)

