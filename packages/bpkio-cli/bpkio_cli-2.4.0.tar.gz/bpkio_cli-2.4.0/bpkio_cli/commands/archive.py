import base64
import functools
import json
import urllib.parse
from dataclasses import dataclass
from datetime import datetime
from pathlib import PosixPath
from typing import Dict, Optional

import bpkio_cli.click_options as bic_options
import bpkio_cli.utils.prompt as prompt
import click
import cloup
from bpkio_api.models import MediaFormat
from bpkio_cli.click_mods.resource_commands import ARG_TO_IGNORE, ResourceGroup
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.exceptions import BroadpeakIoCliError
from bpkio_cli.writers.content_display import display_content
from haralyzer import HarEntry, HarParser
from media_muncher.handlers.hls import HLSHandler
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from pydantic import FilePath, parse_obj_as
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


# Group: URLs
@cloup.group(
    cls=ResourceGroup,
    help="Explore archive files, such as HAR captures",
    resource_type=PosixPath,  # TODO - Make this a specific type, to allow finding it in the cache and avoid conflict with other possible commands
)
@cloup.argument(
    "archive_path", help=("The local file to work with"), metavar="<archive-file>"
)
@click.pass_obj
def archive(obj: AppContext, archive_path: str):
    if archive_path and archive_path != ARG_TO_IGNORE:

        if archive_path == "$":
            archive_path = obj.current_resource
        archive = parse_obj_as(FilePath, archive_path)
        obj.resource_chain.add_resource(archive_path, archive)
        obj.cache.record(archive)


# --- INFO Commmand
@archive.command(
    aliases=["content"],
    help="Get detailed information about the content of the archive",
)
@click.pass_obj
def info(obj: AppContext):
    file_path = obj.current_resource

    console = Console()
    analyser = HarAnalyser(file_path)

    # Extract unique manifests
    manifests = analyser.get_manifests()
    (start, end) = analyser.get_time_range()
    console.print(
        f"Archive contains entries from {start.isoformat()} to {end.isoformat()}",
        highlight=False,
    )

    table = Table(title="Archive manifests")
    table.add_column("Index")
    table.add_column("First occurrence")
    table.add_column("Entries")
    table.add_column("URL")
    for i, manifest in enumerate(manifests.values()):
        table.add_row(
            str(i),
            manifest.start.isoformat(),
            str(manifest.count),
            manifest.url,
        )

    console.print(table)


# --- READ Command
@archive.command(
    help="Browse and display entries for manifests in the archive",
)
@bic_options.read
@bic_options.poll
@click.option(
    "--match",
    type=str,
    default=None,
    help="Filter the list of manifests in the archive to those matching a particular sub-string",
)
@click.pass_obj
def read(
    obj: AppContext,
    match,
    raw,
    top,
    tail,
    trim,
    ad_pattern,
    pager,
    diff,
    clear,
    silent,
    **kwargs,
):
    file_path = obj.current_resource

    analyser = HarAnalyser(file_path)

    # Extract unique manifests
    manifests = analyser.get_manifests(partial_url=match)

    if len(manifests) == 0:
        if match:
            raise BroadpeakIoCliError("No matching manifests found in archive")
        else:
            raise BroadpeakIoCliError("No manifests found in archive")

    # Ask what manifest to read
    selected_manifest_url = prompt.fuzzy(
        message="Select a manifest to read",
        choices=[
            prompt.Choice(
                manifest.url, name=f"({manifest.count} entries) {manifest.url}"
            )
            for manifest in manifests.values()
        ],
    )
    selected_manifest = manifests[selected_manifest_url]

    entries = analyser.get_entries_for_manifest(selected_manifest)
    first_index = 0
    if entries:
        first_index = prompt.select(
            message="Select a first entry to read",
            choices=[
                prompt.Choice(i, name=f"({entry.response.status}) {entry.startTime}")
                for i, entry in enumerate(entries)
            ],
        )

    display_content_fn = functools.partial(
        display_content,
        raw=raw,
        top=top,
        tail=tail,
        trim=trim,
        ad_pattern=ad_pattern,
        pager=pager,
        clear=clear,
        silent=silent,
        max=1,  # required but unused
        interval=0,  # required but unused
    )

    display_entry_fn = functools.partial(
        display_entry,
        analyser=analyser,
        manifest=selected_manifest,
        display_content_fn=display_content_fn,
    )

    (bindings, key_labels) = setup_keybindings(
        max=len(entries),
        index=[first_index],
        display_entry_fn=display_entry_fn,
        initial_diff_mode=diff,
    )
    session = PromptSession(key_bindings=bindings)

    display_entry_fn(index=first_index, diff_mode=diff)
    print_key_labels(key_labels)
    session.prompt()


