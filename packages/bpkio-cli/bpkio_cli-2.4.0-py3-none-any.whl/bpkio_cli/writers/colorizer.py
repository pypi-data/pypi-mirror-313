import re
from typing import Callable, List, Optional, Tuple
from urllib.parse import parse_qs, urlparse

import click


class Colorizer:
    @staticmethod
    def orange(text):
        return click.style(text, fg=(255, 165, 0))

    @staticmethod
    def magenta(text, bold: bool = False):
        return click.style(text, fg="magenta", bold=bold)

    @staticmethod
    def node(text):
        return click.style(text, fg="white", bold=True)

    @staticmethod
    def attr(text):
        return click.style(text, fg="bright_blue")

    @staticmethod
    def value(text):
        return click.style(text, fg="cyan")

    @staticmethod
    def markup(text):
        return click.style(text, fg="white", dim=True)

    @staticmethod
    def past(text):
        return click.style(text, fg="white", dim=True)

    @staticmethod
    def future(text):
        return click.style(text, fg="green", dim=False)

    @staticmethod
    def high1(text):
        return click.style(text, fg="yellow")

    @staticmethod
    def high2(text):
        return click.style(text, fg="yellow", bold=True)

    @staticmethod
    def high2_rev(text):
        return click.style(text, fg="yellow", bold=True, reverse=True)

    @staticmethod
    def high3(text):
        return click.style(text, fg="magenta", bold=True)

    @staticmethod
    def high3_rev(text):
        return click.style(text, fg="magenta", bold=True, reverse=True)

    @staticmethod
    def url(text, highlight=True):
        return Colorizer.split_url(text, fg="yellow", italic=True, highlight=highlight)

    @staticmethod
    def url_ad(text, highlight=True):
        return Colorizer.split_url(text, fg="green", italic=True, highlight=highlight)

    @staticmethod
    def url_slate(text, highlight=True):
        return Colorizer.split_url(text, fg="blue", italic=True, highlight=highlight)

    @staticmethod
    def comment(text):
        return click.style(text, fg="bright_black", italic=True)

    @staticmethod
    def info(text):
        return click.style(text, fg="cyan")

    @staticmethod
    def ok(text):
        return click.style(text, fg="green")

    @staticmethod
    def warning(text):
        return click.style(text, fg="red")

    @staticmethod
    def error(text):
        return click.style(text, fg="red", bold=True)

    @staticmethod
    def error_high(text):
        return click.style(text, fg="red", reverse=True)

    @staticmethod
    def label(text):
        return click.style(text, fg="white", bg="black", dim=True)

    @staticmethod
    def bic_label(text):
        return click.style(text, fg=(255, 165, 0), bg="black", dim=True)

    @staticmethod
    def make_separator(
        text: Optional[str] = None, length: Optional[int] = None, mode=None
    ):
        # if text:
        #     dashes = "-" * len(text)
        # else:
        #     if not length:
        length = 50
        dashes = "-" * length

        if mode == "xml":
            dashes = f"<!-- {dashes} -->"
        if mode == "hls":
            dashes = f"## {dashes}"

        return Colorizer.high3(dashes)

    @staticmethod
    def indent(num, text):
        out = []
        for line in text.split("\n"):
            out.append("   " * num + line)

        return "\n".join(out)

    @staticmethod
    def bullet(text):
        return " • " + text

    @staticmethod
    def hfield(*items):
        return " ".join(items)

    @staticmethod
    def vfield(*items):
        return "\n".join(items)

    @staticmethod
    def log(text, type):
        match str(type).lower():
            case "warning":
                return Colorizer.warning(f"[Warning] {text}")
            case "info":
                return Colorizer.attr(text)
            case "error":
                return Colorizer.error(f"[Error] {text}")

    @staticmethod
    def labeled(
        text,
        label,
        value_style: Optional[Callable] = None,
        label_style: Optional[Callable] = None,
    ):
        if label_style:
            lbl = label_style(label)
        else:
            lbl = Colorizer.label(label)

        if value_style:
            return f"{lbl} {value_style(text)}"
        else:
            return f"{lbl} {text}"

    @staticmethod
    def format(
        value,
        label: Optional[str] = None,
        conditions: Optional[List[Tuple[Callable, Callable]]] = None,
        label_style: Optional[Callable] = None,
        **kwargs,
    ):
        """
        Formats a given value with its label and applies colorization based on conditions.
        Allows passing extra keyword arguments to condition functions.

        :param value: The main value to format.
        :param label: The label for the value.
        :param conditions: A list of tuples where each tuple contains a condition function and a colorizing function.
        :param kwargs: Additional keyword arguments passed to condition functions.
        :return: Formatted string with label and possibly colorized value.
        """
        if conditions:
            for condition, colorize in conditions:
                # Check if the condition accepts any additional kwargs
                if condition(value, **kwargs):
                    try:
                        value = colorize(value)
                        break  # Stop after the first match
                    except Exception:
                        pass  # Skip this one on exception, and try next
        if label:
            if label_style:
                label = label_style(label)
            else:
                label = Colorizer.label(label)
            return f"{label} {value}"
        else:
            return value

    @staticmethod
    def split_url(url, fg="yellow", italic=True, highlight=True):
        strings = []
        parsed = urlparse(url)

        if parsed.scheme:
            strings.append(click.style(parsed.scheme + "://", fg=fg, bold=True))
        if parsed.netloc:
            strings.append(
                click.style(
                    parsed.netloc,
                    fg=fg,
                    bold=True,
                )
            )

        path_parts = parsed.path.split("/")

        # find index of the part to highlight
        if highlight:
            highlight_index = len(path_parts) - 1
            for i, part in enumerate(path_parts):
                if part == "bpk-sst":

                    highlight_index = i - 1
                    break
        else:
            highlight_index = -1

        for i, part in enumerate(path_parts):
            # resplit in case of ellipses
            subparts = part.split(" ")

            for subpart in subparts:
                if subpart == "(⋯)":
                    strings.append(
                        click.style(
                            " " + subpart + " ",
                            fg="white",
                            reverse=False,
                            bold=True,
                            italic=False,
                        )
                    )
                else:

                    if i == highlight_index:
                        strings.append(
                            click.style(
                                subpart,
                                fg=fg,
                                reverse=True,
                                bold=True,
                                italic=italic,
                            )
                        )
                    else:
                        strings.append(
                            click.style(
                                subpart,
                                fg=fg,
                                italic=italic,
                            )
                        )

            if i < len(path_parts) - 1:
                strings.append(click.style("/", fg=fg, italic=italic))

        qs = parse_qs(parsed.query, keep_blank_values=False, strict_parsing=False)
        for i, (k, v) in enumerate(qs.items()):
            separator = "?" if i == 0 else "&"
            strings.append(
                click.style(separator + k + "=", fg=fg, italic=italic, bold=True)
            )
            strings.append(click.style(f"{v[0]}", fg=fg, italic=italic, dim=True))

        if parsed.fragment:
            strings.append(
                click.style("#" + parsed.fragment, fg=fg, italic=italic, dim=True)
            )

        # Add query params
        return "".join(strings)


