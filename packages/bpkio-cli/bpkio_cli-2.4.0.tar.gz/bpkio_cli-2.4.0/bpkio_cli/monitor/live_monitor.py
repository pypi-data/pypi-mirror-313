import functools
import time
from collections import deque
from copy import copy
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Tuple

import bpkio_cli.utils.sounds as sounds
import click
import progressbar
from bpkio_cli.core.config_provider import CONFIG
from bpkio_cli.core.output_store import OutputStore
from bpkio_cli.monitor.bk_ml import BkMlAdInfoStore
from bpkio_cli.monitor.frame_extract import FrameExtractor
from bpkio_cli.monitor.hls_segment_map import SYMBOLS
from bpkio_cli.monitor.store import (LiveMonitorInfoStore, LiveSignal,
                                     SegmentMapRecord, SignalEventStatus,
                                     SignalEventType, SignalType)
from bpkio_cli.utils.datetimes import (format_datetime_with_milliseconds,
                                       format_timedelta)
from bpkio_cli.writers.breadcrumbs import (display_bpkio_session_info,
                                           display_tip)
from bpkio_cli.writers.colorizer import Colorizer as CL
from bpkio_cli.writers.colorizer import (trim_or_pad, trim_or_pad_plus,
                                         visible_length)
from bpkio_cli.writers.hls_formatter import HLSFormatter
from bpkio_cli.writers.scte35 import summarize
from media_muncher.handlers.hls import HLSHandler


