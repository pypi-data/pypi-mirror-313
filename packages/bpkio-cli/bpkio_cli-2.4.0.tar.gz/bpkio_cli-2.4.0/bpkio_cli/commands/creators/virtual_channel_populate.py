import copy
import math
from datetime import datetime, timedelta

import bpkio_cli.click_mods.resource_commands as bic_res_cmd
import bpkio_cli.click_options as bic_options
import bpkio_cli.utils.prompt as prompt
import click
import cloup
from bpkio_api.helpers.source_type import SourceTypeDetector
from bpkio_api.helpers.times import relative_time
from bpkio_api.models import (AssetSourceIn, LiveSourceIn, SourceType,
                              VirtualChannelService, VirtualChannelSlotIn,
                              VirtualChannelSlotType)
from bpkio_cli.commands.creators.slot_iterators import clear_slots
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.config_provider import CONFIG
from bpkio_cli.core.resource_decorator import add_category_info
from bpkio_cli.utils.datetimes import (parse_date_expression_as_utc,
                                       parse_duration_expression)
from bpkio_cli.utils.progressbar import widgets_slots
from bpkio_cli.writers.colorizer import Colorizer as CL
from media_muncher.handlers import ContentHandler, factory
from progressbar import ProgressBar

MAX_REPEAT = 100
ADBREAK_DEFAULT_DURATION = "2 min"


def populate_virtual_channel_slots_command():
    # COMMAND: POPULATE
    @bic_res_cmd.command(help="Populate the slots of a Virtual Channel service")
    @bic_options.slots(times=False)
    @click.pass_obj
    def populate(obj: AppContext, categories, **kwargs):
        vc_id = obj.resource_chain.last_key()
        populate_virtual_channel_slots_with_prompts(obj, vc_id, categories)

    return populate


def populate_virtual_channel_slots_with_prompts(context: AppContext, vc_id, categories):
    api = context.api.services.virtual_channel
    vc: VirtualChannelService = api.retrieve(vc_id)
    supports_ads = vc.adBreakInsertion is not None

    slot_sources = _get_compatible_sources(context, vc.format)

    # Ask for population mode
    modes = [
        dict(value="INDIV", name="Slot by slot - most control over timing, but slower"),
        dict(value="FAST", name="Groups of assets - less control, but faster"),
    ]
    pop_mode = prompt.select(message="Populate mode", choices=modes)

    if categories is None or len(categories) == 0:
        categories = [None]

    # Ask for a category (if not provided)
    # if len(categories):
    #     category_id = _select_category(context.api, categories)
    # else:
    #     category_id = None

    # Start building an asset plan
    click.secho("\nDefine schedule for the channel", fg="yellow")

    asset_plan = []
    if pop_mode == "INDIV":
        asset_plan = _define_asset_plan_slot_by_slot(context.api, vc, slot_sources)
    elif pop_mode == "FAST":
        asset_plan = _define_asset_plan_fast(context.api, vc, slot_sources)

    click.echo()

    if not len(asset_plan):
        return

    # Ask whether to allow transition/gaps between assets
    if len(asset_plan) > 1:
        gaps = _select_gaps(
            slot_sources, mode="within-block", adbreaks_allowed=supports_ads
        )
    else:
        gaps = []

    plan = []
    for i, element in enumerate(asset_plan):
        plan.append(element)
        if i < len(asset_plan) - 1:
            plan.extend(gaps)

    # Ask if the plan are to be repeated
    repeat = prompt.text(
        message="How many times should this schedule repeat?",
        long_instruction="Use a number or a duration expression (eg. 2h, 30m)",
        default="1",
    )

    # Ask whether to add gaps between repeats
    if repeat != "1":
        gaps2 = _select_gaps(
            slot_sources,
            mode="between-blocks",
            adbreaks_allowed=supports_ads,
            previous=gaps,
        )
        plan.extend(gaps2)

    # Ask for a starting time
    starting_at = _determine_schedule_start_time(api, vc_id)

    # Calculate end time
    until_time = None
    if repeat.isdigit():
        repeat = int(repeat)
    else:
        duration = parse_duration_expression(repeat)
        until_time = starting_at + timedelta(seconds=duration)
        repeat = MAX_REPEAT

    # Define the schedule with actual times
    final_schedule = []
    t0 = starting_at
    try:
        for i in range(repeat):
            for j in range(len(plan)):
                effective_slot = copy.copy(plan[j])
                effective_slot["start"] = t0

                if until_time and effective_slot["start"] >= until_time:
                    raise StopAdding

                if effective_slot["source_id"] != "GAP":
                    final_schedule.append(effective_slot)

                t0 += timedelta(seconds=effective_slot["duration"])

    except StopAdding:
        pass  # and continue

    slots_created = []
    for category in categories:
        # Clear slots if necessary
        _clear_conflicting_slots(api, final_schedule, vc_id, category)

        # Now create the slots
        slots = _create_slots_via_api(api, vc_id, category, final_schedule)
        slots_created.extend(slots)

    context.response_handler.treat_list_resources(
        slots_created,
        select_fields=[
            "id",
            "name",
            "type",
            "relativeStartTime",
            "relativeEndTime",
            "duration",
            "replacement.id",
            "replacement.name",
            "category.id",
            "category.name",
        ],
    )


