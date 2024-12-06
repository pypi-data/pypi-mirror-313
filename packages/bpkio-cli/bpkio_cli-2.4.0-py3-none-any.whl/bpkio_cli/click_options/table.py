import functools

import click


def table_options(fn):
    @click.option(
        "-t",
        "--table",
        is_flag=True,
        type=bool,
        default=False,
        help="Show key information in tabular format (where supported)",
    )
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    return wrapper
