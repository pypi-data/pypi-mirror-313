import functools

from cloup import option, option_group
from cloup.constraints import AcceptAtMost


def output_format_options(fn):
    @option_group(
        "Output format",
        option(
            "-j",
            "--json",
            is_flag=True,
            default=False,
            help="Return the results as a JSON representation",
        ),
        option(
            "--csv",
            is_flag=True,
            default=False,
            help="Return the results as a CSV document",
        ),
        option(
            "--format",
            "list_format",
            default=None,
            help="Format the table of results with a specific format (see `tabulate` options)",
        ),
        constraint=AcceptAtMost(1),
    )
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if kwargs.get("json"):
            kwargs["list_format"] = "json"
        if kwargs.get("csv"):
            kwargs["list_format"] = "csv"

        del kwargs["json"]
        del kwargs["csv"]

        return fn(*args, **kwargs)

    return wrapper