def _select_category(api, categories):
    if isinstance(categories, list) and len(categories) == 0:
        categories = api.categories.list()
        categories = sorted(categories, key=lambda c: c.name)
        category_choices = [
            dict(value=c.id, name=f"({c.id})  {c.name}") for c in categories
        ]
        category_choices.insert(0, dict(value=None, name="-- No category --"))

        category_id = prompt.fuzzy(
            message="What category do you want to associate the schedule with?",
            choices=category_choices,
        )
    else:
        category_id = categories[0] if isinstance(categories, list) else None
    return category_id


def _get_compatible_sources(context, format):
    all_sources = context.api.sources.list()

    # Determine the list of compatible sources
    slot_sources = [
        s
        for s in all_sources
        if s.type in (SourceType.LIVE, SourceType.ASSET) and s.format == format
    ]
    slot_sources = sorted(slot_sources, key=lambda s: s.id, reverse=True)
    slot_sources = context.cache.sort_resources_by_most_recently_accessed(slot_sources)
    return slot_sources


def _make_source_choices(
    candidate_sources, ad_breaks_allowed=False, urls_allowed=False
):
    choices = [
        dict(value=s.id, name=f"({s.id})  {s.name}  [{s.type.value}]")
        for s in candidate_sources
    ]

    if urls_allowed:
        choices.append(dict(value="BYURL", name="-- From URL --"))

    if ad_breaks_allowed:
        choices.append(dict(value="ADBREAK", name="-- Ad Break --"))

    choices.append(dict(value=None, name="-- End of schedule --"))

    return choices


def _define_asset_plan_slot_by_slot(api, vc, slot_sources):
    default_adbreak_duration = ADBREAK_DEFAULT_DURATION
    asset_plan = []

    while True:
        # Ask for a source
        supports_ads = vc.adBreakInsertion is not None

        source_choices = _make_source_choices(slot_sources, supports_ads)
        msg = "Source to add" if len(asset_plan) == 0 else "Next source to add"
        source_id = prompt.fuzzy(message=msg, choices=source_choices)

        # Stop the loop if the user wants to end the schedule
        if source_id is None:
            break

            # retrieve the source from the source list
        source = None
        if isinstance(source_id, int) or source_id.isdigit():
            source = next(s for s in slot_sources if s.id == source_id)

            # allow new source
        if source_id == "BYURL":
            url = prompt.text(message="Source URL", level=1)

            source_type = SourceTypeDetector.determine_source_type(url)
            name = ".." + url[-30:] if len(url) > 30 else url

            match source_type:
                case SourceType.LIVE:
                    name = "Live Source for VC: .." + name
                    (source, status) = api.sources.live.upsert(
                        LiveSourceIn(name=name, url=url), if_exists="retrieve"
                    )
                    source_id = source.id
                case SourceType.ASSET:
                    name = "Source Asset for VC: .." + name
                    (source, status) = api.sources.asset.upsert(
                        AssetSourceIn(name=name, url=url), if_exists="retrieve"
                    )
                    source_id = source.id
                case _:
                    click.secho(
                        f"Source type not supported in VCs: {source_type}",
                        fg="red",
                    )
                    source_id = "SKIP"

            if source:
                click.secho(
                    f"     » Source {source.id}: {status.name.lower()}", fg="green"
                )
            if source.format != vc.format:
                click.secho(
                    f"     ! Source {source.id} has wrong format ({source.format} != {vc.format})",
                    fg="red",
                )
                source = None
                source_id = "SKIP"

            # set default duration for valid sources
        if source_id == "ADBREAK":
            default_duration = default_adbreak_duration

        if source:
            if source.type == SourceType.LIVE:
                default_duration = "10 min"
            else:
                default_duration = str(_get_duration_from_asset(source.full_url))

        if source_id != "SKIP":
            # ask for duration to insert
            duration = prompt.text(
                message="Duration",
                default=default_duration,
                level=1,
                filter=lambda t: parse_duration_expression(t),
                transformer=lambda t: str(
                    timedelta(seconds=parse_duration_expression(t))
                ),
                long_instruction="Use a number (of seconds) or a duration expression (eg. 2h, 30m)",
            )

            if source_id == "ADBREAK":
                default_adbreak_duration = str(duration)

            asset_plan.append(dict(source_id=source_id, duration=duration))

    return asset_plan


