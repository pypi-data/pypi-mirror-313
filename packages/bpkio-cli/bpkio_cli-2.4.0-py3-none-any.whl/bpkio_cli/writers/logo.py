import os

from rich.console import Console

console = Console()


def show_logo():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "logo.txt")

    with open(file_path, "r") as f:
        logo = f.read()

    console.print(logo, highlight=False)
