import re
from abc import ABC, abstractmethod


class OutputFormatter(ABC):
    @abstractmethod
    def format(self, mode: str = "standard") -> str:
        pass

    @staticmethod
    def trim(content, top=0, tail=0, max_length=0):
        if top or tail:
            lines = content.splitlines()
            lines_to_return = []

            if top + tail > len(lines):
                return OutputFormatter.trim_lines(content, max_length, as_string=True)

            if top > 0:
                lines_to_return.extend(lines[:top])

            if (rest := len(lines) - top - tail) > 0:
                lines_to_return.append(f"#\n# ... {rest} other lines ...\n#")

            if tail > 0:
                lines_to_return.extend(lines[-tail:])

            return OutputFormatter.trim_lines(
                lines_to_return, max_length, as_string=True
            )
        else:
            return OutputFormatter.trim_lines(content, max_length, as_string=True)

    @staticmethod
    def trim_line(line, max_length=0):
        if max_length > 0 and len(line) > max_length:
            return f"{line[:max_length]}..."
        else:
            return line

    @staticmethod
    def trim_lines(lines, max_length=0, as_string=True):
        if not isinstance(lines, list):
            lines = lines.splitlines()

        trimmed_lines = [
            OutputFormatter.trim_line_visible(line, max_length) for line in lines
        ]

        if as_string:
            return "\n".join(trimmed_lines)
        else:
            return trimmed_lines

    @staticmethod
    def trim_line_visible(line, max_length=0):
        if max_length <= 0 or not line:
            return line

        # Regular expression for matching ANSI escape codes
        ansi_escape_regex = re.compile(r"\x1b\[[0-9;]*m")

        # Split the input string into ANSI codes and other text
        parts = ansi_escape_regex.split(line)
        ansi_escapes = ansi_escape_regex.findall(line)

        # Reconstruct the string with trimmed visible characters
        trimmed_string = ""
        visible_length = 0
        for i, part in enumerate(parts):
            for char in part:
                if visible_length < max_length:
                    trimmed_string += char
                    visible_length += 1
                else:
                    # Add ellipsis and break if the string is being trimmed
                    trimmed_string += "..."
                    return trimmed_string
            if i < len(ansi_escapes):
                trimmed_string += ansi_escapes[i]

        # Check if the string was trimmed and add ellipsis if it was
        if len(line) > len(trimmed_string):
            trimmed_string += "..."

        return trimmed_string