# Function to find the maximum number of lines in any string in the dictionary
def monitor_hls(
    handler: HLSHandler,
    max: int,
    interval: int,
    silent: bool,
    ad_pattern: str,
    name: Optional[str] = None,
    save_to_file: bool = False,
    with_schedule: bool = False,
    with_signals: bool = True,
    with_map: bool = True,
    with_adinfo: bool = True,
    with_frames: bool = False,
):
    # Go through the HLS document and retrieve segments with specific markers
    click.secho("Limitations:", fg="yellow")
    click.secho(
        "- this feature only monitors the first rendition in the multi-variant playlist",
        fg="yellow",
    )
    click.secho("- this feature will only work with specific SCTE markers", fg="yellow")
    print()

    bar = progressbar.ProgressBar(
        widgets=[
            CL.high1("---[ "),
            CL.node(name),
            CL.high1(" ]--[ "),
            progressbar.RotatingMarker(),
            CL.high1(" ]--[ "),
            progressbar.Counter(),
            CL.high1(" @ "),
            progressbar.Variable(name="time", format="{formatted_value}"),
            CL.high1(" ]--[ "),
            "HLS media sequence: ",
            progressbar.Variable(name="sequence", format="{value}"),
            CL.high1(" ]---"),
        ],
        redirect_stdout=True,
        max_value=progressbar.UnknownLength,
    )

    livemon_store = LiveMonitorInfoStore()
    counter = max
    inc_counter = 0
    rolling_num_segments = deque(maxlen=10)
    rolling_duration = deque(maxlen=10)
    last_handler = None

    bkml_handler = BkMlAdInfoStore(handler)

    if interval is None:
        try:
            interval = handler.get_update_interval()
            display_tip(
                f"Update frequency acquired from manifest: {interval} seconds. You can overwrite this with --interval."
            )
        except Exception as e:
            interval = 4

    display_bpkio_session_info(handler)

    try:
        while True:
            stamp = datetime.now(timezone.utc)

            attrs = [
                CL.labeled(
                    format_datetime_with_milliseconds(stamp, time_only=True),
                    "@",
                    label_style=CL.high2,
                ),
            ]

            try:
                # Calculate datetimes for the whole span of the (sub-)manifest
                (start, end, duration, delta, num_segments) = calculate_hls_pdt(
                    handler, stamp
                )

                # scan the segments
                scan_segments(handler, stamp, livemon_store, ad_pattern=ad_pattern)

                # Keep an eye on the media sequence, as it determines how to interpret the data from the current handler
                # For example, if there's not been a change of media sequence, there should not be any significant in the document either
                if last_handler:
                    media_sequence_delta = (
                        handler.document.media_sequence
                        - last_handler.document.media_sequence
                    )
                    previous_pdt = last_handler.document.program_date_time
                    start_pdt_should_be = previous_pdt + timedelta(
                        seconds=sum(
                            smr.segment.duration
                            for smr in livemon_store.segment_map
                            if smr.status == SignalEventStatus.REMOVED
                        )
                    )
                else:
                    media_sequence_delta = None
                    start_pdt_should_be = None

                # Re-calculate the rolling averages
                delta_num_segments_from_rolling_avg = None
                delta_duration_from_rolling_avg = None
                if media_sequence_delta and media_sequence_delta != 0:
                    if len(rolling_num_segments) > 0:
                        rolling_avg_num_segments = sum(rolling_num_segments) / len(
                            rolling_num_segments
                        )
                        delta_num_segments_from_rolling_avg = (
                            num_segments - rolling_avg_num_segments
                        )
                        rolling_avg_duration = sum(rolling_duration) / len(
                            rolling_duration
                        )
                        delta_duration_from_rolling_avg = (
                            duration.total_seconds() - rolling_avg_duration
                        )
                    rolling_num_segments.append(num_segments)
                    rolling_duration.append(duration.total_seconds())

                attrs.extend(
                    [
                        CL.format(
                            label="mseq",
                            value=handler.document.media_sequence,
                            conditions=[
                                (lambda x, msq: msq and abs(msq) > 50, CL.error_high),
                                (lambda x, msq: msq and abs(msq) < 0, CL.error_high),
                                (lambda x, msq: msq and abs(msq) > 10, CL.error),
                                (lambda x, msq: msq and abs(msq) > 4, CL.warning),
                                (lambda x, msq: msq == 0, CL.past),
                            ],
                            msq=media_sequence_delta,
                        ),
                        CL.format(
                            label="start",
                            value=format_datetime_with_milliseconds(
                                start, time_only=True, with_timezone=True
                            ),
                            conditions=[
                                (lambda x, **k: media_sequence_delta == 0, CL.past),
                                # start PDT went back?
                                (lambda x, sp, sn, **k: sp and sn < sp, CL.error_high),
                                # start PDT different from previous + delta of removed segments?
                                (
                                    lambda x, sstart, sn, **k: sstart and sn != sstart,
                                    CL.error_high,
                                ),
                            ],
                            sp=(
                                last_handler.document.program_date_time
                                if last_handler
                                else None
                            ),
                            sn=start,
                            sstart=start_pdt_should_be,
                        ),
                        CL.format(
                            label="len",
                            value=format_timedelta(duration),
                            conditions=[
                                # more than 10 sec delta
                                (lambda x, d: d and abs(d) > 10, CL.warning),
                                # (lambda x, d: media_sequence_delta == 0, CL.past),
                            ],
                            d=delta_duration_from_rolling_avg,
                        ),
                        CL.format(
                            label="#seg",
                            value=num_segments,
                            conditions=[
                                # major increase or decrease in number of segments (in average)
                                (lambda x, d: d and abs(d) > 2, CL.warning),
                                # (lambda x, d: media_sequence_delta == 0, CL.past),
                            ],
                            d=delta_num_segments_from_rolling_avg,
                        ),
                        CL.format(
                            label="end",
                            value=format_datetime_with_milliseconds(
                                end, time_only=True
                            ),
                            conditions=[
                                # (lambda x: media_sequence_delta == 0, CL.past)
                            ],
                        ),
                        CL.format(
                            label="tΔ",
                            value=f"{delta:+.3f}",
                            conditions=[(lambda x, d: d < -10 or d > 10, CL.warning)],
                            d=delta,
                        ),
                    ]
                )

            except Exception as e:
                attrs.extend(
                    [
                        CL.format(
                            label="status",
                            value=handler.status,
                            conditions=[
                                (lambda x: x != 200, CL.error),
                            ],
                        ),
                        CL.labeled(e.args[0], "error", CL.error),
                    ]
                )

            click.echo("  ".join(attrs))

            # Add map
            if with_map:
                click.echo(
                    "                "
                    + CL.labeled(
                        label="segs", text=make_segment_map(livemon_store.segment_map)
                    )
                    + "  "
                    + CL.labeled(
                        label="content",
                        text=make_content_summary(livemon_store.segment_map),
                    ),
                )

            # Add bk-ml info
            if with_adinfo:
                adinfo = bkml_handler.retrieve().summarize(end)
                if adinfo:
                    click.echo(
                        "                " + CL.labeled(label="ads", text=adinfo)
                    )

            # Add to file
            if save_to_file:
                output_path = OutputStore.get_output_folder(handler.session_id)
                with open(f"{output_path}/monitor.txt", "a") as f:
                    f.write("  ".join(attrs) + "\n")
                    f.close()

            # Detect signals
            try:
                changes = livemon_store.changes
                if changes["added"]:
                    if not silent:
                        sound_alert(changes["added"])

                    # Print new ones
                    if with_signals:
                        for n, signal in enumerate(changes["added"]):
                            line = "  " + "  ".join(
                                [
                                    CL.labeled(n + 1, "NEW", label_style=CL.high3),
                                    CL.labeled(signal.type.name, "type"),
                                    CL.labeled(
                                        format_signal(signal),
                                        "/",
                                    ),
                                    CL.labeled(
                                        format_datetime_with_milliseconds(
                                            signal.signal_time.astimezone(timezone.utc)
                                        ),
                                        "for",
                                    ),
                                ]
                            )
                            click.echo(line)
                            if signal.payload:
                                # click.echo(
                                #     " " * 2 + CL.labeled(signal.payload, "pld", CL.high3)
                                # )
                                for line in summarize(signal.payload):
                                    click.echo(" " * 2 + line)

                            # Add segment info to which the marker is attached
                            for line in HLSFormatter.pretty(
                                str(signal.content), handler, expand_info=False, ad_pattern=ad_pattern
                            ).splitlines():
                                click.echo("   │ " + line)
                            click.echo()

                            # Add to file
                            if save_to_file:
                                with open("monitor.txt", "a") as f:
                                    f.write(line + "\n")
                                    f.write(str(signal.content) + "\n")
                                    f.write("\n".join(summarize(signal.payload)) + "\n")
                                    f.close()

                    # Print a summary table
                    if with_schedule:
                        livemon_store.event_collector.make_table()

            except Exception as e:
                pass

            if with_frames:
                output_folder = OutputStore.get_output_folder(
                    handler.session_id, "frames"
                )
                show_video_frames(
                    livemon_store.segment_map,
                    max_frames=CONFIG.get(
                        "max-frames", section="monitor", cast_type=int
                    ),
                    output_folder=output_folder,
                )

            # End of processing and displaying

            if counter == 1:
                break

            for j in range(4):
                time.sleep(int(interval) / 4)
                bar.update(
                    -counter - 1,
                    time=stamp.strftime("%H:%M:%S UTC"),
                    sequence=handler.document.media_sequence,
                )

            # time.sleep(int(interval))
            last_handler = copy(handler)
            handler.reload()
            counter = counter - 1
            inc_counter = inc_counter + 1

    except KeyboardInterrupt:
        print("Stopped!")


