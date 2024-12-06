from dataclasses import dataclass
from functools import lru_cache

import threefive

# Adding missing segmentation type ids
threefive.segmentation.table22[2] = "Call Ad Server"


@dataclass
class Scte35DescriptorType:
    id: int
    name: str
    pair: bool = False
    end_id: int | None = None

    @property
    def label(self):
        return self.name.replace(" ", "")

    def __str__(self):
        if self.pair:
            return f"{self.label} ({self.id}/{self.end_id})"
        else:
            return f"{self.label} ({self.id})"

    def __hash__(self) -> int:
        return hash(str(self))

    def color(self):
        if self.name.startswith("Break"):
            return "magenta"
        if self.name.startswith("Program"):
            return "blue"
        if self.name.startswith("Provider Advertisement"):
            return "cyan"
        if self.name.startswith("Distributor Advertisement"):
            return "red"
        if self.name.startswith("Call"):
            return "yellow"
        return "white"


@lru_cache
def descriptor_types():
    """Build the collection of descriptor types/pairs from threefive"""
    descriptor_types = {}
    for id, str in threefive.segmentation.table22.items():
        name = str
        is_range = False
        is_end = False
        if str.endswith("Start"):
            name = str[:-6]
            is_range = True
        if str.endswith("End"):
            name = str[:-4]
            is_end = True

        if is_end:
            descriptor_types[name].end_id = id
        else:
            descriptor_types[name] = Scte35DescriptorType(id, name, is_range)
    return descriptor_types


def get_descriptor_type(id: int) -> Scte35DescriptorType | None:
    for descriptor_type in descriptor_types().values():
        if descriptor_type.id == id:
            return descriptor_type
        if descriptor_type.end_id == id:
            return descriptor_type


def parse_mpu(format_identifier, upid_str):
    if format_identifier == "ADFR":
        if upid_str.startswith("0x"):
            upid_str = upid_str[2:]

        # First character is the version number
        version = int(upid_str[0:2])

        # Next 4 characters (2 bytes) are the channel identifier
        channel_id = int(upid_str[2:6], 16)

        # Next 8 characters (4 bytes) are the date in hex, representing an integer in the form YYYYMMDD
        date_hex = upid_str[6:14]
        date_int = int(date_hex, 16)
        date_str = f"{date_int:08}"  # Ensure the date is 8 characters long, pad with zeros if necessary
        date_formatted = f"{date_str[0:4]}-{date_str[4:6]}-{date_str[6:8]}"

        # Next 4 characters (2 bytes) are the commercial break code
        commercial_break_code = int(upid_str[14:18], 16)

        # The rest of the string is the ad break duration in milliseconds
        ad_break_duration = int(upid_str[18:], 16)

        # Convert the ad break duration from milliseconds to minutes and seconds
        ad_break_minutes = ad_break_duration // 60000
        ad_break_seconds = (ad_break_duration % 60000) // 1000
        ad_break_milliseconds = ad_break_duration % 1000

        hex_string = format_identifier.encode().hex()
        hex_string += upid_str.upper()

        # Create a result dictionary
        result = {
            "formatIdentifier": format_identifier,
            "hex": hex_string,
            "parsable": True,
            "versionNumber": version,
            "channelId": channel_id,
            "date": date_formatted,
            "adBreakCode": commercial_break_code,
            "adBreakDuration": ad_break_duration,
            "aBreakDuration": f"{ad_break_minutes} min, {ad_break_seconds} s, {ad_break_milliseconds} ms",
        }

        return result

    else:
        return {"formatIdentifer": format_identifier, "parsable": False}