@dataclass
class HarAnalyserManifest:
    url: str
    start: datetime
    count: int = 1

    @property
    def session_id(self) -> str | None:
        parsed_url = urllib.parse.urlparse(self.url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        return query_params.get("bpkio_sessionid", [None])[0]

    @property
    def service_id(self) -> str | None:
        parsed_url = urllib.parse.urlparse(self.url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        return query_params.get("bpkio_serviceid", [None])[0]

    @property
    def format(self) -> MediaFormat:
        return MediaFormat.guess_from_url(self.url)

    def update(self, start: datetime):
        if start < self.start:
            self.start = start
        self.count += 1


class HarAnalyser:
    def __init__(self, path) -> None:
        self._file_path = path

        self.parser: HarParser = None
        try:
            with open(
                self._file_path,
                "r",
            ) as file:
                self.parser = HarParser(json.loads(file.read()))

        except Exception as e:
            raise BroadpeakIoCliError(f"Could not parse HAR file: {e}")

    def get_manifests(
        self, partial_url: Optional[str] = None
    ) -> Dict[str, HarAnalyserManifest]:
        manifests = {}
        for page in self.parser.pages:
            for entry in page.entries:
                if any(s in entry.request.url for s in (".m3u8", ".mpd")):
                    if entry.response.status < 200:
                        continue
                    if partial_url and partial_url not in entry.request.url:
                        continue

                    if entry.request.url not in manifests:
                        manifests[entry.request.url] = HarAnalyserManifest(
                            url=entry.request.url,
                            start=entry.startTime,
                        )
                    else:
                        manifests[entry.request.url].update(entry.startTime)

        return manifests

    def get_time_range(self):
        start = None
        end = None
        for page in self.parser.pages:
            for entry in page.entries:
                if start is None or entry.startTime < start:
                    start = entry.startTime
                if end is None or entry.startTime > end:
                    end = entry.startTime

        return (start, end)

    def get_entries_for_manifest(self, manifest: HarAnalyserManifest):
        result = []
        for page in self.parser.pages:
            result.extend(
                [entry for entry in page.entries if entry.request.url == manifest.url]
            )
        return result

    def get_entry_text(self, entry: HarEntry) -> bytes:
        try:
            text = entry.response.text
            if entry.response.textEncoding == "base64":
                text = base64.b64decode(entry.response.text)
        except KeyError:
            text = "This entry has no content".encode()

        return text

    def get_handler(self, manifest: HarAnalyserManifest, entry: HarEntry):
        if manifest.format == MediaFormat.HLS:
            return HLSHandler(entry.request.url, self.get_entry_text(entry))


def display_entry(
    analyser: HarAnalyser,
    manifest: HarAnalyserManifest,
    display_content_fn,
    index,
    diff_mode,
):
    entries = analyser.get_entries_for_manifest(manifest)
    entry = entries[index]

    handler = analyser.get_handler(manifest, entry)
    if index > 0:
        prev_handler = analyser.get_handler(manifest, entries[index - 1])
        prev_content = prev_handler.content
    else:
        prev_content = None

    # add a header
    panel = Panel(
        f"{manifest.url}\n - status: {entry.response.status}",
        title=f"Request {index+1}/{len(entries)} @ {entry.startTime}",
    )
    with console.capture() as capture:
        console.print(panel)
    header = capture.get()

    # display content
    display_content_fn(
        handler=handler, previous_content=prev_content, header=header, diff=diff_mode
    )


def setup_keybindings(
    display_entry_fn, max, index=[0], initial_diff_mode=True
):  # mutable container to change non-locally
    bindings = KeyBindings()
    diff_mode = initial_diff_mode

    # Define functions for each valid key
    def next_entry(event):
        """Go to the next entry."""
        if index[0] < max - 1:
            index[0] += 1
            display_entry_fn(index=index[0], diff_mode=diff_mode)
        else:
            console.print(
                "[bright_black] --- End of entries.",
            )

    def previous_entry(event):
        """Go to the previous entry."""
        if index[0] > 0:
            index[0] -= 1
            display_entry_fn(index=index[0], diff_mode=diff_mode)
        else:
            console.print("[bright_black] --- Start of entries.")

    def toggle_mode(event):
        """Toggle between diff and normal mode."""
        nonlocal diff_mode
        diff_mode = not diff_mode
        display_entry_fn(index=index[0], diff_mode=diff_mode)

    def stop_application(event):
        event.app.exit()

    key_maps = {
        "n": dict(label="Next entry", fn=next_entry),
        "p": dict(label="Previous entry", fn=previous_entry),
        "s": dict(label="Stop", fn=stop_application, alt=["q"]),
        "d": dict(label="Toggle diff mode", fn=toggle_mode),
    }
    key_labels = {}

    # Bind specific keys to functions
    for key, mapping in key_maps.items():
        bindings.add(key)(mapping["fn"])

        if "alt" in mapping:
            for alt in mapping["alt"]:
                bindings.add(alt)(mapping["fn"])
                key = key + ", " + alt
        key_labels[key] = mapping["label"]

    # Default behavior for all other keys
    @bindings.add("<any>")
    def _(event):
        # Check if the key is one of our specified keys before printing the invalid message
        if event.data not in key_maps.keys():
            if event.data != "?":
                console.print(f"[red]Invalid key: {event.data}")
            print_key_labels(key_labels)

    return bindings, key_labels


def print_key_labels(key_labels):
    elements = ["Keys: "]
    for key, label in key_labels.items():
        elements.append(f"[magenta]\[{key}] [white]{label}")

    columns = Columns(elements, padding=(2, 2))
    console.print(Panel(columns))

    # table = Table(show_header=False, header_style="bold magenta")
    # table.add_column("Key")
    # table.add_column("Label")
    # for key, label in key_labels.items():
    #     table.add_row(key, label)
    # console.print(table)
