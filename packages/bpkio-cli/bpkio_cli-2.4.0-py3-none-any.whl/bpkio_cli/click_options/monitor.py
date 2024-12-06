import functools

from cloup import option, option_group


def monitor_options(fn):
    @option_group(
        "Polling options",
        option(
            "--save",
            is_flag=True,
            default=False,
            help="Saves monitoring information to file",
        ),
        option(
            "+map/-map",
            "--show-map/--hide-map",
            "with_map",
            is_flag=True,
            default=True,
            help="Shows a graphical representation of the segments contained in the manifest",
        ),
        option(
            "+sig/-sig",
            "--show-signals/--hide-signals",
            "with_signals",
            is_flag=True,
            default=True,
            help="Shows details of new signals (such as markers)",
        ),
        option(
            "+ad/-ad",
            "--show-adinfo/--hide-adinfo",
            "with_adinfo",
            is_flag=True,
            default=True,
            help="Shows details of the inserted ads",
        ),
        option(
            "+sch/-sch",
            "--show-schedule/--hide-schedule",
            "with_schedule",
            is_flag=True,
            default=False,
            help="Shows the events as a schedule (one column per signal type)",
        ),
        option(
            "+frm/-frm",
            "--show-frames/--hide-frames",
            "with_frames",
            is_flag=True,
            default=False,
            help="Shows a frame from each new segment",
        ),
    )
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    return wrapper
