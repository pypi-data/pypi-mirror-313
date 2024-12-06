import difflib

import click


def styled_text(text, fg_color, effect=None):
    return click.style(text, fg=fg_color, **(effect if effect else {}))


def generate_diff(old, new):
    if isinstance(old, bytes):
        old = old.decode()

    old_lines = old.strip().split("\n")
    new_lines = new.strip().split("\n")
    matcher = difflib.SequenceMatcher(None, old_lines, new_lines)
    result = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for line in old_lines[i1:i2]:
                result.append(styled_text(line, "white"))  # unchanged lines
        elif tag == "delete":
            for line in old_lines[i1:i2]:
                result.append(
                    styled_text(line, "red", {"strikethrough": True})
                )  # deleted lines
        elif tag == "insert":
            for line in new_lines[j1:j2]:
                result.append(styled_text(line, "green", {}))  # inserted lines
        elif tag == "replace":
            for line in old_lines[i1:i2]:
                result.append(
                    styled_text(line, "red", {"strikethrough": True})
                )  # replaced old
            for line in new_lines[j1:j2]:
                result.append(styled_text(line, "yellow", {}))  # replaced new
    return "\n".join(result)
