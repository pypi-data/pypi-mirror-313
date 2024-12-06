# from __future__ import absolute_import

import os

import click
import cloup

import bpkio_cli.commands as commands
from bpkio_cli.click_mods.accepts_plugins_group import AcceptsPluginsGroup
from bpkio_cli.click_mods.accepts_shortcuts import AcceptsShortcutsGroup
from bpkio_cli.click_mods.default_last_command import DefaultLastSubcommandGroup
from bpkio_cli.commands.configure import init
from bpkio_cli.core.config_provider import CONFIG
from bpkio_cli.core.exceptions import UsageError
from bpkio_cli.core.initialize import initialize
from bpkio_cli.core.logging import get_level_names, set_logging_level
from bpkio_cli.writers.breadcrumbs import (
    display_error,
    display_tenant_info,
    display_warning,
)

# Default log level
set_logging_level("ERROR")


SETTINGS = cloup.Context.settings(
    formatter_settings=cloup.HelpFormatter.settings(
        theme=cloup.HelpTheme.dark(), max_width=120
    ),
    help_option_names=["-h", "--help"],
)


class BicTopLevelGroup(DefaultLastSubcommandGroup, AcceptsShortcutsGroup, AcceptsPluginsGroup):
    pass


@cloup.group(
    show_subcommand_aliases=True,
    context_settings=SETTINGS,
    cls=BicTopLevelGroup,
)
@click.version_option(
    package_name="bpkio_cli", prog_name="Command Line helpers for broadpeak.io"
)
@click.option(
    "-t",
    "--tenant",
    help="Label of the tenant profile to impersonate. It must have been added to the local credentials file (for example with the `bic config tenant add`)",
    metavar="<tenant-label>",
)
@click.option(
    "-l",
    "--log-level",
    type=click.Choice(get_level_names()),
    required=False,
    show_default=True,
    help="Set the log level",
)
@click.option(
    "-cc / -nc",
    "--cache / --no-cache",
    "use_cache",
    is_flag=True,
    default=True,
    show_default=True,
    help="Enable or disable resource caches",
)
@click.option(
    "-pp / -np",
    "--prompts / --no-prompts",
    "use_prompts",
    is_flag=True,
    default=True,
    show_default=True,
    help="Enable or disable the use of prompts to ask for some information (where supported)",
)
@click.option(
    "-v",
    "verbose",
    count=True,
    type=int,
    default=None,
    help="Verbosity level. The number of 'v' indicates the level, from -v (lowest) to -vvvv (highest)",
)
@click.option(
    "--safe",
    is_flag=True,
    default=False,
    help="Run in safe mode (no plugins)",
)
@click.pass_context
def bic(ctx, tenant, log_level, use_cache, use_prompts, verbose, safe):
    if log_level:
        set_logging_level(log_level)

    CONFIG.set_temporary("use_prompts", use_prompts)

    if verbose is not None:
        CONFIG.set_temporary("verbose", verbose - 1)

    requires_api = True
    # TODO - move this to the command definition
    if ctx.invoked_subcommand in [
        "init",
        "configure",
        "record",
        "url",
        "archive",
        "memory",
        "doctor",
    ]:
        requires_api = False

    app_context = initialize(
        tenant=tenant,
        use_cache=use_cache,
        requires_api=requires_api,
    )

    if app_context.tenant and ctx.invoked_subcommand not in ["init", "configure"]:
        display_tenant_info(app_context.tenant)

    # TODO - validate the token in the initialisation of BroadpeakApi
    ctx.obj = app_context

    @ctx.call_on_close
    def close_cleanly():
        try:
            # Save the cache to disk
            app_context.cache.save()

            # Save the current command
            with open(".last_command", "w") as f:
                f.write(ctx.invoked_subcommand)

            # Close the local server if it's running
            if app_context.local_server:
                app_context.local_server.stop()

        except Exception:
            pass


def apply_conditional_commands(command_config):
    for section_name, section_commands_definition in command_config.items():
        # Check if the section has a condition
        if (
            "condition" in section_commands_definition
            and section_commands_definition["condition"]()
        ):
            commands = []
            # Commands can have conditions (if they are defined as a dict)
            if isinstance(section_commands_definition["commands"], dict):
                for command, condition in section_commands_definition[
                    "commands"
                ].items():
                    if condition():
                        commands.append(command)
            # Commands can be a list of commands (if they don't have a condition)
            elif isinstance(section_commands_definition["commands"], list):
                commands = section_commands_definition["commands"]
            bic.section(section_name, *commands)


def is_not_mm_only():
    return not os.getenv("BIC_MM_ONLY")


command_config = {
    "Configuration": dict(
        condition=lambda: True,
        commands={
            commands.hello: is_not_mm_only,
            init: lambda: True,  
            commands.configure: lambda: True,
            commands.update: lambda: True,
            commands.doctor: lambda: True,  
        },
    ),
    "Sources": dict(
        condition=is_not_mm_only,
        commands=commands.get_sources_commands(),
    ),
    "Services": dict(
        condition=is_not_mm_only,
        commands=commands.get_services_commands(),
    ),
    "Other resources": dict(
        condition=is_not_mm_only,
        commands=[
            commands.profile,
            commands.get_categories_command(),
            commands.session,
        ],
    ),
    "Media muncher": dict(
        condition=lambda: True,
        commands=[commands.url, commands.archive],
    ),
    "Account resources": dict(
        condition=is_not_mm_only,
        commands=commands.get_users_commands() + [commands.consumption],
    ),
    "Advanced": dict(
        condition=lambda: True,
        commands={
            commands.package: is_not_mm_only,
            commands.record: is_not_mm_only,
            commands.memory: lambda: True,
            commands.plugins: lambda: True,
        },
    ),
    "Updates": dict(
        condition=lambda: True,
        commands=[commands.update],
    ),
}

apply_conditional_commands(command_config)


def safe_entry_point():
    try:
        bic()
    except Exception as e:
        if hasattr(e, "status_code"):
            st = " [{}] ".format(e.status_code)
        else:
            st = ""
        msg = "{}: {}{}".format(e.__class__.__name__, st, e)

        if isinstance(e, UsageError):
            display_warning(msg)
        else:
            display_error(msg)

        if hasattr(e, "original_message") and e.original_message is not None:
            click.secho("  > {}".format(e.original_message), fg="red")


def debug_entry_point():
    set_logging_level("DEBUG", to_file=True)
    bic(obj={})


def mm_only_entry_point():
    bic.shortcut = "url"
    safe_entry_point()


def archive_only_entry_point():
    bic.shortcut = "archive"
    safe_entry_point()


if __name__ == "__main__":
    debug_entry_point()
    # mm_only_entry_point()
