import functools

from bpkio_cli.utils import OptionEatAll
from cloup import option, option_group


def list_options(default_fields=None):
    def decorator(fn):
        """Decorator to add multiple common decorators
        Idea from https://stackoverflow.com/questions/40182157/shared-options-and-flags-between-commands
        """

        @option_group(
            "Data manipulation",
            option(
                "--id",
                "id_only",
                is_flag=True,
                type=bool,
                default=False,
                help="Return the ids only, 1 per line. This can be useful for piping to other tools",
            ),
            option(
                "-s",
                "--sort",
                "sort_fields",
                cls=OptionEatAll,
                type=tuple,
                help="List of fields used to sort the list. Append ':desc' to sort in descending order",
            ),
            option(
                "--select",
                "select_fields",
                cls=OptionEatAll,
                type=tuple,
                default=default_fields,
                help="List of fields to return, separated by spaces",
            ),
            option(
                "--first",
                "return_first",
                is_flag=True,
                default=False,
                type=bool,
                help="Return only the first result",
            ),
        )
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        return wrapper

    return decorator