def _define_asset_plan_fast(api, vc, slot_sources):
    asset_plan = []
    source_ids = []

    # Collect sources
    while len(source_ids) == 0:
        msg = "Select sources to add"
        source_choices = _make_source_choices(
            slot_sources, ad_breaks_allowed=False, urls_allowed=False
        )
        source_ids = prompt.fuzzy_build_list(message=msg, choices=source_choices)

    click.echo()

    # Ask for duration
    NATURAL = "duration of asset (from manifest)"
    preferred_duration = prompt.text(
        message="Duration for the associated slots",
        level=0,
        default=NATURAL,
        filter=lambda t: parse_duration_expression(t) if t != NATURAL else NATURAL,
        transformer=lambda t: (
            str(timedelta(seconds=parse_duration_expression(t)))
            if t != NATURAL
            else NATURAL
        ),
        long_instruction="Use a number (of seconds) or a duration expression (eg. 2h, 30m). \nUse '0' for natural asset duration",
    )

    for source_id in source_ids:
        duration = preferred_duration
        if duration == 0 or duration == NATURAL:
            source = next(s for s in slot_sources if s.id == source_id)
            if source:
                if source.type == SourceType.LIVE:
                    duration = "10 min"
                else:
                    duration = _get_duration_from_asset(source.full_url)
                    click.echo(
                        CL.markup(f"  -> Duration of source '{source_id}' = {duration}")
                    )

        asset_plan.append(dict(source_id=source_id, duration=duration))

    return asset_plan


def _select_gaps(slot_sources, mode, adbreaks_allowed=False, previous=None):
    inters = []

    while True:
        choices = [
            dict(value="GAP", name="Gap"),
            dict(value="ASSET", name="Asset"),
            dict(value=None, name="-- Nothing / End of Break--"),
        ]
        if mode == "within-block":
            msg = (
                "Do you want to insert a break between each of those slots?"
                if len(inters) == 0
                else "Do you want to insert something else in between slots?"
            )
        if mode == "between-blocks":
            msg = (
                "Do you want to insert something between repeats of this schedule?"
                if len(inters) == 0
                else "Do you want to insert something else in between repeats of the schedule?"
            )

        if adbreaks_allowed:
            choices.insert(-1, dict(value="ADBREAK", name="Ad Break"))

        if previous:
            choices.insert(
                -1, dict(value="PREVIOUS", name="-- Same as defined before --")
            )

        gap_type = prompt.select(
            message=msg,
            choices=choices,
            default=None,
        )

        if gap_type is None:
            break

        if gap_type == "PREVIOUS":
            inters = previous
            break

        if gap_type == "ADBREAK":
            duration = prompt.text(
                message="What is the duration of the ad break?",
                default=ADBREAK_DEFAULT_DURATION,
                level=1,
                filter=lambda t: parse_duration_expression(t),
                transformer=lambda t: str(
                    timedelta(seconds=parse_duration_expression(t))
                ),
                long_instruction="Use a number or a duration expression (eg. 2h, 30m)",
            )
            inters.append(dict(source_id=gap_type, duration=duration))
        elif gap_type == "GAP":
            duration = prompt.text(
                message="What is the duration of the gap?",
                default="5s",
                level=1,
                filter=lambda t: parse_duration_expression(t),
                transformer=lambda t: str(
                    timedelta(seconds=parse_duration_expression(t))
                ),
                long_instruction="Use a number or a duration expression (eg. 2h, 30m)",
            )
            inters.append(dict(source_id=gap_type, duration=duration))
        elif gap_type == "ASSET":
            source_choices = _make_source_choices(slot_sources, ad_breaks_allowed=False)
            source_id = prompt.fuzzy(message="Source to add", choices=source_choices)
            source = next(s for s in slot_sources if s.id == source_id)
            default_duration = str(_get_duration_from_asset(source.full_url))
            duration = prompt.text(
                message="Duration",
                default=default_duration,
                level=1,
                filter=lambda t: parse_duration_expression(t),
                transformer=lambda t: str(
                    timedelta(seconds=parse_duration_expression(t))
                ),
                long_instruction="Use a number (of seconds) or a duration expression (eg. 2h, 30m)",
            )
            inters.append(dict(source_id=source_id, duration=duration))

    return inters


