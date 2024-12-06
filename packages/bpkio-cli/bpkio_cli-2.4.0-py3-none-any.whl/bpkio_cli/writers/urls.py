from typing import Optional
from urllib.parse import parse_qs, urlparse

import click


def pretty_url(
    url, path_highlight: Optional[str] = None, highlight_placeholder_params=True
):
    parsed = urlparse(url)
    base_url = click.style(f"{parsed.scheme}://{parsed.netloc}", fg="magenta")
    lines = [base_url]

    path = click.style("  " + parsed.path, fg="yellow")
    if path_highlight:
        path = path.replace(path_highlight, "") + click.style(
            path_highlight, fg="yellow", dim=True
        )
    lines.append(path)

    qs = parse_qs(parsed.query, keep_blank_values=False, strict_parsing=False)
    for i, (k, v) in enumerate(qs.items()):
        style = dict(fg="blue", bold=True)
        if highlight_placeholder_params:
            if v[0].startswith("$arg_"):
                style["fg"] = "green"
                style["bold"] = False
            elif v[0].startswith("$"):
                style["fg"] = "red"
                style["bold"] = False

        separator = "?" if i == 0 else "&"
        elements = [
            "    " + click.style(separator, fg="white", dim=True),
            click.style(k, fg="cyan"),
            click.style("=", fg="white", dim=True),
            click.style(v[0], **style),
        ]
        lines.append(" ".join(elements))

    return "\n".join(lines)


def split_url(url):
    """Splits the URL on common dividers, into segments starting with those dividers"""
    # dividers = ["/", ".", "-", "_", "?", "&"]
    dividers = ["/", "?", "&"]

    parts = []
    current_part = ""
    for char in url:
        if char in dividers:
            if current_part:
                parts.append(current_part)
                current_part = ""
            current_part = char
        else:
            current_part += char
    if current_part:
        parts.append(current_part)
    return parts


def diff_url(first, second):
    # Split the two strings using the previously defined function
    first_parts = split_url(first)
    second_parts = split_url(second)

    # ellipsis = " " + click.style("(⋯)", fg="black", dim=True) + " "
    ellipsis = " (⋯) "

    # Compare and construct the new array, collapsing consecutive ellipses
    new_array = []
    last_item = None
    for i in range(len(second_parts)):
        if i < len(first_parts) and second_parts[i] == first_parts[i]:
            if last_item != ellipsis:
                new_array.append(ellipsis)
                last_item = ellipsis
        else:
            new_array.append(second_parts[i])
            last_item = second_parts[i]

    return "".join(new_array)
