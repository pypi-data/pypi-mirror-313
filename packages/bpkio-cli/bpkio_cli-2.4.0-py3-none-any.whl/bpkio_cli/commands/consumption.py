import click
import cloup
from bpkio_cli.click_mods.option_eat_all import OptionEatAll
from bpkio_cli.utils.datetimes import (get_utc_date_ranges,
                                       parse_date_expression_as_utc)


@cloup.command()
@click.option(
    "-s",
    "--start",
    type=tuple,
    cls=OptionEatAll,
    default=("5 months ago",),
    help="Start time",
)
@click.option(
    "-e", "--end", type=tuple, cls=OptionEatAll, default=("now",), help="End time"
)
@click.option(
    "--by",
    type=click.Choice(["day", "week", "month"]),
    required=False,
    default="month",
    help="Split the data in ranges of dates",
)
@click.option(
    "--tenant",
    type=int,
    required=False,
    help="[ADMIN] ID of the tenant",
)
@click.pass_obj
def consumption(obj, start, end, by, tenant):
    """Extract consumption/billing info"""

    start = parse_date_expression_as_utc(start)
    end = parse_date_expression_as_utc(end)

    if not by:
        # cons = obj.api.consumption.retrieve(start, end, tenant)
        cons = obj.api.consumption.retrieve(start, end)
        obj.response_handler.treat_single_resource(cons)
        return

    else:
        ranges = get_utc_date_ranges(from_time=start, to_time=end, unit=by)
        data = []
        for start, end in ranges:
            # data.append(obj.api.consumption.retrieve(start, end, tenant))
            data.append(obj.api.consumption.retrieve(start, end, tenant))

        obj.response_handler.treat_list_resources(
            data,
            select_fields=[
                "tenantId",
                "startTime",
                "endTime",
                "days",
                "egress",
                "virtualChannel",
                "contentReplacement",
                "insertedAds",
            ],
        )
    return