def _determine_schedule_start_time(api, vc_id):
    starting_at = None
    while starting_at is None:
        starting_at = prompt.text(
            message="Starting time",
            default="in 30 sec",
            filter=lambda t: _parse_start_time_prompt(t, filter=True),
            transformer=lambda t: _parse_start_time_prompt(t, filter=False),
            long_instruction="Use an exact time, or a time expression "
            "(eg. 'in 10 min', 'tomorrow 10am', 'now').  "
            "Or use 'slot' if you want to align with an existing future slot",
        )

        # Optionally select a slot to align with
        if starting_at == "SLOT":
            candidate_slots = api.slots.list(
                vc_id,
                from_time=datetime.now(),
                to_time=datetime.now() + timedelta(hours=4),
            )
            add_category_info(candidate_slots)
            if not candidate_slots:
                click.echo(CL.error("No present or future slot found"))
                starting_at = None  # ready to go back through the while loop
            else:
                slot_choices = [
                    dict(
                        value=sl.id,
                        name=f"from {sl.startTime} - ({sl.id}) {sl.type}"
                        f"{': ' + sl.replacement.name if sl.replacement else ''}"
                        f"{'  [cat: ' + sl.category.name + ']' if sl.category else ''}",
                    )
                    for sl in candidate_slots
                ]
                slot_id = prompt.fuzzy(
                    message="Select a slot to align with", choices=slot_choices
                )
                slot = next(s for s in candidate_slots if s.id == slot_id)

                starting_at = prompt.select(
                    message="What end of the slot do you want to align to?",
                    choices=[
                        dict(
                            value=slot.startTime,
                            name=f"Start - {relative_time(slot.startTime)}",
                        ),
                        dict(
                            value=slot.endTime,
                            name=f"End - {relative_time(slot.endTime)}",
                        ),
                    ],
                )
    # end while
    return starting_at


def _clear_conflicting_slots(api, final_schedule, vc_id, category_id):
    schedule_start = final_schedule[0]["start"]
    schedule_end = final_schedule[-1]["start"] + timedelta(
        seconds=final_schedule[-1]["duration"]
    )
    existing_slots = api.slots.list(
        vc_id,
        from_time=schedule_start,
        to_time=schedule_end,
        categories=category_id,
    )
    if existing_slots:
        clear = prompt.confirm(
            message=f"There are {len(existing_slots)} conflicting slots in this channel for category {category_id}. "
            "Would you like to clear them?",
            default=False,
        )

        if clear:
            clear_slots(
                api,
                service_id=vc_id,
                start=schedule_start,
                end=schedule_end,
                categories=category_id,
            )
        # else:
        #     raise click.Abort()


def _create_slots_via_api(api, vc_id, category_id, final_schedule):
    widget_title = "Creating slots"
    if category_id:
        widget_title += f" for category {category_id}"
    else:
        widget_title += " (no category)"

    slots = []
    failed_messages = []
    with ProgressBar(
        widgets=widgets_slots(widget_title),
        max_value=len(final_schedule),
        redirect_stdout=True,
    ) as bar:
        for i, sched in enumerate(final_schedule):
            try:
                if sched["source_id"] == "ADBREAK":
                    slot = VirtualChannelSlotIn(
                        startTime=sched["start"],
                        duration=sched["duration"],
                        type=VirtualChannelSlotType.AD_BREAK,
                    )
                else:
                    slot = VirtualChannelSlotIn(
                        startTime=sched["start"],
                        duration=sched["duration"],
                        replacement=dict(id=sched["source_id"]),
                        type=VirtualChannelSlotType.CONTENT,
                    )
                if category_id:
                    slot.category = dict(id=category_id)

                slot = api.slots.create(vc_id, slot)
                slots.append(slot)

            except Exception as e:
                failed_messages.append(e)

            bar.update(i, success=len(slots), error=len(failed_messages))

    if len(failed_messages):
        click.secho(f"Failed to create {len(failed_messages)} slots", fg="red")
        click.secho("- " + "\n- ".join(map(str, failed_messages)), fg="red")

    # decorate with the full categories
    add_category_info(slots)
    return slots


def _parse_start_time_prompt(t: str, filter=False):
    if t.startswith("slot"):
        return "SLOT"

    try:
        if filter:
            # returned value
            return parse_date_expression_as_utc(t)
        else:
            # displayed value
            return relative_time(parse_date_expression_as_utc(t))
    except Exception as e:
        return None


def _get_duration_from_asset(url):
    handler: ContentHandler = factory.create_handler(
        url, user_agent=CONFIG.get_user_agent()
    )
    return math.floor(handler.get_duration())


class StopAdding(Exception):
    pass