def format_signal(signal):
    if not signal.signal_event_type:
        return "-"

    t = signal.signal_event_type
    n = t.name
    if t == SignalEventType.AD:
        return click.style(n, fg="green")
    if t == SignalEventType.SLATE:
        return click.style(n, fg="blue")
    if t == SignalEventType.CUE_OUT:
        return click.style(n, fg="magenta")
    if t == SignalEventType.CUE_IN:
        return click.style(n, fg="yellow")
    return n


def calculate_hls_pdt(
    handler: HLSHandler, now_stamp
) -> Tuple[datetime, datetime, timedelta, float, int]:
    start = handler.document.program_date_time
    end = handler.document.segments[-1].current_program_date_time
    end += timedelta(seconds=handler.document.segments[-1].duration)
    duration = end - start
    num_segments = len(handler.document.segments)

    delta = end - now_stamp

    return (
        start.astimezone(timezone.utc),
        end.astimezone(timezone.utc),
        duration,
        delta.total_seconds(),
        num_segments,
    )


def scan_segments(
    handler: HLSHandler,
    stamp: datetime,
    store: LiveMonitorInfoStore,
    ad_pattern: str = "/bpkio-jitt",
):
    """Function that scans all segments in the playlist and extracts relevant information from them"""
    with store:
        # Detect markers
        for segment in handler.document.segments:

            # First we look at tags
            # #EXT-X-DISCONTINUITY
            if segment.discontinuity:
                event_type = None
                if ad_pattern in segment.uri:
                    event_type = SignalEventType.AD
                    if "/slate_" in segment.uri:
                        event_type = SignalEventType.SLATE

                store.record_signal(
                    LiveSignal(
                        type=SignalType.DISCONTINUITY,
                        appeared_at=stamp,
                        content=segment,
                        signal_time=segment.current_program_date_time,
                        signal_event_type=event_type,
                    )
                )
                store.add_to_map(segment, SignalType.DISCONTINUITY)

            # #EXT-OATCLS-SCTE35
            if segment.oatcls_scte35:
                if segment.cue_out_start:
                    store.record_signal(
                        LiveSignal(
                            type=SignalType.SCTE35_MARKER,
                            appeared_at=stamp,
                            content=segment,
                            signal_time=segment.current_program_date_time,
                            payload=segment.oatcls_scte35,
                            signal_event_type=SignalEventType.CUE_OUT,
                        )
                    )
                    store.add_to_map(segment, SignalEventType.CUE_OUT)
                if segment.cue_in:
                    store.record_signal(
                        LiveSignal(
                            type=SignalType.SCTE35_MARKER,
                            appeared_at=stamp,
                            content=segment,
                            signal_time=segment.current_program_date_time,
                            payload=segment.oatcls_scte35,
                            signal_event_type=SignalEventType.CUE_IN,
                        )
                    )
                    store.add_to_map(segment, SignalEventType.CUE_IN)

            # #EXT-X-DATERANGES
            for daterange in segment.dateranges:
                sig = LiveSignal(
                    type=SignalType.DATERANGE,
                    appeared_at=stamp,
                    content=segment,
                    signal_time=(
                        datetime.fromisoformat(
                            daterange.start_date.replace("Z", "+00:00")
                        )
                        if daterange.start_date
                        else datetime.fromisoformat(
                            daterange.end_date.replace("Z", "+00:00")
                        )
                    ),
                    payload=(
                        daterange.scte35_out
                        or daterange.scte35_in
                        or daterange.scte35_cmd
                    ),
                    signal_event_type=(
                        SignalEventType.CUE_IN
                        if daterange.scte35_in
                        else SignalEventType.CUE_OUT
                    ),
                )
                store.record_signal(sig)
                store.add_to_map(segment, sig.signal_event_type)

            # Others
            if segment.cue_in:
                store.record_signal(
                    LiveSignal(
                        type=SignalType.SCTE35_MARKER,
                        appeared_at=stamp,
                        content=segment,
                        signal_time=segment.current_program_date_time,
                        signal_event_type=SignalEventType.CUE_IN,
                        # payload=segment.scte35,
                    )
                )
                store.add_to_map(segment, SignalEventType.CUE_IN)

            # Then the segments themselves
            if ad_pattern in segment.uri:
                if "/slate_" in segment.uri:
                    store.add_to_map(segment, SignalEventType.SLATE)
                else:
                    store.add_to_map(segment, SignalEventType.AD)
            else:
                store.add_to_map(segment, SignalEventType.CONTENT)


