import importlib.metadata
import json
import os
import subprocess
import sys
import tempfile
import urllib
import zipfile
from datetime import datetime
from urllib.parse import urlparse

import boto3
import click
import cloup
import requests
import tomlkit
from rich.console import Console
from rich.table import Table

from bpkio_cli.click_mods.accepts_plugins_group import (
    AcceptsPluginsGroup,
    retrieve_plugin_commands_by_file,
)
from bpkio_cli.core.config_provider import CONFIG
from bpkio_cli.utils import prompt
from bpkio_cli.writers.breadcrumbs import display_error, display_ok, display_warning

console = Console()


class PluginManifest:
    def __init__(self, manifest_path: str = None):
        self.manifest_path = manifest_path
        if not self.manifest_path:
            raise ValueError("No manifest path provided or found in config.")

        self.manifest = {}
        self.manifest = self.load()

    def load(self) -> dict:
        content = self._load_manifest_from_location(self.manifest_path)
        if content:
            self.manifest = content
        return self.manifest

    def _load_manifest_from_location(self, manifest_location: str) -> dict:
        """
        Loads the manifest from the given path or URL.
        Returns the manifest dictionary if successful, otherwise None.
        """
        if _is_url(manifest_location):
            # manifest is a URL
            try:
                response = requests.get(manifest_location)
                response.raise_for_status()
                manifest = response.json()
                manifest["path"] = manifest_location
                return manifest
            except requests.RequestException:
                return None
            except json.JSONDecodeError:
                return None
        elif _is_s3(manifest_location):
            # manifest is an S3 path
            try:
                s3_bucket, s3_key = manifest_location.split("s3://")[1].split("/", 1)
                s3_client = boto3.client("s3")
                manifest = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)
                # load its content as json
                return json.loads(manifest["Body"].read().decode("utf-8"))
            except Exception as e:
                console.print(f"[bold yellow]Warning: Failed to load manifest from S3: {e}[/bold yellow]")
                return None
        else:
            # manifest is a local file path
            manifest_location = os.path.abspath(manifest_location)

            if not os.path.exists(manifest_location):
                return None
            try:
                with open(manifest_location, "r") as f:
                    self.manifest_path = manifest_location
                    return json.load(f)
            except json.JSONDecodeError:
                return None

    def save(self):
        if _is_url(self.manifest_path):
            raise ValueError("Cannot save manifest to a URL.")
        elif _is_s3(self.manifest_path):
            raise ValueError("Cannot save manifest to an S3 path.")

        manifest_path = os.path.abspath(self.manifest_path)

        # Add metadata
        self.manifest["generated_at"] = datetime.now().isoformat()

        cli_version, git_hash = get_cli_version_and_git_hash()
        self.manifest["cli_version"] = cli_version
        self.manifest["git_hash"] = git_hash

        with open(manifest_path, "w") as f:
            json.dump(self.manifest, f, indent=4)

    def get_plugins(self) -> list[dict]:
        return self.manifest.get("plugins", {})

    def add_plugin(self, plugin_metadata: dict):
        """
        Add or update a plugin in the manifest.
        """
        if "plugins" not in self.manifest:
            self.manifest["plugins"] = {}
        self.manifest["plugins"][plugin_metadata["name"]] = plugin_metadata

    def remove_plugin(self, plugin_name: str):
        if "plugins" in self.manifest:
            self.manifest["plugins"] = {
                p: plugin
                for p, plugin in self.manifest["plugins"].items()
                if p != plugin_name
            }

    def get_plugin(self, plugin_name: str) -> dict:
        if "plugins" in self.manifest:
            return self.manifest["plugins"].get(plugin_name, {})
        return {}


def _is_url(path: str) -> bool:
    return urlparse(path).scheme in ("http", "https")

def _is_s3(path: str) -> bool:
    return path.startswith("s3://")



@cloup.command(
    cls=AcceptsPluginsGroup,
    aliases=["plugin"],
    help="Other functionality provided through addons (plugins)",
)
def plugins():
    pass


@cloup.command(help="List all the available addons", name="list")
def list_plugins():
    display_list_plugins()


def display_list_plugins(cache_buster=False):
    plugins = retrieve_plugin_commands_by_file(cache_buster=cache_buster)

    table = Table()
    table.add_column("file")
    table.add_column("commands")
    for i, (file, commands) in enumerate(plugins.items()):
        inner_table = Table(show_header=(i == 0), show_lines=False)
        inner_table.add_column("name", width=20)
        inner_table.add_column("description", width=80)
        # inner_table.add_column("scopes", width=20)
        for c in commands:
            inner_table.add_row(
                c.name,
                c.help,
                # ", ".join(getattr(c, "scopes", [])),
            )

        table.add_row(
            f"[bold]\n{file}[/bold]",
            inner_table,
        )

    console.print(table)


