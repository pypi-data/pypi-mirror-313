import math
import os
import shutil
import time
from datetime import datetime
from typing import Optional

import click
import media_muncher.handlers as handlers
from bpkio_cli.core.exceptions import BroadpeakIoCliError
from bpkio_cli.monitor.live_monitor import scan_segments, sound_alert
from bpkio_cli.monitor.store import LiveMonitorInfoStore
from bpkio_cli.monitor.timeline import print_mpd_timeline
from bpkio_cli.writers.breadcrumbs import (
    display_bpkio_session_info,
    display_error,
    display_tip,
)
from bpkio_cli.writers.diff import generate_diff
from bpkio_cli.writers.formatter import OutputFormatter
from bpkio_cli.writers.hls_formatter import HLSFormatter
from bpkio_cli.writers.mpd_formatter import MPDFormatter
from bpkio_cli.writers.tables import display_table
from bpkio_cli.writers.xml_formatter import XMLFormatter


# ---- Shared Functions ----
def display_content(
    handler: handlers.ContentHandler,
    max: int,
    interval: int,
    trim: int,
    table: bool = False,
    raw: bool = False,
    diff: bool = False,
    top: int = 0,
    tail: int = 0,
    clear: bool = False,
    header: bool | str = True,
    pager: bool = None,
    silent: bool = True,
    ad_pattern: str = "/bpkio-jitt",
    previous_content: str = None,
    timeline: bool = False,
    **kwargs,
):
    """Fetches the content of the URL associated with ID"""

    terminal_size = shutil.get_terminal_size().lines

    counter = max
    inc_counter = 0

    livemon_store = LiveMonitorInfoStore()

    if interval is None:
        try:
            interval = handler.get_update_interval()
            display_tip(
                f"Update frequency acquired from manifest: {interval} seconds. You can overwrite this with --interval."
            )
        except Exception:
            interval = 4

    try:
        while True:
            displayed = False
            stamp = datetime.utcnow()

            if clear:
                _clear_screen()

            if header:
                if isinstance(header, str):
                    head = header
                    click.echo(head)
                else:
                    head = _make_header(
                        stamp=stamp,
                        url=handler.original_url,
                        counter=inc_counter,
                    )
                    click.secho(head, err=True, fg="white", underline=True)

            # Force fetch of the content
            handler.content
            # Raise status code error if any
            if handler.status is not None and handler.status > 299:
                display_error(f"The document could not get accessed: HTTP status code {handler.status}")
            
            # Some functionality only applies to successful responses            
            else:

                # Table view
                if table and handler:
                    tb1 = handler.extract_info()
                    _show_redirect(handler.url, handler.original_url)
                    if tb1:
                        display_table(tb1)

                    if hasattr(handler, "extract_timeline"):
                        tb2 = handler.extract_timeline()
                        if tb2:
                            display_table(tb2)

                    tb3 = handler.extract_features()
                    if tb3 and len(tb3) == 0:
                        click.secho(
                            "Empty table returned. This is likely because the URL returned an empty response. \n"
                            "Use the `read` command for more",
                            fg="red",
                        )
                    elif tb3 is not None:
                        display_table(tb3)

                    else:
                        raise BroadpeakIoCliError(
                            "No summary functionality implemented for this type of resource"
                        )
                    displayed = True

                # MPEG-DASH Timeline view
                if timeline:
                    if not isinstance(handler, handlers.DASHHandler):
                        display_error(
                            "This command is only implemented with MPEG-DASH content"
                        )
                        return

                    print_mpd_timeline(
                        handler,
                        level=kwargs.get("mpd_level"),
                        selected_period=kwargs.get("mpd_period"),
                        selected_adaptation_set=kwargs.get("mpd_adaptation_set"),
                    )

                    displayed = True

            # Fallback = standard mechanism: show the content itself
            if not displayed:
                content = "No content to display"

                try:
                    match handler:
                        case handlers.DASHHandler():
                            formatter = MPDFormatter(handler=handler)
                            content = formatter.format(
                                "raw" if raw or diff else "standard",
                                top=top,
                                tail=tail,
                                **kwargs,
                            )

                        case handlers.XMLHandler():
                            formatter = XMLFormatter(handler=handler)
                            content = formatter.format(
                                "raw" if raw or diff else "standard",
                                top=top,
                                tail=tail,
                                **kwargs,
                            )

                        case handlers.HLSHandler():
                            formatter = HLSFormatter(handler=handler)
                            formatter.ad_pattern = ad_pattern
                            content = formatter.format(
                                "raw" if raw or diff else "standard",
                                top=top,
                                tail=tail,
                                trim=trim,
                            )
                            if handler.is_live():
                                scan_segments(
                                    handler,
                                    stamp,
                                    store=livemon_store,
                                    ad_pattern=ad_pattern,
                                )
                                changes = livemon_store.changes
                                if changes["added"] and not silent:
                                    sound_alert(changes["added"])
                                    
                except Exception:
                    # Allowing non-parseable content to still be displayed
                    content = handler.content

                _show_redirect(handler.url, handler.original_url)

                display_bpkio_session_info(handler)

                if previous_content and diff:
                    content_to_display = generate_diff(previous_content, content)
                else:
                    content_to_display = content

                # use a pager - including if content is too long to fit on screen
                if pager or (
                    pager is None
                    and len(content_to_display.splitlines()) > terminal_size - 5
                ):
                    # Avoid pager if polling
                    if max != 1 and top == 0 and tail == 0:
                        content_to_display = OutputFormatter.trim(
                            content_to_display,
                            top=math.floor((terminal_size - 5) / 2),
                            tail=math.floor((terminal_size - 5) / 2),
                        )
                        click.echo(content_to_display)
                    else:
                        click.echo_via_pager(content_to_display)
                else:
                    click.echo(content_to_display)

                previous_content = content

            if counter == 1:
                break

            time.sleep(int(interval))
            handler.reload()
            counter = counter - 1
            inc_counter = inc_counter + 1

    except KeyboardInterrupt:
        print("Stopped!")


def _clear_screen():
    cls = lambda: os.system("cls" if os.name == "nt" else "clear")
    cls()


def _make_header(stamp: datetime, url: str, counter: Optional[int]):
    lines = []
    if url:
        lines.append(click.style(url, fg="white", underline=True))

    lines.append(
        click.style(
            "[request{} @ {}]".format(
                " " + str(counter + 1) if counter else "", stamp.isoformat()
            ),
            bg="white",
            fg="black",
        )
    )

    header = "\n".join(lines)
    return header


def _show_redirect(url: str, original_url: str):
    if original_url and original_url != url:
        click.secho(f"  ↪ redirect to {url}", fg="white")
