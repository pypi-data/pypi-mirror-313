import os
from importlib.metadata import version
from importlib.util import find_spec

import click
from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text

from bpkio_cli.core.app_context import AppContext

console = Console()

# Command: DOCTOR
@click.command(hidden=True)
@click.pass_obj
def doctor(obj: AppContext):
    print()
    # Module check
    texts = []
    for module_name, module in {
        "bpkio_cli": "bpkio_cli",
        "bpkio_python_sdk": "bpkio_api",
        "media_muncher": "media_muncher",
    }.items():
        module_spec = find_spec(module)
        texts.append(
            Text.from_markup(f"[bold]{module_name}[/bold] - version: [bold blue]{version(module_name)}[/bold blue] \n -> [magenta]{module_spec.origin}[/magenta]")
        )

    module_panel = Panel(Group(*texts), title="Installed modules", expand=False, border_style="green", title_align="left")
    console.print(module_panel)

    # Mode check
    admin_texts = []
    try:
        module_spec = find_spec("bpkio_api_admin")
        admin_text = Text.from_markup(
            f"[bold]bpkio-python-sdk-admin[/bold] - version: [bold blue]{version('bpkio_python_sdk_admin')}[/bold blue] \n -> [magenta]{module_spec.origin}[/magenta]"
        )
        admin_texts.append(admin_text)
        admin_panel = Panel(Group(*admin_texts), title="Admin mode", expand=False, border_style="red", title_align="left")
        console.print(admin_panel)
    except Exception as e:
        console.print(
            Panel(
                "Running at standard level",
                width=80,
                border_style="green",
                title_align="left",
            )
        )

    if os.environ.get("BIC_MM_ONLY"):
        console.print(
            Panel("Running in Media Muncher only mode", width=80, border_style="yellow", title_align="left")
            )
    
