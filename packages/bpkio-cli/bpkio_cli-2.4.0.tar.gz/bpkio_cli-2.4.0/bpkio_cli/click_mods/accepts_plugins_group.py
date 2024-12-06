import os
from collections import defaultdict
from functools import cache

import click
import cloup

from bpkio_cli.core.config_provider import CONFIG
from bpkio_cli.core.exceptions import BroadpeakIoCliError
from bpkio_cli.core.logging import logger

PLUGIN_SECTION_NAME = "Plugin commands"
ADMIN_PLUGIN_SECTION_NAME = "🔒 Admin commands"


class InvalidPluginError(BroadpeakIoCliError):
    def __init__(self, message):
        super().__init__(message)


class AcceptsPluginsGroup(cloup.Group):

    def __init__(self, *args, **kwargs):
        self.plugins = {}
        self.plugin_section = cloup.Section(PLUGIN_SECTION_NAME, is_sorted=True)
        self.admin_plugin_section = cloup.Section(
            ADMIN_PLUGIN_SECTION_NAME, is_sorted=True
        )

        super().__init__(*args, **kwargs)

    def _fully_qualified_command_name(self, ctx):
        """Generate an optionally composite command name
        by traversing the chain of commands to the current one
        """
        cmd = ctx.command.name
        if hasattr(ctx, "parent") and ctx.parent is not None:
            if ctx.parent.command.name != "bic":
                cmd = self._fully_qualified_command_name(ctx.parent) + "." + cmd
        return cmd

    def discover_plugins(self, ctx):
        self.plugins = {}

        # Safe mode?  No plugins
        if ctx.params.get("safe") is True:
            logger.debug("Safe mode enabled, skipping plugin discovery")
            return

        candidate_plugins = retrieve_local_plugins()

        for plugin_name, plugin_info in candidate_plugins.items():
            plugin = plugin_info["command"]
            # Validate the scope of the plugin (if defined)
            if hasattr(plugin, "scopes"):
                if not plugin.scopes:
                    plugin.scopes = ["plugins"]

                if (
                    plugin.scopes != ["*"]
                    and self._fully_qualified_command_name(ctx) not in plugin.scopes
                ):
                    continue

            self.plugins[plugin_name] = plugin
            try:
                logger.debug(
                    f"Adding plugin '{plugin_name}' to group '{self.name}', with name {plugin.name}"
                )
                if plugin.admin_only:
                    self.add_command(
                        plugin, plugin.name, section=self.admin_plugin_section
                    )
                else:
                    self.add_command(plugin, plugin.name, section=self.plugin_section)

            except Exception:
                # TODO - somehow we sometimes get duplication of command addition, in particular when using the ApiResourceGroup
                pass

    def get_command(self, ctx, name):
        self.discover_plugins(ctx)

        if name in self.commands.keys():
            return self.commands[name]

    def list_sections(self, ctx):
        self.discover_plugins(ctx)
        sections = super().list_sections(ctx)
        return sections


def _load_plugin_from_file(filename) -> list[click.Command]:
    ns = {}
    plugin_commands = []

    plugin_folder = CONFIG.get("path", section="plugins")
    fn = os.path.join(plugin_folder, filename)
    with open(fn) as f:
        try:
            code = compile(f.read(), fn, "exec")
            eval(code, ns, ns)
        except ImportError as e:
            raise InvalidPluginError(f"Error loading plugin {filename}: {e}")

    # find all plugin commands from the file
    for k, v in ns.items():
        if isinstance(v, click.Command):
            plugin_commands.append(v)

    if not plugin_commands:
        raise InvalidPluginError(f"No plugin command found in {filename}")

    return plugin_commands


@cache
def retrieve_local_plugins(cache_buster=False) -> dict[str, click.Command]:
    candidate_plugins = {}
    plugin_folder = CONFIG.get("path", section="plugins")
    if not os.path.isdir(plugin_folder):
        logger.warning(
            f"Plugin folder {plugin_folder} does not exist",
        )
        return candidate_plugins

    for filename in os.listdir(plugin_folder):
        if filename.endswith(".py") and filename != "__init__.py":
            logger.debug(f"Loading plugin {filename}")
            try:
                plugin_commands = _load_plugin_from_file(filename)
            except InvalidPluginError as e:
                logger.error(f"Plugin {filename} cannot be loaded and is ignored: {e}")
                continue

            for command in plugin_commands:
                if command.name in candidate_plugins:
                    logger.warning(
                        f"Duplicate plugin command '{command.name}' found in {filename}. Overwriting the original one"
                    )
                candidate_plugins[f"{filename}:{command.name}"] = dict(
                    command=command, file=filename[:-3]
                )

    return candidate_plugins


def retrieve_plugin_commands_by_file(cache_buster=False) -> dict[str, dict]:
    plugins = retrieve_local_plugins(cache_buster=cache_buster)
    plugins_by_file = defaultdict(list)

    for item in plugins.values():
        plugins_by_file[item["file"]].append(item["command"])
    return plugins_by_file
