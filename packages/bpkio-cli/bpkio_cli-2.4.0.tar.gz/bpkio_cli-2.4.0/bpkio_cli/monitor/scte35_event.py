from dataclasses import dataclass, field
from datetime import datetime
from typing import List

import bpkio_cli.utils.scte35 as scte35


@dataclass
class Scte35Event:
    """Used to record SCTE35 events (as delimited by SCTE35 descriptors)"""

    event_id: int
    segment_type: scte35.Scte35DescriptorType
    occur: List[datetime] = field(default_factory=lambda: [])
    start: datetime | List[datetime] | None = None
    end: datetime | None = None
    duration: float | None = None
    upid: str | None = None
    upid_format: int | None = None
    position: int | None = None
    out_of: int | None = None
    chunks: List = field(default_factory=lambda: [])

    def relative_order_at_time(self, t: datetime):
        if self.end == self.start == t:
            return 0
        elif self.end == t:
            return -1
        elif self.start == t:
            return 2
        else:
            return 1

    def __hash__(self):
        return hash(self.event_id)