def sound_alert(signals: List[LiveSignal]):
    scte_signals = [
        s for s in signals if s.type in (SignalType.SCTE35_MARKER, SignalType.DATERANGE)
    ]
    if len(scte_signals):
        # only check the first signal
        if any(
            s for s in scte_signals if s.signal_event_type == SignalEventType.CUE_OUT
        ):
            sounds.chime_up()
        elif any(
            s for s in scte_signals if s.signal_event_type == SignalEventType.CUE_IN
        ):
            sounds.chime_down()
        else:
            sounds.chime()

    period_signals = [
        s for s in signals if s.type in (SignalType.DISCONTINUITY, SignalType.PERIOD)
    ]
    if len(period_signals):
        if any(s for s in period_signals if s.signal_event_type == SignalEventType.AD):
            sounds.chime_uphigh()
        else:
            sounds.chime()

    if any(s for s in signals if s not in scte_signals and s not in period_signals):
        sounds.chime()


def make_segment_map(map):
    backgrounds = dict()
    backgrounds[SignalEventStatus.EXISTING] = (90, 90, 90)
    backgrounds[SignalEventStatus.NEW] = (50, 102, 102)
    backgrounds[SignalEventStatus.REMOVED] = (60, 40, 40)

    outputs = {}

    last_status = None
    for seg in map:
        if seg.status == SignalEventStatus.EXPIRED:
            continue

        current_status = seg.status
        # Just to beautify things...
        if current_status != last_status:
            outputs[current_status] = click.style(" ", bg=backgrounds[current_status])
            last_status = current_status

        if segdef := SYMBOLS.get(seg.type):
            fg_color = segdef.get("color", "white")
            if current_status == SignalEventStatus.REMOVED:
                fg_color = (105, 105, 105)

            outputs[current_status] += click.style(
                segdef["symbol"],
                fg=fg_color,
                bg=backgrounds[seg.status],
            )
        else:
            output += "?"

        # White space for readability
        outputs[current_status] += click.style(" ", bg=backgrounds[current_status])

    sizes = CONFIG.get("segment-map-size", section="monitor", cast_type=list[int])
    # doubled to account for whitespaces
    sizes = [s * 2 for s in sizes]

    # trim/pad the map of removed segments to ensure alignment between subsequent calls
    removed_str = outputs.get(SignalEventStatus.REMOVED, "")
    removed_str = trim_or_pad_plus(
        removed_str,
        size=9,
        pad=True,
        align="right",
        bg=functools.partial(click.style, bg=backgrounds[SignalEventStatus.REMOVED]),
    )
    outputs[SignalEventStatus.REMOVED] = removed_str

    # trim the map of new and existing segments
    for st in [SignalEventStatus.EXISTING, SignalEventStatus.NEW]:
        ot = outputs.get(st, "")
        outputs[st] = trim_or_pad_plus(
            ot,
            size=sizes,
            pad=False,
            align="right",
            bg=functools.partial(click.style, bg=backgrounds[st]),
        )

    output = ""
    output += outputs.get(SignalEventStatus.REMOVED, "")
    output += outputs.get(SignalEventStatus.EXISTING, "")
    output += outputs.get(SignalEventStatus.NEW, "")

    return output


