import functools

import click
from bpkio_cli.utils import OptionEatAll
from bpkio_cli.utils.datetimes import parse_date_expression_as_utc
from cloup import option, option_group


def slot_range_options(
    default_start="now", default_end="in 24 hours", times=True, allcats=False
):
    def decorator(fn):
        """Decorator to add multiple common decorators
        Idea from https://stackoverflow.com/questions/40182157/shared-options-and-flags-between-commands
        """

        time_options = []
        if times:
            time_options = [
                option(
                    "--start",
                    type=tuple,
                    cls=OptionEatAll,
                    default=[default_start],
                    help="Start time for first slot",
                    callback=transform_time_expression,
                ),
                option(
                    "--end",
                    type=tuple,
                    cls=OptionEatAll,
                    default=[default_end],
                    help="End time for last slot",
                    callback=transform_time_expression,
                ),
            ]

        cats_options = [
            option(
                "-cat",
                "--category",
                "categories",
                type=str,
                multiple=True,
                help="Categories of the slots",
                callback=validate_categories,
            ),
            option(
                "-nocat",
                "--no-category",
                "no_category",
                is_flag=True,
            ),
            option(
                "-allcats",
                "--all-categories",
                "all_categories",
                is_flag=True,
            ),
        ]

        @option_group("Range of slots", *time_options, *cats_options)  # type: ignore
        # @constraint(mutually_exclusive, ["categories", "no_category", "all_categories"])
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def transform_time_expression(ctx, param, value):
    try:
        start_time = parse_date_expression_as_utc(value, future=True)
        return start_time
    except ValueError:
        raise click.BadParameter("The date or time expression cannot be parsed")


def validate_categories(ctx, param, value):
    # A None value will be used to retrieve slots without categories
    if ctx.params.get("no_category"):
        return None

    if ctx.params.get("all_categories"):
        resources = ctx.obj.api.categories.list()
        return [r.id for r in resources]

    categories = []
    if value and isinstance(value, tuple):
        for cat in value:
            if cat.isdigit():
                categories.append(int(cat))
            else:
                resources = ctx.obj.api.categories.search(cat)
                if len(resources) == 0:
                    click.secho(f"Category `{cat}` not found and is ignored")
                else:
                    categories.append(resources[0].id)

        # Check that we didn't end up with none
        if len(value) and len(categories) == 0:
            raise click.BadParameter("No valid category found")

    return categories
