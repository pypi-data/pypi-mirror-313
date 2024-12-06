import functools
from datetime import datetime
from typing import List

import bpkio_cli.utils.scte35 as scte35
import click
from bpkio_cli.monitor.scte35_event import Scte35Event
from bpkio_cli.writers.colorizer import Colorizer as CL
from bpkio_cli.writers.colorizer import trim_or_pad
from tabulate import tabulate
from threefive import SegmentationDescriptor


def max_lines_in_dict(d):
    max_lines = 0
    for value_list in d.values():
        if isinstance(value_list, list):
            line_count = 0
            for s in value_list:
                line_count += s.count("\n") + 1
            if line_count > max_lines:
                max_lines = line_count
    return max_lines


def vertical_pad_table_cell(content, max_lines, color, witdh):
    line_count = 0
    if isinstance(content, list):
        for s in content:
            line_count += s.count("\n") + 1

    if line_count < max_lines:
        color_line = functools.partial(click.style, fg=color, bold=False)
        content.extend(
            [color_line("│") + " " * (witdh - 2) + color_line("│")]
            * (max_lines - line_count)
        )

    return content


class Scte35EventCollector:
    def __init__(self) -> None:
        self.events = {}

    def add_descriptor(self, descr: SegmentationDescriptor, signal_time: datetime):
        # find the segmentation type
        seg_type = scte35.get_descriptor_type(descr.segmentation_type_id)
        if not seg_type:
            return

        # search for an existing event
        event_id = int(descr.segmentation_event_id, 16)
        if event_id in self.events:
            event = self.events[event_id]
        else:
            event = Scte35Event(event_id=event_id, segment_type=seg_type)
            self.events[event_id] = event

        # populate it
        if not seg_type.pair:
            event.occur.append(signal_time)
        if seg_type.pair and descr.segmentation_type_id == seg_type.id:
            event.start = signal_time
        if seg_type.pair and descr.segmentation_type_id == seg_type.end_id:
            event.end = signal_time

        if descr.segmentation_duration:
            event.duration = descr.segmentation_duration
        if descr.segmentation_upid:
            if descr.segmentation_upid_type == 12:
                event.upid_format = descr.segmentation_upid["format_identifier"]
                event.upid = descr.segmentation_upid["private_data"]
            else:
                event.upid = descr.segmentation_upid
        if descr.segment_num:
            event.position = descr.segment_num
            event.out_of = descr.segments_expected

    def get_all_times(self) -> List[datetime]:
        times = set()
        for event in self.events.values():
            times.update(event.occur)

            if event.start:
                times.add(event.start)

            if event.end:
                times.add(event.end)
        return sorted(times)

    def get_events_for_time(self, t, boundaries_only=True) -> List[Scte35Event]:
        events = set()
        for event in self.events.values():
            if t in event.occur:
                events.add(event)

            if event.start == t:
                events.add(event)

            if event.end == t:
                events.add(event)

            if event.segment_type.pair and (
                (event.start and event.end and event.start < t and t < event.end)
                or (event.start and not event.end and event.start < t)
                or (event.end and not event.start and t < event.end)
            ):
                events.add(event)

        # sort them do that the end ones come first
        events = sorted(events, key=lambda e: e.relative_order_at_time(t))
        return list(events)

    def get_segmentation_types_used(self) -> List[scte35.Scte35DescriptorType]:
        types = set()
        for event in self.events.values():
            types.add(event.segment_type)

        sorted_types = sorted(types, key=lambda t: t.id)
        return sorted_types

    def get_first_event_of_type(
        self, st: scte35.Scte35DescriptorType
    ) -> Scte35Event | None:
        for t in self.get_all_times():
            events = self.get_events_for_time(t)

            # only keep the ones for that segmentation type
            typed_events = [e for e in events if e.segment_type == st]
            typed_events = sorted(
                typed_events, key=lambda e: e.relative_order_at_time(t)
            )
            if typed_events:
                return typed_events[0]

    def make_table(self):
        times = self.get_all_times()
        schedule = []

        max_box_size = 38

        for t in times:
            record = dict(time=str(t), ongoing={})
            events = self.get_events_for_time(t, boundaries_only=False)
            for e in events:
                color_line = functools.partial(
                    click.style, fg=e.segment_type.color(), bold=False
                )
                color_title = functools.partial(
                    click.style, bg=e.segment_type.color(), fg="white", bold=True
                )

                ongoing = None
                header = None
                body = []
                footer = None
                if e.start == t and e.end == t:
                    header = str(e.event_id)
                    footer = "(start & end)"
                    ongoing = False
                elif e.start == t:
                    # line1 = f"{e.event_id} (start)"
                    header = str(e.event_id)
                    ongoing = True
                elif e.end == t:
                    # line1 = f"{e.event_id} (end)"
                    footer = str(e.event_id)
                    ongoing = False
                elif t in e.occur:
                    header = str(e.event_id)
                    ongoing = False

                if e.start == t or t in e.occur:
                    if e.upid:
                        try:
                            upid_parsed = scte35.parse_mpu(e.upid_format, e.upid)
                            body.append(CL.labeled(upid_parsed["hex"], "u"))
                            # body.append(CL.labeled(upid_parsed["adBreakCode"], "code"))
                            # body.append(
                            #     CL.labeled(
                            #         upid_parsed["adBreakDuration"] / 1000,
                            #         "dur",
                            #         value_style=CL.high1,
                            #     )
                            # )
                        except Exception as error:
                            body.append(CL.labeled(e.upid, "upid"))

                if e.start == t or (not e.start and e.end == t):
                    if e.position:
                        body.append(
                            CL.labeled(
                                f"{e.position}/{e.out_of}", "seg", value_style=CL.attr
                            )
                        )
                    if e.duration:
                        body.append(CL.labeled(e.duration, "dur", value_style=CL.high1))

                # Colorize
                lines = []
                if header:
                    lines.append(
                        color_title(
                            trim_or_pad(f" {header} ", size=max_box_size, pad=True)
                        )
                    )
                if body:
                    line = " " + "  ".join([str(b) for b in body])
                    lines.append(
                        color_line("└" if not e.segment_type.pair else "│")
                        + trim_or_pad(line, size=max_box_size - 2, pad=True)
                        + color_line("╯" if not e.segment_type.pair else "│")
                    )

                if footer:
                    lines.append(
                        color_line(
                            "└"
                            + "─" * (max_box_size - 2 - len(footer) - 1)
                            + footer
                            + "─"
                            + "╯"
                        )
                    )

                cell = record.get(e.segment_type, [])
                if len(lines):
                    cell.append("\n".join(lines))
                record[e.segment_type] = cell

                # record if the column is ongoing
                record["ongoing"][e.segment_type] = ongoing

            schedule.append(record)

        # Prepare for tabulate (to re-order columns and pad the cells)
        headers = dict(time="time")
        for t in self.get_segmentation_types_used():
            headers[t] = str(t)

        ongoing_columns = {}
        # Seed them based on the segmentation type, and whether the first record in the column is an end one
        for t in self.get_segmentation_types_used():
            first_event_in_column = self.get_first_event_of_type(t)
            if (
                first_event_in_column
                and first_event_in_column.end
                and not first_event_in_column.start
            ):
                ongoing_columns[t] = True if t.pair else False

        table = []
        for record in schedule:
            max_lines = max_lines_in_dict(record)
            row: List[str] = []
            table.append(row)
            for h in headers.keys():
                # Determine if the row has has ongoing events in that column
                if isinstance(record["ongoing"].get(h), bool):
                    ongoing_columns[h] = record["ongoing"][h]
                if h in record and bool(record[h]):
                    if isinstance(record[h], list):
                        lines = record[h]
                        if ongoing_columns.get(h) is True:
                            lines = vertical_pad_table_cell(
                                lines, max_lines, h.color(), max_box_size
                            )
                        row.append("\n".join(lines))
                    else:
                        row.append(record[h])
                    # TODO - backfill to match max lines
                else:
                    if (
                        isinstance(h, scte35.Scte35DescriptorType)
                        and ongoing_columns.get(h) is True
                    ):
                        lines = vertical_pad_table_cell(
                            [], max_lines, h.color(), max_box_size
                        )

                        row.append("\n".join(lines))
                    else:
                        # single line to make it easier to find start time across columns
                        row.append(
                            # click.style(" " + "─" * (max_box_size - 2), fg="white", dim="true")
                            ""
                        )

        print(tabulate(table, headers=headers, tablefmt="rounded_outline"))
        return schedule
