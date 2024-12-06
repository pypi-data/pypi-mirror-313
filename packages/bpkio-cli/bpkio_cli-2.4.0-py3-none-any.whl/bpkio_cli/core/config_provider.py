import configparser
import os
from typing import Any, Dict


class ConfigProvider:
    def __init__(self, config_path="~/.bpkio/cli.cfg"):
        self.config_path = os.path.expanduser(config_path)
        self.config = configparser.ConfigParser()
        self.temporary = dict()  # For temporary or overrides values
        self.initialize()

    def initialize(self):
        default_values = {
            "settings": {
                "default-player": "CHOICE",
                "editor": "vim",
                "verbose": "2",
                "user-agent": "chrome",
                "table-format": "psql",  # can be any of the formats supported by the tabulate package
                "verify-ssl": "true",
            },
            "pygments": {"style": "monokai", "linenos": "0"},
            "players": {
                "browser": "{url}",
                "ridgeline": "Ridgeline Demo Player||http://demo.ridgeline.fr/index.html?url1={url}&title1={name}&autoplay=true",
                "hlsjs": "Public test player from HLS.js||https://hlsjs.video-dev.org/demo/?src={url}",
                "dashjs": "dashjs = Public test player from DASH.js||https://reference.dashif.org/dash.js/nightly/samples/dash-if-reference-player/index.html?mpd={url}&autoLoad=true",
                "ffplay": 'FFmpeg player||ffplay "{url}"',
            },
            "user-agents": {
                "chrome": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
                "safari": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
            },
            "monitor": {
                "segment-map-size": "10,20",
                "bkml-ad-metadata": "adid",
                "max-frames": "3",
                "image-processor": "chafa",
            },
            "plugins": {
                "path": "~/.bpkio/plugins",
                "repo": "",
            },
        }

        if not os.path.exists(self.config_path):
            self.config.read_dict(default_values)
            self.save_config()
        else:
            self.config.read(self.config_path)

            for section, values in default_values.items():
                self.add_section(section, values)

    def get(self, key, cast_type=None, section="settings"):
        if key in self.temporary:
            value = self.temporary[key]
        else:
            value = self.config.get(section, key)

        return self.cast_value(value, cast_type)

    def cast_value(self, value, cast_type):
        if cast_type is None:
            return value
        elif cast_type == bool:
            return value.lower() in {"true", "1"}
        elif cast_type == int:
            return int(value)
        elif cast_type.__class__.__name__ == "Type":
            return cast_type(value)
        elif getattr(cast_type, "__origin__", None) == list:
            item_type = cast_type.__args__[0]
            return [item_type(item.strip()) for item in value.split(",")]
        elif cast_type == "bool_or_str":
            if value.lower() in {"true", "1"}:
                return True
            if value.lower() in {"false", "0"}:
                return False
            else:
                return value.strip()
        else:
            raise ValueError(f"Unsupported cast_type: {cast_type}")

    def get_section_items(self, section: str) -> Dict[str, Any]:
        if section not in self.config.sections():
            raise ValueError(
                f"The [{section}] section is missing in the configuration file."
            )

        return {key: value for key, value in self.config.items(section)}

    def add_section(self, section_name, default_values):
        if section_name not in self.config:
            self.config.add_section(section_name)

        for key, value in default_values.items():
            if key not in self.config[section_name]:
                self._set(key, value, section_name)

    def _set(self, key, value, section="settings"):
        self.config.set(section, key, value)
        self.save_config()

    def set_config(self, key, value, section=None):
        if section is not None:
            if section not in self.config.sections():
                raise ValueError(f"There is no config section named {section}.")
            else:
                self._set(key, value, section)
                return

        # Fallback: "best effort"
        match key:
            case "player":
                self.set_player(value)
            case _:
                if key in self.config["settings"]:
                    self._set(key, value)
                    return
                else:
                    for section in self.config.sections():
                        if key in self.config[section]:
                            self._set(key, value, section)
                            return
                    raise ValueError(f"There is no setting called '{key}'.")

    def set_temporary(self, key, value):
        self.temporary[key] = value

    def save_config(self):
        # Create all folders first
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, "w") as config_file:
            self.config.write(config_file)

    # --- Specific config parameters ---

    def set_player(self, value):
        if value in self.config["players"]:
            self._set("default-player", value)
        else:
            raise ValueError("The specified player is not in the [players] section.")

    def add_player(self, label, player_string):
        self.config.set("players", label, player_string)
        self.save_config()

    def list_players(self) -> Dict[str, Any]:
        return self.get_section_items("players")

    def get_user_agent(self, label=None):
        if not label:
            label = self.get("user-agent")
        if label not in self.config["user-agents"]:
            # allows passing a user-agent string directly
            return label

        return self.get(label, section="user-agents")

    def list_user_agents(self) -> Dict[str, Any]:
        return self.get_section_items("user-agents")

    # --- For plugins to register their own stuff ---

    def add_plugin_section(self, section_name, default_values):
        self.add_section(section_name, default_values)


CONFIG = ConfigProvider()
