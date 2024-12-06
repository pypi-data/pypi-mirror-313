from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional

import m3u8
from bpkio_cli.monitor.event_collector import Scte35EventCollector
from threefive import Cue


class SignalType(Enum):
    PERIOD = "dash-period"
    DISCONTINUITY = "discontinuity"
    SCTE35_MARKER = "scte35-marker"
    DATERANGE = "daterange"
    HLS_MARKER = "hls-marker"
    DASH_EVENT = "dash-event"


class SignalEventType(Enum):
    CUE_IN = "cue-in"
    CUE_OUT = "cue-out"
    AD = "ad"
    SLATE = "slate"
    CONTENT = "content"


class SignalEventStatus(Enum):
    EXISTING = "existing"
    NEW = "new"
    REMOVED = "removed"
    ERROR = "error"
    WARNING = "warning"
    EXPIRED = "expired"
    _PENDING = "_pending"


@dataclass
class LiveSignal:
    """Used to record signals that occur in the HLS/DASH manifests"""

    type: SignalType
    appeared_at: datetime
    content: object
    payload: object | None = None
    disappeared_at: datetime | None = None
    num_appearances: int = 0
    signal_event_type: SignalEventType | None = None
    signal_time: datetime | None = None  # The time that the signal applies to, eg. PDT

    @property
    def id(self):
        if self.payload:
            return (self.payload, self.signal_event_type, self.signal_time)
        if isinstance(self.content, m3u8.Segment):
            return (self.content.uri, self.content.current_program_date_time)


@dataclass
class SegmentMapRecord:
    """Used to record segments and markers for a graphical representation"""

    type: SignalEventType | SignalType
    status: SignalEventStatus
    segment: m3u8.Segment


class LiveMonitorInfoStore:
    def __init__(self) -> None:
        self.signals: dict = {}
        self.changes: dict = {}
        self.event_collector = Scte35EventCollector()
        self.segment_map: List[SegmentMapRecord] = []
        self._timestamp: datetime

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.end()
        else:
            self.end()

    def __repr__(self):
        return f"<LiveMonitor signals={len(self.signals)} [A:{len(self.changes['added'])} U:{len(self.changes['updated'])} R:{len(self.changes['removed'])}]>"

    def _reset(self):
        self.changes = dict(
            added=[],
            updated=[],
            removed=[],
        )

    def start(self, timestamp: Optional[datetime] = None):
        # Start a new "transaction"
        self._reset()
        self._timestamp = timestamp or datetime.now()

        # Go through segment map and remove status from all previous non-expired markers
        # (which allows us to determine the ones removed at the end of the transaction)
        for seg in self.segment_map:
            if seg.status == SignalEventStatus.REMOVED:
                seg.status = SignalEventStatus.EXPIRED
            if seg.status != SignalEventStatus.EXPIRED:
                seg.status = SignalEventStatus._PENDING

    def end(self):
        # End the "transaction"

        # Search for removed signals
        signal: LiveSignal
        for sid, signal in self.signals.items():
            if not signal.disappeared_at:
                if (
                    signal not in self.changes["updated"]
                    and signal not in self.changes["added"]
                ):
                    self.changes["removed"].append(signal)
                    self.signals[signal.id].disappeared_at = self._timestamp

        # Go through segment map and those still pending must have been removed
        for seg in self.segment_map:
            if seg.status == SignalEventStatus._PENDING:
                seg.status = SignalEventStatus.REMOVED

    def record_signal(self, signal: LiveSignal) -> LiveSignal:
        # previously seen signal
        if signal.id in self.signals:
            signal = self.signals[signal.id]
            self.changes["updated"].append(signal)

        # new signal
        else:
            signal.appeared_at = self._timestamp
            self.changes["added"].append(signal)

        # then increment count and overwrite
        signal.num_appearances += 1
        self.signals[signal.id] = signal

        # extract event information
        if signal.payload:
            self.record_scte35(signal.payload, signal.signal_time)

        return signal

    def record_scte35(self, payload: str, signal_time: datetime):
        cue = Cue(payload)
        cue.decode()

        for d in cue.descriptors:
            if cue.info_section.splice_command_type == 6:
                self.event_collector.add_descriptor(d, signal_time)

    def add_to_map(self, segment: m3u8.Segment, type: SignalEventType | SignalType):
        # check if the segment was already seen before (based on mediasequence)
        # TODO - validate that the segment is the same
        segment_seen_before = False
        try:
            existing_segment = next(
                seg
                for seg in self.segment_map
                if seg.type == type
                and seg.segment.media_sequence == segment.media_sequence
            )
            segment_seen_before = True
            existing_segment.status = SignalEventStatus.EXISTING
        except Exception:
            pass

        if not segment_seen_before:
            self.segment_map.append(
                SegmentMapRecord(
                    type=type, status=SignalEventStatus.NEW, segment=segment
                )
            )