def make_content_summary(map):
    discontinuity_counter = 0
    content_map = []

    for seg in map:
        if seg.status in [SignalEventStatus.EXPIRED, SignalEventStatus.REMOVED]:
            continue

        if seg.type == SignalType.DISCONTINUITY:
            discontinuity_counter += 1
            continue

        # Add new info if first segment following a discontinuity
        if len(content_map) <= discontinuity_counter:
            if segdef := SYMBOLS.get(seg.type):
                if letter := segdef.get("letter"):
                    content_map.append(
                        click.style(letter, fg=segdef.get("color", "white"))
                    )

    return "".join(content_map)


def show_video_frames(segment_map, max_frames, output_folder):
    click.echo()

    frame_extractor = FrameExtractor(output_folder)
    new_segments = [seg for seg in segment_map if seg.status == SignalEventStatus.NEW][
        -max_frames:
    ]

    frames = {}
    spaces = 3
    margin_left = 6
    seg: SegmentMapRecord
    for seg in new_segments:
        # TODO - do it in parallel with multiprocessing
        orig_filename, frame, vert_cursor_moves = (
            frame_extractor.extract_frame_and_show(seg)
        )

        if frame:
            frames[orig_filename] = frame.splitlines()

    if len(frames):
        num_lines = len(list(frames.values())[0])
        frame_width = visible_length(list(frames.values())[0][0])  # TODO - faulty

        # Line of frame titles
        titles = ""
        for filename in frames.keys():
            # size of 32 found empirically, for 16:9 content and chafa size set to 32x18
            title = trim_or_pad(filename, size=32, pad=True)
            if seg.type == SignalEventType.AD:
                title = click.style(title, fg="green")
            if seg.type == SignalEventType.SLATE:
                title = click.style(title, fg="blue")

            titles += title + " " * (spaces + 1)
        click.echo(" " * margin_left + titles)

        # Detect whether vui was used in image mode
        cursor_move_up = cursor_move_down = ""
        if num_lines == 1:
            cursor_move_up = f"\033[{vert_cursor_moves}A"
            cursor_move_down = f"\033[{vert_cursor_moves}B\n"

        # frames, line by line
        for i in range(num_lines):
            line = ""
            for frame in frames.values():
                line += frame[i] + " " * spaces + cursor_move_up
            click.echo(" " * margin_left + line)

        click.echo(cursor_move_down)
