import functools

from cloup import option, option_group


def read_options(fn):
    @option_group(
        "Content display options",
        option(
            "--raw",
            is_flag=True,
            type=bool,
            default=False,
            help="Get the raw content, unchanged",
        ),
        option("--top", type=int, default=0, help="Only display the first N lines"),
        option("--tail", type=int, default=0, help="Only display the last N lines"),
        option(
            "--pager/--no-pager",
            type=bool,
            is_flag=True,
            default=None,
            help="Display through a pager (to allow scrolling). "
            + "If the flag is not set, a pager will automatically be used if the content "
            + "is too long to fit on screen. "
            + "In the pager, use keyboard shortcuts to navigate and search; "
            + "type `h` for help on available shortcuts",
        ),
        option(
            "--trim",
            type=int,
            default=0,
            is_flag=False,
            flag_value=200,
            help="Trim lines to this length (for text-based content only, such as HLS)",
        ),
        option(
            "--ad-pattern",
            type=str,
            default="/bpkio-jitt",
            help="Substring of a segment URL that indicates that it's an ad segment",
        ),
    )
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    return wrapper