def trim_or_pad(s, size, pad=False):
    # Remove ANSI color codes using regex
    s_stripped = re.sub(r"\x1b\[[0-9;]*[a-zA-Z]", "", s)
    length = len(s_stripped)

    if length <= size:
        return (
            s + " " * (size - length - 1) if pad else s
        )  # Pad the string with spaces if `pad` is True
    else:
        half_n = (size - 1) // 2  # Subtract 1 for the ellipsis, then divide by 2
        return f"{s[:half_n]}…{s[-half_n:]}"


def trim_or_pad_plus(
    s, size: int | list, pad=False, align="left", bg: Callable = lambda x: x
):
    # Pattern to match ANSI codes and non-ANSI characters
    ansi_pattern = r"(\x1b\[[0-9;]*m)"
    # Find all ANSI codes and characters
    parts = re.split(ansi_pattern, s)

    # Filter out empty strings and consolidate ANSI codes with their following character
    consolidated = []
    visual_length = 0
    ansi_sequence = ""
    closing_ansi_sequence = ""
    for part in parts:
        if not part:
            continue
        if re.match(ansi_pattern, part):
            ansi_sequence += part  # Accumulate ANSI codes
        else:
            # Append the ANSI sequence (if any) with its following character
            consolidated.append(ansi_sequence + part)
            visual_length += len(part)
            ansi_sequence = ""  # Reset for the next sequence

    # Ensure the last ANSI sequence is stored if there's no character after it
    if ansi_sequence:
        closing_ansi_sequence = ansi_sequence

    output_string = ""

    required_size = size
    if isinstance(size, list):
        required_size = size[0] + size[1]

    if visual_length <= required_size:
        # Padding
        if pad:
            padding_length = required_size - visual_length
            padding = [bg(" ")] * padding_length
            if align == "left":
                output_string = "".join(consolidated) + "".join(padding)
            else:
                output_string = "".join(padding) + "".join(consolidated)
        else:
            output_string = "".join(consolidated)
    else:
        # Trimming
        ellipsis = " … "
        trim_size = required_size - len(ellipsis)
        if isinstance(size, list) and trim_size > 0:
            # Trim in the middle
            trimmed = (
                consolidated[: size[0]] + [bg(ellipsis)] + consolidated[-size[1] :]
            )
        elif align == "right":
            # Keep the start of the string, trim towards the end
            trimmed = [bg(ellipsis)] + consolidated[-trim_size:]
        elif align == "left":
            # Trim from the start, keep the end of the string
            trimmed = consolidated[:trim_size] + [bg(ellipsis)]

        # Reassemble the string, ensuring it ends with an ellipsis if trimming was necessary
        output_string = "".join(trimmed)

    return output_string + closing_ansi_sequence


def visible_length(string):
    """Calculate the length of string, after stripping all ANSI characters"""
    ansi_escape = re.compile(r"\x1b\[([0-9]+)(;[0-9]+)*[ml]")
    # Remove ANSI color codes
    s_without_ansi = ansi_escape.sub("", string)
    return len(s_without_ansi)
