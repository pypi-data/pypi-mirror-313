import subprocess
from urllib.parse import quote_plus

import bpkio_cli.utils.prompt as prompt
import click
from bpkio_cli.core.config_provider import CONFIG
from bpkio_cli.core.exceptions import BroadpeakIoCliError
from bpkio_cli.writers.breadcrumbs import display_tip


class StreamPlayer:
    def __init__(self):
        self.config_provider = CONFIG
        self._player_templates = None

    def launch(self, stream_url: str, key: str = None, **kwargs):
        players = self.available_player_templates()

        kwargs["url_encoded"] = quote_plus(stream_url)

        # Check if the key exists
        if key not in players:
            # search for the first one with a partial match
            for k in players.keys():
                if k.lower().startswith(key.lower()):
                    key = k
                    break

        try:
            command_template = players[key]["url"] if key is not None else stream_url
        except KeyError:
            raise BroadpeakIoCliError(
                f"There is no player template in your config file corresponding to key '{key}'"
            )

        if command_template.startswith("http"):
            kwargs["url"] = kwargs.get("url_encoded")
        else:
            kwargs["url"] = stream_url

        try:
            command = command_template.format(**kwargs)
        except KeyError as e:
            key = str(e).strip("'")
            if ":" in key:
                key, default = key.split(":", 1)
                kwargs[key] = default
                command = command_template.format(**kwargs)
            else:
                raise ValueError(
                    f"No value provided for the placeholder '{key}' in the template string."
                )

        # if url starts with http, then it's a URL, and we send it to the browser
        if command.startswith("http"):
            display_tip(f"Browser URL: {command}")
            click.launch(command)
        else:
            # otherwise it's a command, and we send it to the shell
            display_tip(f"Command: {command}")
            process = subprocess.Popen(command, shell=True)

    def available_player_templates(self):
        config_players = self.config_provider.list_players()
        players = dict()
        for key, template in config_players.items():
            t_parts = template.split("||")
            if len(t_parts) == 1:
                players[key] = dict(name=key, label="", url=t_parts[0])
            else:
                players[key] = dict(name=key, label=t_parts[0], url=t_parts[1])
        return players

    @staticmethod
    def prompt_player():
        player = prompt.fuzzy(
            message="What player (or page) do you want to open this resoure in?",
            choices=[
                dict(name=f"{k:<12}  -  {v['label']}", value=k)
                for k, v in StreamPlayer().available_player_templates().items()
            ],
            transformer=lambda x: x.split("  -  ")[0],
            long_instruction="Use `bic config set default-player <label>` to make your choice permanent",
        )
        return player
