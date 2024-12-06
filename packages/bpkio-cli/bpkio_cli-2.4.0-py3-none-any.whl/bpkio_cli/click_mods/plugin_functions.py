from typing import Callable

import click
from bpkio_cli.core.exceptions import BroadpeakIoCliError


def add_shared_function(name: str, fn: Callable):
    fns = click.get_current_context().meta.get("plugin_functions", {})
    fns[name] = fn
    click.get_current_context().meta["plugin_functions"] = fns


def get_shared_function(name: str) -> Callable:
    error_message = (
        f"This functionality relies on the shared function '{name}' which was not found"
    )
    if (
        not hasattr(click.get_current_context(), "meta")
        or "plugin_functions" not in click.get_current_context().meta
    ):
        raise BroadpeakIoCliError(message=error_message)
    fns = click.get_current_context().meta["plugin_functions"]
    if name not in fns:
        raise BroadpeakIoCliError(message=error_message)
    return fns[name]
