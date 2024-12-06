import json

from bpkio_cli.core.config_provider import CONFIG
from bpkio_cli.writers.formatter import OutputFormatter
from pygments import formatters, highlight, lexers


class JSONFormatter(OutputFormatter):
    def __init__(self) -> None:
        super().__init__()

    def format(self, data: object | list, mode="standard") -> str:
        style = CONFIG.get("style", section="pygments")
        with_linenos = CONFIG.get(
            "linenos", section="pygments", cast_type=bool
        )

        return highlight(
            json.dumps(data, indent=3),
            lexers.JsonLexer(),
            formatters.Terminal256Formatter(style=style, linenos=with_linenos),
        )
