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
@click.command()
def update():
    """Update the application and its dependencies"""
    import subprocess
    import sys

    import requests

    try:
        # Get the current version of the package
        current_version = version('bpkio-cli')

        # Fetch the latest version from PyPI
        response = requests.get('https://pypi.org/pypi/bpkio-cli/json')
        response.raise_for_status()
        latest_version = response.json()['info']['version']

        if latest_version > current_version:
            console.print(f"[yellow]A new version ({latest_version}) is available. Updating...[/yellow]")
            
            # Upgrade the package using pip
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'bpkio-cli'])
            
            console.print(f"[green]Successfully updated to version {latest_version}.[/green]")
        else:
            console.print("[green]You are already using the latest version.[/green]")

    except requests.RequestException as e:
        console.print(f"[red]Failed to fetch the latest version: {e}[/red]")
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Failed to update the package: {e}[/red]")
    except Exception as e:
        console.print(f"[red]An unexpected error occurred: {e}[/red]")