@cloup.command(help="Install a plugin package")
@cloup.argument("zip_file_path", type=str)
@click.pass_context
def install(ctx, zip_file_path):
    """
    Install a plugin from a zip file path or URL.
    """
    plugin_folder = CONFIG.get("path", section="plugins")

    if _is_url(zip_file_path):
        # Download to a temporary directory
        with tempfile.TemporaryDirectory() as tmp_dir:
            local_zip_path = os.path.join(tmp_dir, "plugin.zip")
            try:
                urllib.request.urlretrieve(zip_file_path, local_zip_path)
                result = extract_and_install(local_zip_path, plugin_folder)
            except Exception as e:
                console.print(
                    f"[bold red]Failed to download plugin from URL: {e}[/bold red]"
                )
                return
    elif _is_s3(zip_file_path):
        # Download from S3
        with tempfile.TemporaryDirectory() as tmp_dir:
            local_zip_path = os.path.join(tmp_dir, "plugin.zip")
            try:    
                s3_bucket, s3_key = zip_file_path.split("s3://")[1].split("/", 1)
                s3_client = boto3.client("s3")
                s3_client.download_file(s3_bucket, s3_key, local_zip_path)
                result = extract_and_install(local_zip_path, plugin_folder)
            except Exception as e:
                console.print(
                    f"[bold red]Failed to download plugin from S3: {e}[/bold red]"
                )
                return
    else:
        if not os.path.exists(zip_file_path):
            console.print(f"[bold red]Plugin file not found at {zip_file_path}[/bold red]")
            return
        result = extract_and_install(zip_file_path, plugin_folder)

    if result is True:
        display_ok(f"Plugin {zip_file_path} installed successfully.")

    # display_list_plugins(cache_buster=True)


def extract_and_install(zip_file_path, plugin_folder):
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(plugin_folder)

    # if there is any corresponding requirements.txt file, install it
    for f in os.listdir(plugin_folder):
        plugin_name = os.path.splitext(os.path.basename(zip_file_path))[0]
        req_filename = f"{plugin_name}.requirements.txt"
        req_path = os.path.join(plugin_folder, req_filename)
        if os.path.exists(req_path):
            subprocess.check_call(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "-r",
                    req_path,
                ]
            )

    return True


@cloup.command(
    help="Package plugin into distributable ZIPs and generate a manifest",
    name="package",
    aliases=["zip"],
)
@cloup.option(
    "--all",
    "preselect_all",
    is_flag=True,
    default=False,
    help="Package all available plugins without prompting for selection.",
)
@cloup.option(
    "--force",
    is_flag=True,
    default=False,
    help="Force re-packaging of plugins even if no changes are detected.",
)
@cloup.option(
    "--name",
    type=str,
    default=None,
    help="Name of the manifest file to package into.",
)
def package_plugins(preselect_all, force, name):
    plugin_folder = CONFIG.get("path", section="plugins")
    package_folder = os.path.join(plugin_folder, "packages")
    if not os.path.exists(package_folder):
        os.makedirs(package_folder)

    if not name:
        manifest_non_admin_path = os.path.join(package_folder, "manifest.json")
        manifest_non_admin = PluginManifest(manifest_non_admin_path)
        manifest_admin_path = os.path.join(package_folder, "manifest-admin.json")
        manifest_admin = PluginManifest(manifest_admin_path)
        target_manifests = [manifest_non_admin, manifest_admin]
    else:
        manifest_file = PluginManifest(os.path.join(package_folder, f"{name}.json"))
        target_manifests = [manifest_file]
    all_local_plugins = retrieve_plugin_commands_by_file()
    all_local_plugins = {k: v for k, v in all_local_plugins.items() if any(getattr(command, "allow_package", True) for command in v)}

    # Keep track of packaged plugins
    packaged_plugins = set()

    selected_plugins = _prompt_for_plugins_to_select(all_local_plugins, preselect_all)
    if not selected_plugins:
        return

    for plugin_file_name in selected_plugins:
        plugin_commands = all_local_plugins[plugin_file_name]
        is_admin = any(
            getattr(command, "admin_only", False) for command in plugin_commands
        )
        plugin_description = next((command.help for command in plugin_commands), "")

        commit_hash, commit_date = get_commit_info(
            plugin_file_name, plugin_folder
        )

        # Determine which manifest to add the plugin to
        if name:
            manifests = target_manifests
        else:
            manifests = (
                [manifest_admin] if is_admin else [manifest_non_admin, manifest_admin]
        )

        proposed_plugin = next(
            (manifest.get_plugin(plugin_file_name) for manifest in manifests), None
        )

        if (
            proposed_plugin
            and proposed_plugin["git_hash"] == commit_hash
            and not force
        ):
            display_ok(
                f"No changes detected for plugin '{plugin_file_name}'. Skipping packaging."
            )
            packaged_plugins.add(plugin_file_name)
            continue

        # Package the plugin
        zip_name, zip_path = create_zip_name_and_path(plugin_file_name, package_folder, commit_hash)

        plugin_metadata = prepare_plugin_metadata(
            plugin_file_name,
            plugin_description,
            zip_name,
            commit_date,
            commit_hash,
        )
        toml_content, toml_filename = create_toml_content(plugin_metadata)

        package_plugin_files(
            plugin_file_name, plugin_folder, zip_path, toml_content, toml_filename
        )

        display_ok(
            f"Plugin '{plugin_file_name}' packaged into {zip_name} with metadata."
        )
        packaged_plugins.add(plugin_file_name)

        # Update manifests
        for manifest in manifests:
            manifest.add_plugin(plugin_metadata)

    # Remove plugins that no longer exist
    for manifest in target_manifests:
        for plugin_name, _ in manifest.get_plugins().items():
            if plugin_name not in all_local_plugins:
                manifest.remove_plugin(plugin_name)
                display_warning(
                f"Plugin '{plugin_name}' has been removed and its entry deleted from the manifest."
            )

    # Save updated manifests
    for manifest in target_manifests:
        try:
            manifest.save()
            display_ok(f"Manifest saved to {manifest.manifest_path}")
        except ValueError:
            console.print(
                "[bold red]Cannot save manifest to a URL. Skipping save operation.[/bold red]"
            )


