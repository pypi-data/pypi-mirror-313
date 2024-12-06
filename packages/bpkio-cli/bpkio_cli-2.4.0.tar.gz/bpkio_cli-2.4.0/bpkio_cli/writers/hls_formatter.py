import re

import bpkio_cli.writers.scte35 as scte35
from bpkio_api.exceptions import BroadpeakIoHelperError
from bpkio_cli.core.exceptions import UnexpectedContentError
from bpkio_cli.writers.breadcrumbs import display_error
from bpkio_cli.writers.colorizer import Colorizer as CL
from bpkio_cli.writers.formatter import OutputFormatter
from colorama import init
from media_muncher.codecstrings import CodecStringParser
from media_muncher.handlers import HLSHandler

init()


class HLSFormatter(OutputFormatter):
    def __init__(self, handler: HLSHandler) -> None:
        super().__init__()
        self.handler = handler
        self.top: int = 0
        self.tail: int = 0
        self.ad_pattern = "/bpkio-jitt"

    @property
    def _content(self):
        content = self.handler.content.decode()

        # content = self.trim(content, self.top, self.tail)

        return content

    @property
    def _looks_like_hls(self):
        return self.handler.appears_supported()

    def format(self, mode="standard", top: int = 0, tail: int = 0, trim: int = 0):
        if top and top > 0:
            self.top = top
        if tail and tail > 0:
            self.tail = tail

        try:
            if self._looks_like_hls:
                match mode:
                    case "raw":
                        out = self._content
                    case "standard":
                        out = self.highlight()
            else:
                out = self._content
                out += "\n\n"
                out += display_error("Error - This payload does not appear to be HLS")

            return self.trim(out, self.top, self.tail, max_length=trim)

        except BroadpeakIoHelperError as e:
            out = self._content
            out += "\n\n"
            out += display_error(f"Error - {e.message}: {e.original_message}")
            return out

        except Exception as e:
            raise UnexpectedContentError(
                message="Error formatting the content. "
                "It does not appear to be a valid or supported HLS document.\n"
                "Error raised: \n{}\n"
                "Raw content: \n{}".format(e, self.handler.content)
            )

    def highlight(self):
        return HLSFormatter.pretty(
            self._content, self.handler, ad_pattern=self.ad_pattern
        )

    @staticmethod
    def pretty(content, handler: HLSHandler, ad_pattern: str, expand_info=True):
        """Highlights specific HLS elements of interest"""

        nodes_to_highlight = {
            "#EXT-X-DATERANGE": CL.high2,
            "#EXT-OATCLS-SCTE35": CL.high2,
            "#EXT-X-PROGRAM-DATE-TIME": CL.high2,
            "#EXT-X-ENDLIST": CL.high2,
            "#EXT-X-DISCONTINUITY-SEQUENCE": CL.high2,
        }

        separator_sequences = [
            "#EXT-X-DISCONTINUITY",
            "#EXT-X-CUE-IN",
            "#EXT-X-CUE-OUT",
            "#EXT-X-CUE",
        ]

        new_lines = []
        previous_pdt = None
        delta_pdt = None
        last_segment_duration = None
        last_segment_url = None

        for line in content.splitlines():
            pattern = re.compile(r"^(#[A-Z0-9\-]*?)(\:|$)(.*)$")
            match = pattern.match(line)

            # handle HLS markup
            if match:
                node = match.group(1)

                # Special treatment for separators. Add a separator line
                if node in separator_sequences:
                    ansi_escape = re.compile(
                        r"(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]"
                    )
                    for index, line in reversed(list(enumerate(new_lines))):
                        line = ansi_escape.sub("", line)
                        if line.startswith("#"):
                            continue
                        else:
                            new_lines.insert(
                                index + 1,
                                CL.make_separator(length=150, mode="hls"),
                            )
                            break

                # Highlight specific nodes (relevant to broadpeak.io functionality)
                if node in nodes_to_highlight:
                    new_node = nodes_to_highlight[node](node)
                elif node in separator_sequences:
                    new_node = CL.high3(node)
                else:
                    new_node = CL.node(node)

                new_lines.append(
                    "{}{}{}".format(
                        new_node,
                        match.group(2),
                        HLSFormatter.pretty_attributes(match.group(3)),
                    )
                )

                # Extract stream information
                if node in ["#EXT-X-STREAM-INF"]:
                    # Extract the CODECS string, eg. '...,CODECS="mp4a.40.2,avc1.4d401f,mp4a.40.2",...'
                    codecstrings = HLSFormatter.extract_attribute_value(
                        match.group(3), ["CODECS"]
                    )
                    if codecstrings and expand_info:
                        codecs = CodecStringParser.parse_multi_codec_string(
                            codecstrings
                        )
                        info = [HLSFormatter.summarize_codecstring(c) for c in codecs]
                        new_lines.append(
                            bic_prefix()
                            + CL.bic_label("codecs")
                            + "  "
                            + "  ".join(
                                [
                                    CL.labeled(v, label=label, value_style=CL.comment)
                                    for label, v in info
                                ]
                            )
                        )

                # Provide a summary of SCTE35 information
                scte_payload = None
                if node in ["#EXT-OATCLS-SCTE35"]:
                    scte_payload = match.group(3)
                else:
                    scte_payload = HLSFormatter.extract_attribute_value(
                        match.group(3),
                        ["SCTE35-IN", "SCTE35-OUT", "SCTE35-CMD", "SCTE35"],
                    )

                if scte_payload and expand_info:
                    scte_payload = scte_payload.strip('"')
                    try:
                        summary = scte35.summarize(payload=scte_payload)
                        for line in summary:
                            new_lines.append(bic_prefix() + line)
                    except Exception as e:
                        new_lines.append(
                            bic_prefix()
                            + CL.comment(
                                "SCTE35 payload (unparsed): {}".format(scte_payload)
                            )
                        )

            # HLS comments
            elif line.startswith("#"):
                new_lines.append(CL.markup(line))

            # what's left is URLs
            else:
                this_segment_url = line

                # We calculate and compare PDTs to validate the timing in the manifest
                seg = handler.get_segment_for_url(this_segment_url)
                if (
                    seg
                    and hasattr(seg, "current_program_date_time")
                    and getattr(seg, "current_program_date_time")
                ):
                    pdt_comment = seg.current_program_date_time.isoformat()
                    if previous_pdt:
                        delta_pdt = seg.current_program_date_time - previous_pdt
                        pdt_comment += f"  (δ {round(delta_pdt.total_seconds(), 4)})  "

                        if (
                            last_segment_duration
                            and delta_pdt.total_seconds() != last_segment_duration
                        ):
                            delta_with_last_segment = round(
                                last_segment_duration - delta_pdt.total_seconds(), 4
                            )
                            if delta_with_last_segment > 0:
                                pdt_comment += CL.error_high(
                                    f" ⚠️  should be {last_segment_duration}  (overlap of {abs(delta_with_last_segment)}) "
                                )
                            else:
                                pdt_comment += CL.error(
                                    f" ⚠️  should be {last_segment_duration}  (gap of {abs(delta_with_last_segment)}) "
                                )

                    # Add to the last line (which should be the EXTINF)
                    new_lines[-1] += (
                        " " * 3
                        + bic_prefix()
                        + CL.labeled(pdt_comment, "pdt", CL.comment, CL.bic_label)
                    )
                    # new_lines.append(
                    #     bic_prefix() + CL.labeled(pdt_comment, "pdt", CL.comment)
                    # )
                    previous_pdt = seg.current_program_date_time
                    last_segment_duration = seg.duration

                # We apply smart trim of the segment URL to reduce noise
                # Removed 13-JUN-24 as it's confusing when used with trim/top/tail
                # if last_segment_url and not handler.has_children():
                #     line = diff_url(last_segment_url, this_segment_url)

                if ad_pattern in this_segment_url:
                    if "/slate_" in line:
                        new_lines.append(CL.url_slate(line))
                    else:
                        new_lines.append(CL.url_ad(line))
                else:
                    new_lines.append(CL.url(line))
                # new_lines.append(line)

                # blank line for readability
                new_lines.append("")

                last_segment_url = this_segment_url

        return "\n".join(new_lines)

    @staticmethod
    def pretty_attributes(text: str):
        # special case for standalone base64 SCTE payloads,
        #  eg. `EXT-OATCLS35:/AAuAAAAAAAAAP/wBQaAAAAAAAAYAhZDVUVJAADRiADfAABSZcAAADQAAAAAnp73Jg==`
        if text.endswith("="):
            return CL.value(text)

        pattern = re.compile(r'([\w-]+)=((?:[^,"]+|"[^"]*")+),?')
        matches = pattern.findall(text)
        key_value_pairs = [match for match in matches]

        if matches:
            new_attrs = []
            for k, v in key_value_pairs:
                new_key = CL.attr(k)
                has_quotes = v.startswith('"')
                if has_quotes:
                    v = v[1:-1]
                new_value = CL.url(v) if k == "URI" else CL.value(v)
                if has_quotes:
                    new_value = f'"{new_value}"'
                new_attrs.append(f"{new_key}={new_value}")

            return ",".join(new_attrs)
        else:
            return CL.value(text)

    @staticmethod
    def extract_attribute_value(text, attr):
        if not isinstance(attr, list):
            attr = [attr]

        pattern = re.compile(r'([\w-]+)=((?:[^,"]+|"[^"]*")+),?')
        matches = pattern.findall(text)
        key_value_pairs = {m[0]: m[1] for m in matches}

        for a in attr:
            if a in key_value_pairs:
                return key_value_pairs[a]

    @staticmethod
    def summarize_codecstring(codec):
        if codec["type"] == "video":
            return (
                "video",
                f"{codec.get('codec')}, profile {codec.get('profile')} @ level {codec.get('level')}",
            )

        if codec["type"] == "audio":
            return "audio", f"{codec.get('codec')}, {codec.get('mode')}"


def bic_prefix():
    return CL.comment("# ") + CL.orange("bic:")
