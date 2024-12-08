from typing import Any, Dict

import pluggy

from congruent.llm import hookspecs


class PluginManager:
    def __init__(self):
        self._pm = pluggy.PluginManager("llm_interface")
        self._pm.add_hookspecs(hookspecs)
        self._plugins: Dict[str, Any] = {}

    def register(self, plugin, name: str):
        self._pm.register(plugin)
        self._plugins[name] = plugin

    def get_plugins(self):
        return self._plugins

    @property
    def hook(self):
        return self._pm.hook

    def register_default_providers(self):
        from congruent.llm.providers import anthropic, openai

        self.register(openai, "openai")
        self.register(anthropic, "anthropic")


pm = PluginManager()