def _prompt_for_plugins_to_select(plugin_list: list[str], preselect_all: bool):
    if preselect_all:
        if not plugin_list:
            display_ok("No plugins available for packaging.")
            return None
        return plugin_list

    selected_plugins = prompt.select(
        message="Select the plugins to package",
        multiselect=True,
        choices=plugin_list,
        keybindings={"toggle": [{"key": "right"}]},
        long_instruction="Keyboard: right arrow = toggle select/unselect; ctrl+r = toggle all",
    )

    if not selected_plugins:
        display_ok("No plugins selected for packaging.")
        return None

    return selected_plugins


def get_cli_version_and_git_hash():
    try:
        cli_version = importlib.metadata.version("bpkio-cli")
    except importlib.metadata.PackageNotFoundError:
        cli_version = "unknown"

    try:
        git_hash = (
            subprocess.check_output(
                ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
            )
            .decode("utf-8")
            .strip()
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        git_hash = "unknown"

    return cli_version, git_hash


def get_commit_info(plugin_name, plugin_folder):
    plugin_file_path = os.path.join(plugin_folder, f"{plugin_name}.py")
    try:
        commit_info = (
            subprocess.check_output(
                ["git", "log", "-1", "--format=%H|%cI", plugin_file_path],
                stderr=subprocess.DEVNULL,
            )
            .decode("utf-8")
            .strip()
        )
        commit_hash, commit_date = commit_info.split("|")
    except subprocess.CalledProcessError:
        commit_hash = "unknown"
        commit_date = "unknown"
    return commit_hash, commit_date


def prepare_plugin_metadata(
    plugin_name, plugin_description, zip_name, commit_date, commit_hash
):
    return {
        "name": plugin_name,
        "description": plugin_description or "",
        "filename": zip_name,
        "last_modified": commit_date,
        "git_hash": commit_hash,
    }


def create_toml_content(plugin_metadata):
    toml_doc = tomlkit.document()
    toml_doc.add("name", plugin_metadata["name"])
    toml_doc.add("description", plugin_metadata["description"])

    version = tomlkit.table()
    version.add("last_modified", plugin_metadata["last_modified"])
    version.add("git_hash", plugin_metadata["git_hash"])
    toml_doc.add("version", version)
    toml_content = tomlkit.dumps(toml_doc)
    toml_filename = f"{plugin_metadata['name']}.toml"
    return toml_content, toml_filename


def package_plugin_files(
    plugin_name, plugin_folder, zip_path, toml_content, toml_filename
):
    with zipfile.ZipFile(zip_path, "w") as f_out:
        plugin_filename = f"{plugin_name}.py"
        f_out.write(
            os.path.join(plugin_folder, plugin_filename), arcname=plugin_filename
        )

        req_filename = f"{plugin_name}.requirements.txt"
        req_path = os.path.join(plugin_folder, req_filename)
        if os.path.exists(req_path):
            f_out.write(
                req_path,
                arcname=req_filename,
            )

        f_out.writestr(toml_filename, toml_content)


def create_zip_name_and_path(plugin_name, plugin_folder, commit_hash):
    zip_name = f"{plugin_name}_{commit_hash[:7]}.bicplugin"
    zip_path = os.path.join(plugin_folder, zip_name)
    return zip_name, zip_path


@cloup.command(
    help="Discover and install plugins from a manifest file",
    name="discover",
)
@cloup.argument(
    "manifest_path", type=str, required=False, help="Path or URL to the manifest file"
)
@cloup.option(
    "--update-only",
    is_flag=True,
    default=False,
    help="Only suggest plugins that are in need of update.",
)
@click.pass_context
def discover(ctx, manifest_path, update_only):
    """
    Discover and install plugins based on a provided manifest file.
    The manifest can be a local file path or a URL.
    If no path is provided, it uses the stored repository path from the config.
    """
    if not manifest_path:
        manifest_path = CONFIG.get("repo", section="plugins")

    plugin_manifest = PluginManifest(manifest_path)
    manifest = plugin_manifest.load()

    while not manifest:
        manifest_path = prompt.text(
            message=f"Failed to load the manifest from {manifest_path}. Please enter a valid manifest file path or URL:",
        )
        if not manifest_path:
            sys.exit(1)
        plugin_manifest = PluginManifest(manifest_path)
        manifest = plugin_manifest.load()

    # Update the repo path in the config
    CONFIG.set_config("repo", section="plugins", value=plugin_manifest.manifest_path)

    available_plugins = plugin_manifest.get_plugins()
    if not available_plugins:
        display_warning("No plugins found in the manifest.")
        return

    # Directory where local .toml files are stored
    plugin_folder = CONFIG.get("path", section="plugins")

    if not available_plugins:
        display_warning("No plugins found in the manifest.")
        return

    # Prepare choices with pre-selected plugins based on git_hash comparison
    choices = []
    for plugin_name, plugin_info in available_plugins.items():
        toml_path = os.path.join(plugin_folder, f"{plugin_name}.toml")
        local_git_hash = None

        if os.path.exists(toml_path):
            try:
                with open(toml_path, "r") as toml_file:
                    toml_data = tomlkit.load(toml_file)
                    local_git_hash = toml_data.get("version", {}).get("git_hash", "")
            except Exception as e:
                console.print(f"[bold yellow]Warning: Failed to read {toml_path}: {e}[/bold yellow]")

            # Compare git_hash values
            preselect = local_git_hash != plugin_info.get("git_hash", "")
            existing_plugin = True
        else:
            # If the plugin exists, but without toml file, it's an old version and must be updated
            if os.path.exists(os.path.join(plugin_folder, f"{plugin_name}.py")):
                existing_plugin = True
                preselect = True
            else:
                # Not found, it must be new
                existing_plugin = False
                preselect = False

        marker = "[NEW]" if not existing_plugin else "[UPD]" if preselect else "     "

        if update_only and not preselect:
            continue

        choices.append(
            prompt.Choice( 
                name=f"{plugin_name:24s} {marker} - {plugin_info['description']}",
                value=plugin_info,
                enabled=preselect,                
            )
        )

    if update_only and not choices:
        display_ok("No plugins need updating.")
        return

    # Prompt user to select plugins to install/update
    selected_plugins = prompt.checkbox(
        message="Select plugins to install/update:",
        choices=choices,
        keybindings={"toggle": [{"key": "right"}]},
        instruction="Plugins with available updates are pre-selected.",
        long_instruction="Keyboard: right arrow = toggle select/unselect; ctrl+r = toggle all",
        transformer=lambda l: f"{len(l)} plugins selected",
    )

    if not selected_plugins:
        display_warning("No plugins selected for installation/updating.")
        return

    for plugin_info in selected_plugins:
        zip_file = plugin_info.get("filename")
        if not zip_file:
            display_error(
                f"No file path or URL provided for plugin '{plugin_info}'. Skipping."
            )
            continue

        # Location of the zip file is relative to the manifest file
        manifest_dir = os.path.dirname(plugin_manifest.manifest_path)
        if _is_url(plugin_manifest.manifest_path) or _is_s3(plugin_manifest.manifest_path):
            zip_file_path = f"{manifest_dir}/{zip_file}"
        else:
            # absolute path to the local zip file
            zip_file_path = os.path.abspath(os.path.join(manifest_dir, zip_file))

        # Use the existing install command to handle installation
        try:
            install_command = install
            ctx.invoke(install_command, zip_file_path=zip_file_path)
        except Exception as e:
            console.print(
                f"[bold red]Failed to install plugin '{plugin_info}': {e}[/bold red]"
            )
            continue

    console.print(
        "[bold green]Discovery and installation process completed.[/bold green]"
    )


plugins.section(
    "Management of addons", list_plugins, install, package_plugins, discover
)

